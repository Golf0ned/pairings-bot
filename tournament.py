#tournament.py
import re
import requests

from bs4 import BeautifulSoup

REGEXTOROUND = {"1" : "1",
                "2" : "2",
                "3" : "3",
                "4" : "4",
                "5" : "5",
                "6" : "6",
                "7" : "7",
                "8" : "8",
                "tr" : "Triples",
                "sex" : "Doubles",
                "d" : "Doubles",
                "oct" : "Octos",
                "q" : "Quarters",
                "sem" : "Semis",
                "fin" : "Finals"}

ROUNDENUM = {None : 0,
             "1" : 1,
             "2" : 2,
             "3" : 3,
             "4" : 4,
             "5" : 5,
             "6" : 6,
             "7" : 7,
             "8" : 8,
             "Triples" : 9,
             "Doubles" : 10,
             "Octos" : 11,
             "Quarters" : 12,
             "Semis" : 13,
             "Finals" : 14}

def getPairingsURL(tournamentID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournamentID}'
def getRoundURL(tournamentID, roundID): return f'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id={tournamentID}&round_id={roundID}'

def isValidTournament(tournamentID):
    url = f'https://www.tabroom.com/index/tourn/index.mhtml?tourn_id={tournamentID}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    text = ' '.join(soup.get_text().split())

    return not ('Invalid tourn ID or URL' in text)

def isValidEvent(tournamentID, eventID):
    url = f'https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tournamentID}&event_id={eventID}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    text = ' '.join(soup.get_text().split())
    print(text)

    return not ('Invalid event ID or URL' in text) and not ('This event\'s field is not published by the tournament' in text)



def parseRoundNumber(round):
    string = round.lower().split()[-1]
    regex = re.search('(\\d+)|(sex)|(d)|(oct)|(q)|(tr)|(sem)|(fin)', string)
    if not regex:
        return None
    return REGEXTOROUND[regex.group()]



class TournamentManager():

    def __init__(self, school, tournamentID, eventID):
        self.__school = school
        self.__tournamentID = tournamentID
        self.__eventID = eventID

        self.__round = None
        self.__roundURL = ""
        self.__teams = []
        self.__sides = []
        self.__opponents = []
        self.__judges = []
        self.__rooms = []



    def getTournamentID(self): return self.__tournamentID
    def getEventID(self): return self.__eventID
    def getRoundNumber(self): return self.__round
    def getRoundURL(self): return self.__roundURL



    def updateTournamentRound(self):

        # first, get round url
        data = {'tourn_id': self.__tournamentID,
                  'event_id': self.__eventID}
        response = requests.post('https://www.tabroom.com/index/tourn/postings/index.mhtml', data=data)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("a", class_="dkblue full nowrap")
        
        # empty
        if not results: return False
        
        roundNum = parseRoundNumber(results[0].string)
        postData = results[0]['href']

        # now, get round info
        response = requests.get(f'https://www.tabroom.com/{postData}')
        soup = BeautifulSoup(response.content, "html.parser")
        hasONL = 'ONL' in soup.get_text()
        
        # tableize data
        roundData = []
        results = soup.findAll('tr')

        for row in results:
            cols = row.findAll('td')
            newRow = []
            for cellInd in range(len(cols)):
                # skip if online column
                if hasONL and cellInd == 1:
                    continue
                # get text of cell
                newRow.append(cols[cellInd].text.strip())
                # get url of cell, if applicable
                url = cols[cellInd].contents[1].get('href')
                if url: 
                    if url[0:6] == '/index': # tournament entry
                        newRow.append(f'https://www.tabroom.com{url}')
                    else: # judge paradigm
                        newRow.append(f'https://www.tabroom.com/index/tourn/postings/{url}')

            roundData.append(newRow)

        # filter and blast
        filteredData = self.filterPairings(roundData[1:], roundNum)
        if self.updatePairings(filteredData, roundNum):
            self.__round = roundNum
            self.__roundURL = f'https://www.tabroom.com/{postData}'
            return True
        return False



    def filterPairings(self, data, round):
        out = []
        
        # prelim
        if round.isnumeric():
            try:
                for row in data:
                    room = row[0]
                    aff = row[1]
                    affPage = row[2]
                    neg = row[3]
                    negPage = row[4]
                    judge = row[5]
                    judgePage = row[6]

                    if self.__school in aff: 
                        out.append([' '.join(aff.split()[1:]),
                                    "Aff",
                                    (neg, negPage),
                                    [(judge, judgePage)],
                                    room])

                    if self.__school in neg:
                        out.append([' '.join(neg.split()[1:]),
                                    "Neg",
                                    (aff, affPage),
                                    [(judge, judgePage)],
                                    room])
            except:
                pass
        # elim
        else:
            for row in data:
                room = row[0]
                side1 = row[1]
                side1Page = row[2]
                side2 = row[3]
                side2Page = row[4]
                judges = row[5::2] # odd from 5-onwards
                judgePages = row[6::2] # even from 6-onwards

                if self.__school in side1:
                    if "Locked" in side1:
                        out.append([' '.join(side1.split()[1:-2]),
                                    side1.split()[-1],
                                    (' '.join(side2.split()[:-2]), side2Page),
                                    list(zip(judges, judgePages)),
                                    room])
                    else:
                        out.append([' '.join(side1.split()[1:]),
                                    "Flip",
                                    (side2, side2Page),
                                    list(zip(judges, judgePages)),
                                    room])
                        
                if self.__school in side2:
                    if "Locked" in side2:
                        out.append([' '.join(side2.split()[1:-2]),
                                    side2.split()[-1],
                                    (' '.join(side1.split()[:-2]), side1Page),
                                    list(zip(judges, judgePages)),
                                    room])
                    else:
                        out.append([' '.join(side2.split()[1:]),
                                    "Flip",
                                    (side1, side1Page),
                                    list(zip(judges, judgePages)),
                                    room])

        return sorted(out)



    def updatePairings(self, data, newRound):
        try:
            newTeams = []
            newSides = []
            newOpponents = []
            newJudges = []
            newRooms = []

            for row in data:
                newTeams.append(row[0])
                newSides.append(row[1])
                newOpponents.append(row[2])
                newJudges.append(row[3])
                newRooms.append(row[4])
            
            if self.validBlast(newRound, newTeams, newOpponents, newJudges, newRooms):
                self.__teams = newTeams
                self.__sides = newSides
                self.__opponents = newOpponents
                self.__judges = newJudges
                self.__rooms = newRooms
                return True
            return False
        except:
            print("Tried to get pairings: Tab error occured")
            return False



    def validBlast(self, newRound, teams, opponents, judges, rooms):
        # new round: blast
        if ROUNDENUM[newRound] > ROUNDENUM[self.__round]:
            return True
        # same round: blast if different opponents, judges, or rooms BUT only if not less
        elif ROUNDENUM[newRound] == ROUNDENUM[self.__round]:
            if len(teams) < len(self.__teams) or len([o for o in opponents if o]) < len(self.__opponents):
                return False
            elif (self.__opponents != opponents or self.__judges != judges or self.__rooms != rooms):
                return True
        # older round: don't blast
        return False



    def getTournamentRound(self):
        return[self.__teams,
               self.__sides,
               self.__opponents,
               self.__judges,
               self.__rooms]