# pairings.py
import tournament

class PairingsManager():

    def __init__(self):
        self.__configured = False

        self.__school = ''
        self.__blastChannel = ''
        self.__blasting = False

        self.__tournament = None

    def setSchool(self, school : str): self.__school = school
    def getSchool(self): return self.__school


    def isBlasting(self): return self.__blasting
    def startBlasting(self): self.__blasting = True
    def stopBlasting(self): self.__blasting = False


    def setBlastChannel(self, id : str): self.__blastChannel = id
    def getBlastChannel(self): return self.__blastChannel


    def initTournament(self, id : str):
        self.__tournament = tournament.TournamentManager(self.__school, id)

    
    def getTournamentID(self): return self.__tournament.getTournamentID()
    def getTournamentName(self): return self.__tournament.getTournamentName()
    def getTournamentTeams(self): return self.__tournament.getTournamentTeams()
