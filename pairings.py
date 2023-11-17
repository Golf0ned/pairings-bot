# pairings.py
import tournament

class PairingsManager():

    def __init__(self):
        self.__tournament = None
        self.__school = ''
        self.__blastChannel = ''
        self.__blasting = False
        self.__hasBlast = False

    def initTournament(self, id : str):
        self.__tournament = tournament.TournamentManager(self.__school, id)
    
    def hasTournament(self): 
        return True if self.__tournament else False
    def getTournamentID(self): return self.__tournament.getTournamentID()
    def getRoundNumber(self): return self.__tournament.getRoundNumber()

    def setSchool(self, school : str): self.__school = school
    def getSchool(self): return self.__school

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
        if self.__tournament.updateRound():
            self.__hasBlast = True


    def getRoundInfo(self):
        data = self.__tournament.getRound()

        res = [self.__tournament.getTeams()]
        for row in data:
            res.append(row)
        
        return res
