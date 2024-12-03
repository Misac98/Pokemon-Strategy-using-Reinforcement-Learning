from poke_env.player.player import Player
from poke_env.environment.abstract_battle import AbstractBattle
import requests
import re


class PowerPlayer(Player):
    def choose_move(self, battle: AbstractBattle):
        if battle.available_moves:
            return self.create_order(max(battle.available_moves, key=lambda move: move.base_power*move.accuracy))
        else:
            return self.choose_random_move(battle)



class OptimizedPlayer(Player):                
    def choose_move(self, battle: AbstractBattle):
        if battle.available_moves:
            attacker = battle.active_pokemon
            defender = battle.opponent_active_pokemon
            gen_number = re.search(r'\d+', self._format).group()
            
            params = {
                'generation': gen_number,
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

