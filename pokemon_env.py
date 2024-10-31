import numpy as np
from poke_env.teambuilder import Teambuilder
import time
import requests
# import matplotlib


class RandomTeamFromPool(Teambuilder):
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return np.random.choice(self.teams)
    

import os

relative_path = "pokémonTeams/teams1"

teamsPaths = []
for root, dirs, files in os.walk(relative_path):
	for file in files:
		teamsPaths.append(os.path.join(root,file))

teams = []
for teamPath in teamsPaths:
    with open(teamPath, "r") as team:
        teams.append(team.read())

custom_builder = RandomTeamFromPool(teams)

import subprocess
import json

def run_javascript(file_path, *args):
    result = subprocess.run(["node", file_path] + list(args), capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

from poke_env.player.player import Player
from poke_env.environment.abstract_battle import AbstractBattle

# Define a custom player by subclassing Player
class CustomPlayer(Player):
    def choose_move(self, battle: AbstractBattle):
        if battle.available_moves:
            return self.create_order(max(battle.available_moves, key=lambda move: move.base_power*move.accuracy))
        else:
            return self.choose_random_move(battle)

# Define a optimized player by subclassing Player
class OptimizedPlayer(Player):                
    def choose_move(self, battle: AbstractBattle):
        if battle.available_moves:
            attacker = battle.active_pokemon
            defender = battle.opponent_active_pokemon

            params = {
                'attackerName': str(attacker.species),
                'attackerLevel': str(attacker.level),
                'attackerItem': str(attacker.item),
                'attackerStatus':str(attacker.status),
                'attackerAbility':str(attacker.ability),
                'attackerBoosts':str(attacker.boosts),
                'defenderName': str(defender.species),
                'defenderLevel': str(defender.level),
                'defenderItem':  str(defender.item),
                'defenderStatus': str(defender.status),
                'defenderAbility': str(defender.ability),
                'defenderBoosts': str(defender.boosts),
                'moveName': None
            }
            
            average_damage_moves = {}
            for current_move in battle.available_moves:

                params['moveName'] = str(current_move.id)
                
                response = requests.get('http://localhost:3000/calculate-damage', params=params)
                calculate_damage = response.json()
                
                if calculate_damage == 0:
                    average_damage_moves[current_move] = 0
                else:
                    average_damage_moves[current_move] = sum(calculate_damage)/len(calculate_damage)
                    
            return self.create_order(max(average_damage_moves, key=average_damage_moves.get))
        else:
            return self.choose_random_move(battle)

from poke_env import RandomPlayer

generation = "gen2ou"

optimized_player = OptimizedPlayer(
    battle_format=generation,
    team=custom_builder,
    max_concurrent_battles=100)

custom_player = CustomPlayer(
    battle_format=generation,
    team=custom_builder,
    max_concurrent_battles=100)

random_player = RandomPlayer(
    battle_format=generation,
    team=custom_builder,
    max_concurrent_battles=100)

random_player2 = RandomPlayer(
    battle_format=generation,
    team=custom_builder,
    max_concurrent_battles=100)

async def time_n_battles(n):
    start_time = time.time()
    await custom_player.battle_against(random_player, n_battles=n)
    return time.time() - start_time

async def plot_battle_times():
    times = []

    x = range(1, 100, 5)

    for i in x:
        times.append(time_n_battles(i))
    
    # Plot the times


async def run_battle():
    start_time = time.time()
    await optimized_player.battle_against(custom_player, n_battles=1)
    print("--- %s seconds ---" % (time.time() - start_time))

    print(f"Battles played: {optimized_player.n_finished_battles}")
    print(f"Battles won: {optimized_player.n_won_battles}")
    print(f"Win rate: {optimized_player.win_rate}")

import cProfile, pstats
import asyncio

async def main():
    profiler = cProfile.Profile()
    profiler.enable()
    await run_battle()
    profiler.disable()

    stats = pstats.Stats(profiler)
    # stats = stats.strip_dirs()  # Remove the path from filenames
    stats.sort_stats('cumulative')  # Sort by cumulative time

    # Print the stats to a file
    with open('results/profile_output.txt', 'w') as f:
        stats.stream = f
        stats.print_stats()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
