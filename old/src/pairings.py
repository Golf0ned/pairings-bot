# pairings.py
import os

from dotenv import load_dotenv

from src import tournament

load_dotenv()
DEBUG = int(os.getenv('DEBUG'))

class PairingsManager():

    def __init__(self):
        self.__tournament = None
        self.__school = ''
        self.__judges = []
        self.__blastChannel = ''
        self.__blasting = False
        self.__hasBlast = False

    def initTournament(self, tournamentID, eventID):
        self.__tournament = tournament.TournamentManager(self.__school, self.__judges, tournamentID, eventID)
    
    def hasTournament(self): 
        return True if self.__tournament else False
    def getTournamentID(self): return self.__tournament.getTournamentID()
    def getRoundNumber(self): return self.__tournament.getRoundNumber()

    def getEventID(self): return self.__tournament.getEventID()

    def setSchool(self, school : str): self.__school = school
    def getSchool(self): return self.__school

    def setJudges(self, judges : list[str]): self.__judges = judges
    def getJudges(self): return self.__judges

    def isBlasting(self): return self.__blasting

    def startBlasting(self): self.__blasting = True
    def stopBlasting(self): self.__blasting = False

    def setBlastChannel(self, id : str): self.__blastChannel = id
    def getBlastChannel(self): return self.__blastChannel

    def hasBlast(self): 
        if self.__hasBlast:
            self.__hasBlast = False
            return True
        return False



    def checkForRound(self):
        if self.__tournament.updateTournamentRound():
            self.__hasBlast = True


    def getRoundInfo(self):
        return self.__tournament.getTournamentRound()

    def getRoundURL(self): return self.__tournament.getRoundURL()

    if DEBUG:
        def testBlast(self):
            self.__hasBlast = True
