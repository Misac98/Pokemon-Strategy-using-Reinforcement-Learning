from poke_env.teambuilder import Teambuilder
import os
import numpy as np


class StaticTeamFromPool(Teambuilder):
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return self.teams[0]

class RandomTeamFromPool(Teambuilder):
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return np.random.choice(self.teams)
    
def read_teams_from_file(relative_path):
    teamsPaths = []
    for root, dirs, files in os.walk(relative_path):
        for file in files:
            teamsPaths.append(os.path.join(root,file))

    teams = []
    for teamPath in teamsPaths:
        with open(teamPath, "r") as team:
            teams.append(team.read())

    return teams