import re
import requests

from bs4 import BeautifulSoup


#
# URL generators.
#
def invite_url(tourn_id):
    return f'https://www.tabroom.com/index/tourn/index.mhtml?tourn_id={tourn_id}'


def entries_url(tourn_id):
    return f'https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tourn_id}'


#
# Data processing.
#
def is_valid_tournament(tourn_id):
    response = requests.get(invite_url(tourn_id))
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return not 'Invalid tourn ID or URL' in text and not 'This event\'s field is not published by the tournament' in text


def get_events(tourn_id):
    response = requests.get(entries_url(tourn_id))
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('a')
    events = []
    events_name = []
    for a in results:
        href = a.get('href')
        if href and href.startswith(f'/index/tourn/fields.mhtml?tourn_id={tourn_id}&event_id='):
            events.append(href.split('=')[-1])
            events_name.append(a.get_text().strip())
    return (events, events_name)


def get_pairings(tourn_id, event_id):
    # Get round info
    data = {'tourn_id': tourn_id, 'event_id': event_id}
    response = requests.post(f'https://www.tabroom.com/index/tourn/postings/index.mhtml', data=data)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('a', class_='dkblue full nowrap')
    if not results: return None

    round_number = parse_round_number(results[0].get_text())
    round_url = f'https://www.tabroom.com{results[0].get("href")}'

    # Get pairings from round
    response = requests.get(round_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    has_online_rounds = 'ONL' in soup.get_text()

    round_data = []
    results = soup.find_all('tr')
    for row in results:
        cells = row.find_all('td')
        cur = []
        for i in range(len(cells)):
            if has_online_rounds and i == 1: continue # Skip if online column
            cur.append(cells[i].text.replace('\n', ' ').strip())
            # Add URL if it exists
            try:
                url = cells[i].contents[1].get('href')
                if url:
                    if url.startswith('/index'): # Tournament entry
                        cur.append(f'https://www.tabroom.com{url}')
                    else: # Judge paradigm
                        cur.append(f'https://www.tabroom.com/index/tourn/postings/{url}')
            except Exception as e:
                # print(f'Exception in get_pairings: {e}')
                pass
        round_data.append(cur)

    return [round_number, round_data[1:]]


def filter_round_data(data, round_number, school_name, school_judges):
    res_competitors, res_judges = [], []

    # Prelims
    if round_number[0].isnumeric():
        try:
            for row in data:
                # De-magic-number data and cleanup
                round_room = row[0]
                round_aff = row[1]
                round_aff_page = row[2]
                round_neg = row[3]
                round_neg_page = row[4]
                round_judges = row[5::2]
                round_judges_pages = row[6::2]

                round_judges = [' '.join(j.split()) for j in round_judges]

                if school_name in round_aff:
                    res_competitors.append([' '.join(round_aff.split()[1:]),
                                            'Aff',
                                            (round_neg, round_neg_page),
                                            list(zip(round_judges, round_judges_pages)),
                                            round_room])
                if school_name in round_neg:
                    res_competitors.append([' '.join(round_neg.split()[1:]),
                                            'Neg',
                                            (round_aff, round_aff_page),
                                            list(zip(round_judges, round_judges_pages)),
                                            round_room])

                for sj in school_judges:
                    for rj in round_judges:
                        if sj in rj:
                            res_judges.append([sj, round_judges, round_aff, round_neg, round_room])
        except Exception as e:
            print(f'Exception in filter_round_data (prelims): {e}')
            pass

    # Elims
    else:
        try:
            for row in data:
                # De-magic-number data and cleanup
                round_room = row[0]
                round_side_1 = row[1]
                round_side_1_page = row[2]
                round_side_2 = row[3]
                round_side_2_page = row[4]
                round_judges = row[5::2]
                round_judges_pages = row[6::2]

                round_judges = [' '.join(j.split()) for j in round_judges]

                if school_name in round_side_1:
                    if "Locked" in round_side_1:
                        res_competitors.append([' '.join(round_side_1.split()[1:-2]),
                                                round_side_1.split()[-1],
                                                (' '.join(round_side_2.split()[:-2]), round_side_2_page),
                                                list(zip(round_judges, round_judges_pages)),
                                                round_room])
                    else:
                        res_competitors.append([' '.join(round_side_1.split()[1:]),
                                                'Flip',
                                                (round_side_2, round_side_2_page),
                                                list(zip(round_judges, round_judges_pages)),
                                                round_room])
                if school_name in round_side_2:
                    if "Locked" in round_side_2:
                        res_competitors.append([' '.join(round_side_2.split()[1:-2]),
                                                round_side_2.split()[-1],
                                                (' '.join(round_side_1.split()[:-2]), round_side_1_page),
                                                list(zip(round_judges, round_judges_pages)),
                                                round_room])
                    else:
                        res_competitors.append([' '.join(round_side_2.split()[1:]),
                                                'Flip',
                                                (round_side_1, round_side_1_page),
                                                list(zip(round_judges, round_judges_pages)),
                                                round_room])


                for sj in school_judges:
                    for rj in round_judges:
                        if sj in rj:
                            res_judges.append([sj, round_judges, round_side_1, round_side_2, round_room])
        except Exception as e:
            print(f'Exception in filter_round_data (elims): {e}')
            pass

    return [round_number, [sorted(res_competitors), sorted(res_judges)]]


# This exists to avoid tabroom variance with blasts.
def is_valid_blast(prev_data, cur_data):
    if cur_data and cur_data[1] and not prev_data: return True
    if prev_data == cur_data: return False
    if not cur_data or not cur_data[1]: return False
    if prev_data[0][1] > cur_data[0][1]: return False
    return True


#
# Round number processing.
#
regex_to_round = {
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        'tr': 'Triples',
        'sex': 'Doubles',
        'd': 'Doubles',
        'oct': 'Octos',
        'q': 'Quarters',
        'sem': 'Semis',
        'fin': 'Finals',
        }


round_enum = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        'Triples': 9,
        'Doubles': 10,
        'Octos': 11,
        'Quarters': 12,
        'Semis': 13,
        'Finals': 14,
        }


def parse_round_number(round_name):
    round_name = round_name.lower().split()[-1]
    regex = re.search('(\\d+)|(sex)|(d)|(oct)|(q)|(tr)|(sem)|(fin)', round_name)
    return (None, -1) if not regex else (regex_to_round[regex.group()], round_enum[regex_to_round[regex.group()]])
