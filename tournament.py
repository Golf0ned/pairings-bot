#tournament.py
import asyncio
import re
import requests

def getPairingsURL(tournamentID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournamentID}'
def getRoundURL(tournamentID, roundID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={tournamentID}&round_id={roundID}'


class TournamentManager():

    def __init__(self, school, tournamentID):
        self.__school = school
        self.__tournamentID = tournamentID

        parser = TournamentParser()

    async def checkRoundOne(interval):
        roundOneOut = False
        while(not roundOneOut):
            # code goes hsere
            await asyncio.sleep(interval)



class TournamentParser():

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
    
    def __init__(self):
        pass
    
    def parseRound(self, round):
        
        round = TournamentParser.parseRoundNumber(round)
        if round == "1":
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
        return TournamentParser.REGEXTOROUND[regex[0]]
        