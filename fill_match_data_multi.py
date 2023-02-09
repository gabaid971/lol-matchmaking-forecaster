import random
import time
from cassiopeia import set_riot_api_key
from sortedcontainers import SortedList
from params import riot_params, starting_match_ids
from cassiopeia.core import Match
from match_stats import features
import requests
import threading
import csv


def first_line():
    first_line = 'match_id'
    for i in range(1, 11):
        rank = 'rank_player_' + str(i) + ','
        first_line += rank
    for i in range(1, 11):
        winrate = 'winrate_player_' + str(i) + ','
        first_line += winrate
    for i in range(1, 11):
        mean_kda = 'mean_kda_player_' + str(i) + ','
        first_line += mean_kda
    for i in range(1, 11):
        mean_gpm = 'mean_gpm_player_' + str(i) + ','
        first_line += mean_gpm
    for i in range(1, 11):
        mean_cs = 'mean_cs_player_' + str(i) + ','
        first_line += mean_cs    
    for i in range(1, 11):
        autofill = 'autofill_player_' + str(i) + ','
        first_line += autofill
    first_line += 'win'
    return first_line


def add_match(match):
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids = features(match, SortedList([match.id]))
    with open('match_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([match.id] + ranks + winrates + mean_kdas + mean_gpms + mean_css + autofills + [win]) 
        file.close()


def add_matches(api_key, match_id, nb_of_games):
    set_riot_api_key(api_key)
    match = Match(id=match_id, region="EUW")
    match_ids = SortedList([match.id])
    start = time.time()
    for i in range(nb_of_games):
        before = time.time()
        match_id = random.choice(match_ids)
        match = Match(id=match_id, region="EUW")
        ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids = features(match, match_ids)
        row = [match_id] + ranks + winrates + mean_kdas + mean_gpms + mean_css + autofills + [win]
        match_ids.remove(match_id)
        with open('match_data.csv', 'a', newline='') as file:
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
    thread1 = threading.Thread(target=add_matches, args=(riot_params()[0], starting_match_ids()[0], 10))
    thread2 = threading.Thread(target=add_matches, args=(riot_params()[1], starting_match_ids()[1], 10))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
