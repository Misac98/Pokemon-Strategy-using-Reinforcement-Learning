# Pokemon-Strategy-using-Reinforcement-Learning

This project aims to develop a strategy for Pokémon battles using reinforcement learning. It includes team builders, player implementations, and a damage calculator.

## Table of Contents
- [Environment Usage](#environment-usage)
  - [Team Builder](#team-builder)
  - [Player Implementations](#player-implementations)
  - [Battle Simulation](#battle-simulation)
- [Damage Calculator](#damage-calculator)
  - [Input Values](#input-values)
  - [Output](#output)
  - [Server Details](#server-details)
  - [Querying the Server](#querying-the-server)
  - [Example Response](#example-response)
- [Initial Setup](#initial-setup)

## Environment Usage

### Team Builder
Two different team builders are implemented in the `custom_teambuilders.py` file. The `StaticTeamFromPool` class always returns the first team from a pool of teams, while the `RandomTeamFromPool` class returns a random team from the pool. The teams are read from the `pokémonTeams` folder, where each file contains a team in the Showdown format. This can be done by using the `read_teams_from_files` function from the `custom_teambuilders.py` file.

As an example, the following code reads the teams from the `pokémonTeams` folder and creates a `RandomTeamFromPool` object that will return a random team from the pool:

```python
teams = read_teams_from_file("pokémonTeams")
custom_team = RandomTeamFromPool(teams)
```

### Player implementations

The `poke_env` environment already provides a basic `RandomPlayer` class that chooses a random move from the available moves. Additionally, we have implemented two different player implementations, which are defined in the `custom_players.py` file.
 - The `PowerPlayer` class is a player that always chooses the move with the highest base power and accuracy. If there are no available moves, it chooses a random move.
 - The `OptimizedPlayer` class is a player that uses the damage calculator to calculate the average damage that each move will do to the opponent Pokémon. It then chooses the move that will do the most damage. If there are no available moves, it chooses a random move.

As an example, the following code creates a `PowerPlayer` object, with the `RandomTeamFromPool` object created in the previous example:

```python
custom_player = PowerPlayer(battle_format="gen2ou", team=custom_team)
```

### Battle simulation

The battle simulation is done using the `poke_env` environment. Once the players are defined, the battle can be started using the `battle_against` method. This method receives the opponent player and the number of battles to be played. The following code shows how to run a battle between the `custom_player` and the `optimized_player`:

```python
await optimized_player.battle_against(custom_player, n_battles=1)
```

This code will run a single battle between the two players. After the battle is finished, the players have information about the battles:

```python
print(f"Battles played: {optimized_player.n_finished_battles}")
print(f"Battles won: {optimized_player.n_won_battles}")
print(f"Win rate: {optimized_player.win_rate}")
```

## Damage Calculator

The damage calculator allows the user to calculate the damage that a move will do to a Pokémon. 

#### Input Values
The input values are the following:
- Generation
- Attacker Name
- Attacker Level
- Attacker Item
- Attacker Status
- Attacker Ability
- Attacker Boosts
- Defender Name
- Defender Level
- Defender Item
- Defender Status
- Defender Ability
- Defender Boosts
- Move Name

#### Output
The output is an array of the possible damage values that the move can do to the defender Pokémon, or 0 if the move would not affect the defender Pokémon. In our implementation, the effective damage is calculated as the average of the possible damage values, but other data could be extracted as well, such as the minimum or maximum damage values, or maybe use those values to calculate the probability of the move knocking out the defender Pokémon.

#### Server Details
This damage calculator runs in a `node.js` server to increase the speed of the calculations (Otherwise a new process would have to be instantiated for each calculation). The server also supports basic caching to avoid recalculating the same values multiple times, so the speed should increase slightly as the simulation progresses. The server is hosted on `localhost:{port}`, where the port is defined in the `config.json` file.

#### Querying the Server
To query the server, a 'GET' request should be made to the `/calculate-damage` endpoint, with the query parameters defined in the `damage_calculator_server.js` file. The query parameters should be encoded in the URL, and the response will be a JSON object with the calculated damage values. 

An example of a query is the following:

```http
GET http://localhost:3000/calculate-damage?generation=2&attackerName=snorlax&attackerLevel=100&attackerItem=leftovers&attackerStatus=None&attackerAbility=noability&attackerBoosts=%7B%27accuracy%27%3A+0%2C+%27atk%27%3A+0%2C+%27def%27%3A+0%2C+%27evasion%27%3A+0%2C+%27spa%27%3A+0%2C+%27spd%27%3A+0%2C+%27spe%27%3A+0%7D&defenderName=snorlax&defenderLevel=100&defenderItem=unknown_item&defenderStatus=None&defenderAbility=None&defenderBoosts=%7B%27accuracy%27%3A+0%2C+%27atk%27%3A+0%2C+%27def%27%3A+0%2C+%27evasion%27%3A+0%2C+%27spa%27%3A+0%2C+%27spd%27%3A+0%2C+%27spe%27%3A+0%7D&moveName=protect
``` 

## Initial Setup

0. Pre-requisites:
    - Python 3.6 or higher
    - Node.js 14.0 or higher
    - npm 6.0 or higher
    - pip 20.0 or higher

1. Install the required packages using the following command:
```sh 
pip install -r requirements.txt
```
2. Install the required node modules using the following command:
```sh
npm install 
```
3. Run the following command to start the damage calculator server:
```sh
node damage_calculator_server.js
```

4. Run the following command to start the pokemon showdown server:
```sh
node pokemon-showdown start --no-security
```

## Sample code

All this functionality is demonstrated in the `pokemon_example.py` file. This file reads the teams from the `pokémonTeams` folder, creates a `RandomTeamFromPool` object, and then creates a `PowerPlayer` object. It then runs a battle between the `PowerPlayer` and the `OptimizedPlayer` and prints the results, as well as calculates some profiling information.

```sh
python pokemon_example.py
```