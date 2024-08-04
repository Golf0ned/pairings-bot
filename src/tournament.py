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

    return not ('Invalid event ID or URL' in text) and not ('This event\'s field is not published by the tournament' in text)



def parseRoundNumber(round):
    string = round.lower().split()[-1]
    regex = re.search('(\\d+)|(sex)|(d)|(oct)|(q)|(tr)|(sem)|(fin)', string)
    if not regex:
        return None
    return REGEXTOROUND[regex.group()]



class TournamentManager():

    def __init__(self, school, judges, tournamentID, eventID):
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

        self.__teamJudges = sorted(judges)
        self.__teamJudgePanels = []
        self.__judgeTeam1 = []
        self.__judgeTeam2 = []
        self.__judgeRooms = []


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

        # TEST DATA
        roundNum = '1'
        postData = 'index/tourn/postings/round.mhtml?tourn_id=30545&round_id=1139574'

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
                try:
                    url = cols[cellInd].contents[1].get('href')
                    if url: 
                        if url[0:6] == '/index': # tournament entry
                            newRow.append(f'https://www.tabroom.com{url}')
                        else: # judge paradigm
                            newRow.append(f'https://www.tabroom.com/index/tourn/postings/{url}')
                except Exception as e:
                    # print(e)
                    pass

            roundData.append(newRow)

        # filter and blast
        filteredData = self.filterPairings(roundData[1:], roundNum)
        if self.updatePairings(filteredData, roundNum):
            self.__round = roundNum
            self.__roundURL = f'https://www.tabroom.com/{postData}'
            return True
        return False



    def filterPairings(self, data, round):
        outCompetitors = []
        outJudges = []
        
        # prelim
        if round.isnumeric():
            try:
                for row in data:
                    room = row[0]
                    aff = row[1]
                    affPage = row[2]
                    neg = row[3]
                    negPage = row[4]
                    judge = ' '.join(row[5].split())
                    judgePage = row[6]

                    if self.__school in aff: 
                        outCompetitors.append([' '.join(aff.split()[1:]),
                                    "Aff",
                                    (neg, negPage),
                                    [(judge, judgePage)],
                                    room])

                    if self.__school in neg:
                        outCompetitors.append([' '.join(neg.split()[1:]),
                                    "Neg",
                                    (aff, affPage),
                                    [(judge, judgePage)],
                                    room])

                    for j in self.__teamJudges:
                        if j in judge:
                            outJudges.append([judge, [judge], aff, neg, room])
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
                
                for i in range(len(judges)):
                    judges[i] = ' '.join(judges[i].split())

                if self.__school in side1:
                    if "Locked" in side1:
                        outCompetitors.append([' '.join(side1.split()[1:-2]),
                                    side1.split()[-1],
                                    (' '.join(side2.split()[:-2]), side2Page),
                                    list(zip(judges, judgePages)),
                                    room])
                    else:
                        outCompetitors.append([' '.join(side1.split()[1:]),
                                    "Flip",
                                    (side2, side2Page),
                                    list(zip(judges, judgePages)),
                                    room])
                        
                if self.__school in side2:
                    if "Locked" in side2:
                        outCompetitors.append([' '.join(side2.split()[1:-2]),
                                    side2.split()[-1],
                                    (' '.join(side1.split()[:-2]), side1Page),
                                    list(zip(judges, judgePages)),
                                    room])
                    else:
                        outCompetitors.append([' '.join(side2.split()[1:]),
                                    "Flip",
                                    (side1, side1Page),
                                    list(zip(judges, judgePages)),
                                    room])
                for j1 in judges:
                    for j2 in self.__teamJudges:
                        if j2 in j1:
                            outJudges.append([j2, judges, side1, side2, room])
        
        return [sorted(outCompetitors), sorted(outJudges)]



    def updatePairings(self, data, newRound):
        try:
            
            # competitors
            newCompetitorTeams = []
            newCompetitorSides = []
            newCompetitorOpponents = []
            newCompetitorJudges = []
            newCompetitorRooms = []
            for row in data[0]:
                newCompetitorTeams.append(row[0])
                newCompetitorSides.append(row[1])
                newCompetitorOpponents.append(row[2])
                newCompetitorJudges.append(row[3])
                newCompetitorRooms.append(row[4])

            # judges
            newSchoolJudges = []
            newJudgePanels = []
            newJudgeTeam1 = []
            newJudgeTeam2 = []
            newJudgeRooms = []
            for row in data[1]:
                newSchoolJudges.append(row[0])
                newJudgePanels.append(row[1])
                newJudgeTeam1.append(row[2])
                newJudgeTeam2.append(row[3])
                newJudgeRooms.append(row[4])

            newRoundData = (newCompetitorTeams, newCompetitorOpponents, newCompetitorJudges, newCompetitorRooms,
                            newSchoolJudges, newJudgePanels, newJudgeTeam1, newJudgeTeam2, newJudgeRooms)
            if self.validBlast(newRound, newRoundData):
                self.__teams = newCompetitorTeams
                self.__sides = newCompetitorSides
                self.__opponents = newCompetitorOpponents
                self.__judges = newCompetitorJudges
                self.__rooms = newCompetitorRooms

                self.__teamJudges = newSchoolJudges
                self.__teamJudgePanels = newJudgePanels
                self.__judgeTeam1 = newJudgeTeam1
                self.__judgeTeam2 = newJudgeTeam2
                self.__judgeRooms = newJudgeRooms

                return True
            return False
        except Exception as e:
            print("Tried to get pairings: Tab error occured")
            print(e)
            return False



    def validBlast(self, newRound, data):
        # new round: blast
        if ROUNDENUM[newRound] > ROUNDENUM[self.__round]:
            return True
        # same round: blast if different opponents, judges, or rooms BUT only if not less
        elif ROUNDENUM[newRound] == ROUNDENUM[self.__round]:
            if len(data[0]) < len(self.__teams) or len([o for o in data[1] if o]) < len(self.__opponents) or len([o for o in data[5] if o]) < len(self.__judgeTeam1) or len([o for o in data[6] if o]) < len(self.__judgeTeam2):
                return False
            elif (self.__opponents != data[1] or self.__judges != data[2] or self.__rooms != data[3] or self.__teamJudgePanels != data[5] or self.__judgeTeam1 != data[6] or self.__judgeTeam2 != data[7] or self.__judgeRooms != data[8]):
                return True
        # older round: don't blast
        return False



    def getTournamentRound(self):
        return [[self.__teams, self.__sides, self.__opponents, self.__judges, self.__rooms],
                [self.__teamJudges, self.__teamJudgePanels, self.__judgeTeam1, self.__judgeTeam2, self.__judgeRooms]]
