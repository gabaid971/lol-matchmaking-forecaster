from cassiopeia import set_riot_api_key
from numpy import NaN
from sortedcontainers import SortedList
from lol_matchmaking.match_data.params import riot_params
from cassiopeia.core import Match
from lol_matchmaking.match_data.summoner_stats import get_summoner_historical_features, get_summoner_winrate, get_summoner_rank


def is_participant_autofill(position, team_position_frequency):
    if team_position_frequency is NaN:
        return NaN
    else:
        if position not in team_position_frequency.keys():
            return True
        else:
            if team_position_frequency[position] > 0.2:
                return False
            else:
                return True
    

def winning_team(match):
    """
        returns 1 if the blue team wins
        -1 if the red team wins
    """
    return -1 + 2*int(match.participants[0].team.win)


def features(match, match_ids):
    start = match.patch.start
    end = match.start
    ranks = []
    winrates = []
    mean_kdas = []
    mean_gpms = []
    mean_css = []
    autofills = []
    win = winning_team(match)
    for participant in match.participants:
        summoner = participant.summoner
        ranks.append(get_summoner_rank(summoner))
        winrates.append(get_summoner_winrate(summoner))
        mean_kda, mean_gpm, mean_cs, team_position_frequency, match_ids = get_summoner_historical_features(summoner, start, end, match_ids, 5)
        mean_kdas.append(mean_kda)
        mean_gpms.append(mean_gpm)
        mean_css.append(mean_cs)
        autofills.append(is_participant_autofill(participant.team_position.name, team_position_frequency))
    return ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids


if __name__ == "__main__":
    set_riot_api_key(riot_params()[0])
    match = Match(id=6268365373, region="EUW")
    ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids = features(match, SortedList([match.id]))