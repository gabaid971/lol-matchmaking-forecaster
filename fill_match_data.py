from cassiopeia import set_riot_api_key
from params import riot_params
from cassiopeia.core import Match
from match_stats import features
import csv


def add_match(match):
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win = features(match)
    with open('match_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ranks) 
        file.close()


if __name__ == "__main__":
    set_riot_api_key(riot_params())
    match = Match(id=6268365373, region="EUW")
    add_match(match)