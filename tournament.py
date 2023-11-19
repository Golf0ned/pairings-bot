#tournament.py
from bs4 import BeautifulSoup
import re
import requests

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



def getPairingsURL(tournamentID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournamentID}'
def getRoundURL(tournamentID, roundID): return f'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id={tournamentID}&round_id={roundID}'
def isValidTournament(tournamentID): return True
def isValidEvent(tournamentID, eventID): return True



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
        self.__name = ""

        self.__round = None
        self.__teams = []
        self.__sides = []
        self.__opponents = []
        self.__judges = []
        self.__rooms = []



    def getTournamentID(self): return self.__tournamentID
    def getEventID(self): return self.__eventID
    def getTournamentName(self): return self.__name
    def getRoundNumber(self): return self.__round



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

        roundData = []
        results = soup.findAll('tr')
        for row in results:
            cols = row.findAll('td')
            roundData.append([cell.text.strip() for cell in cols])

        filteredData = self.filterPairings(roundData[1:], roundNum)
        if self.updatePairings(filteredData, roundNum):
            self.__round = roundNum
            return True
        return False



    def filterPairings(self, data, round):
        out = []
        
        # prelim
        if round.isNumeric():
            for row in data:
                # print(row)
                room = row[0]
                aff = row[1]
                neg = row[2]
                judge = row[3]

                if self.__school in aff: 
                    out.append([aff.split()[-1], "Aff", neg, judge, room])

                if self.__school in neg:
                    out.append([neg.split()[-1], "Neg", aff, judge, room])

        # elim
        else:
            for row in data:
                # print(row)
                room = row[0]
                side1 = row[1]
                side2 = row[2]
                judges = ','.join(row[3:])

                if self.__school in side1:
                    if "Locked" in side1:
                        out.append([side1.split()[-3], side1.split()[-1], side2.split()[:-3], judges, room])
                    else:
                        out.append([side1.split()[-1], "Flip", side2, judges, room])
                if self.__school in side2:
                    if "Locked" in side2:
                        out.append([side2.split()[-3], side2.split()[-1], side1.split()[:-3], judges, room])
                    else:
                        out.append([side2.split()[-1], "Flip", side1, judges, room])

        return sorted(out)



    def updatePairings(self, data, round):
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
            
            if self.__round == round and len(newTeams) != self.__teams:
                return False
            elif (self.__round != round or
                self.__opponents != newOpponents or
                self.__judges != newJudges or
                self.__rooms != newRooms):
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



    def getTournamentRound(self):
        return[self.__teams,
               self.__sides,
               self.__opponents,
               self.__judges,
               self.__rooms]