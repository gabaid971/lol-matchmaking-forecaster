from cassiopeia.core import Summoner, Match, MatchHistory, LeagueSummonerEntries, LeagueEntries
from cassiopeia import set_riot_api_key, Patch
from numpy import False_
from params import riot_params
from summoner_stats import get_summoner_historical_features, get_summoner_winrate, get_summoner_rank, get_summoner_match_history
import csv

from utils import team_position_frequency

def score(match):
    """
        for blue team
    """
    score = 0
    for participant in match.participants:
        #is autofill ?
        #winrate
        #winrate on session
        #elo
        print(0)
    return score


def is_participant_autofill(position, team_position_frequency):
    if position not in team_position_frequency.keys():
        return True
    else:
        if team_position_frequency[position] > 0.2:
            return False
        else:
            return True
    


def features(match):
     #patch = Patch.from_str("13.1", region="EUW")
    start = match.patch.start
    end = match.start
    ranks = []
    winrates = []
    mean_kdas = []
    mean_gpms = []
    mean_css = []
    autofills = []
    win = []
    for participant in match.participants:
        summoner = participant.summoner
        ranks.append(get_summoner_rank(summoner))
        winrates.append(get_summoner_winrate(summoner))
        #match_history = get_summoner_match_history(summoner, patch)
        mean_kda, mean_gpm, mean_cs, team_position_frequency = get_summoner_historical_features(summoner, start, end, 6)
        mean_kdas.append(mean_kda)
        mean_gpms.append(mean_gpm)
        mean_css.append(mean_cs)
        autofills.append(is_participant_autofill(participant.team_position.name, team_position_frequency))
        win.append(participant.team.win)
        print(0)
    return ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win


def add_match(match):
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win = features(match)
    with open('match_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ranks) 
        file.close()


if __name__ == "__main__":
    set_riot_api_key(riot_params())
    match = Match(id=6268365373, region="EUW")
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win = features(match)
    print(0)