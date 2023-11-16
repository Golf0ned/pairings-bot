# pairings.py

import requests

validRounds = ["1", "2", "3", "4", "5", "6", "7", "8",
               "triples", "doubles", "octos", "quarters", "semis", "finals"]

class PairingsManager():

    def __init__(self):
        self.school = "Northwestern"
        self.tournamentID = 0

    def setSchool(self, school : str):
        self.school = school

    def setTournament(self, id : int):
        if id < 0:
            # TODO: error checking for id >= 0
            pass
        self.tournamentID = id

    def getRoundURL(self, round):
        if round not in validRounds:
            # TODO: error checking for invalid round 
            pass
        return f'https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id={self.tournamentID}&round_id={round}'


