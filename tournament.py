#tournament.py
import asyncio
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
                "tr" : "triples",
                "d" : "doubles",
                "oct" : "octos",
                "q" : "quarters",
                "sem" : "semis",
                "fin" : "finals"}

def getPairingsURL(tournamentID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournamentID}'
def getRoundURL(tournamentID, roundID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournamentID}&round_id={roundID}'
def isValidTournament(tournamentID) : return True

class TournamentManager():

    def __init__(self, school, tournamentID):
        self.__school = school
        self.__tournamentID = tournamentID
        self.__name = ""
        self.__teams = []

        self.__round = None
        parser = RoundParser()

    def getTournamentID(self): return self.__tournamentID
    def getTournamentName(self): return self.__name
    def getTournamentTeams(self): return self.__teams
    def getCurRound(self): return self.__round

    



class RoundParser():

    def __init__(self):
        pass
    
    def parseRound(self, round):
        
        round = RoundParser.parseRoundNumber(round)
        if round and round == "1":
            # tournamentName = 
            # teams = 
            pass
        # sides =
        # opponents = 
        # judges = 
        # rooms = 
        pass

    def parseRoundNumber(round):
        regex = re.findall('(\\d+)|(d)|(oct)|(q)|(tr)|(sem)|(fin)', round.split(' ')[-1].lower())
        if not regex:
            raise Exception()
        return REGEXTOROUND.get(regex[0], None)
        