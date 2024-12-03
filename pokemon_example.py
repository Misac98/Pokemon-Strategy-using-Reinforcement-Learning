import time
import cProfile, pstats
import asyncio
from poke_env import RandomPlayer
from custom_players import OptimizedPlayer, PowerPlayer
from custom_teambuilders import RandomTeamFromPool, StaticTeamFromPool, read_teams_from_file

teams = read_teams_from_file("pokémonTeams/teams1")
custom_builder = RandomTeamFromPool(teams)

generation = "gen2ou"

optimized_player = OptimizedPlayer(
    battle_format=generation,
    team=custom_builder)

custom_player = PowerPlayer(
    battle_format=generation,
    team=custom_builder)

random_player = RandomPlayer(
    battle_format=generation,
    team=custom_builder)

random_player2 = RandomPlayer(
    battle_format=generation,
    team=custom_builder)


async def run_battle():
    start_time = time.time()
    await optimized_player.battle_against(custom_player, n_battles=10)
    print("--- %s seconds ---" % (time.time() - start_time))

    print(f"Battles played: {optimized_player.n_finished_battles}")
    print(f"Battles won: {optimized_player.n_won_battles}")
    print(f"Win rate: {optimized_player.win_rate}")

async def main():
    profiler = cProfile.Profile()
    profiler.enable()
    await run_battle()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')

    # Print the stats to a file
    with open('results/profile_output.txt', 'w') as f:
        stats.stream = f
        stats.print_stats()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
