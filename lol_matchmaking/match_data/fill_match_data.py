import random
import time
from cassiopeia import set_riot_api_key
from sortedcontainers import SortedList
from lol_matchmaking.match_data.params import riot_params, starting_match_ids
from cassiopeia.core import Match
from lol_matchmaking.match_data.match_stats import features
import csv


def first_line():
    attributes = ['rank', 'winrate', 'mean_kda', 'mean_gpm', 'mean_cs', 'autofill']
    first_line = 'match_id'
    for attribute in attributes:
        for i in range(1, 11):
            player_attribute = f'{attribute}_player_{i},'
            first_line += player_attribute
    first_line += 'win'
    return first_line


def add_match(match):
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids = features(match, SortedList([match.id]))
    with open('saved_data/match_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([match.id] + ranks + winrates + mean_kdas + mean_gpms + mean_css + autofills + [win]) 
        file.close()


def add_matches(match, nb_of_games):
    match_ids = SortedList([match.id])
    start = time.time()
    for i in range(nb_of_games):
        before = time.time()
        match_id = random.choice(match_ids)
        match = Match(id=match_id, region="EUW")
        ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids = features(match, match_ids)
        row = [match_id] + ranks + winrates + mean_kdas + mean_gpms + mean_css + autofills + [win]
        match_ids.remove(match_id)
        with open('saved_data/match_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row) 
            file.close()
        after = time.time()
        print("This match has taken :")
        print(after - before)
        print("From the start :")
        print(after - start)
        print(str(i+1) + " matches saved")


if __name__ == "__main__":
    columns = first_line()
    set_riot_api_key(riot_params()[0])
    match = Match(id=starting_match_ids()[8], region="EUW")
    #add_match(match)
    add_matches(match, 10)
