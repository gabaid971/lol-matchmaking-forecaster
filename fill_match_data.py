from cassiopeia import set_riot_api_key
from params import riot_params
from cassiopeia.core import Match
from match_stats import features
import csv


def first_line():
    first_line = ''
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
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win = features(match)
    with open('match_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ranks + winrates + mean_kdas + mean_gpms + mean_css + autofills + [win]) 
        file.close()


if __name__ == "__main__":
    columns = first_line()
    set_riot_api_key(riot_params())
    match = Match(id=6268365373, region="EUW")
    add_match(match)
    print(0)