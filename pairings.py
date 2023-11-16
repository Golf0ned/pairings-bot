# pairings.py

import requests

validRounds = ["1", "2", "3", "4", "5", "6", "7", "8",
               "triples", "doubles", "octos", "quarters", "semis", "finals"]

class PairingsManager():

    def __init__(self):
        self.__school = "Northwestern"
        self.__tournamentID = 0
        self.__roundManager = RoundManager()
        self.__blasting = False
        self.__blastChannel = ""

    def setSchool(self, school : str): self.__school = school

    def getSchool(self): return self.__school

    def setTournament(self, id : int): 
        if id < 0:
            # TODO: error checking for id >= 0
            pass
        self.__tournamentID = id
    
    def isBlasting(self): return self.__blasting
        
    def startBlasting(self): self.__blasting = True

    def stopBlasting(self): self.__blasting = False

    def setBlastChannel(self, id : str): self.__blastChannel = id

    def getBlastChannel(self): return self.__blastChannel

    def getRoundURL(self, round):
        if round not in validRounds:
            # TODO: error checking for invalid round 
            pass
        return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={self.__tournamentID}&round_id={round}'


class RoundManager():

    def __init__(self):
        pass