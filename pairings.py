# pairings.py
import tournament

class PairingsManager():

    def __init__(self):
        self.__school = ""

        self.__blasting = False
        self.__blastChannel = ""

        self.tournament = None


    def setSchool(self, school : str): self.__school = school
    def getSchool(self): return self.__school


    def isBlasting(self): return self.__blasting
    def startBlasting(self): self.__blasting = True
    def stopBlasting(self): self.__blasting = False


    def setBlastChannel(self, id : str): self.__blastChannel = id
    def getBlastChannel(self): return self.__blastChannel


    def initTournament(self, id : int): 
        if id < 0:
            # TODO: error checking for id >= 0
            pass
        self.__tournament = tournament.TournamentManager(self.__school, id)


    def getTournamentURL(self): return tournament.getTournamentURL()
    def getRoundURL(self, roundID): return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={self.__tournamentID}&round_id={roundID}'
