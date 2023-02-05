from cassiopeia.core import Summoner, Match, MatchHistory, LeagueSummonerEntries, LeagueEntries
from cassiopeia import set_riot_api_key, Patch
from params import riot_params
from summoner_stats import get_summoner_historical_features, get_summoner_winrate, get_summoner_rank, get_summoner_match_history


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


def features(match):
    patch = Patch.from_str("13.1", region="EUW")
    ranks = []
    winrates = []
    mean_kdas = []
    mean_gpms = []
    mean_css = []
    for participant in match.participants:
        summoner = participant.summoner
        ranks.append(get_summoner_rank(summoner))
        winrates.append(get_summoner_winrate(summoner))
        #match_history = get_summoner_match_history(summoner, patch)
        historical_infos = get_summoner_historical_features(summoner, patch, 6)
        mean_kdas.append(historical_infos[0])
        mean_gpms.append(historical_infos[1])
        mean_css.append(historical_infos[2])
        print(0)
    return ranks, winrates, mean_kdas, mean_gpms, mean_css


if __name__ == "__main__":
    set_riot_api_key(riot_params())
    match = Match(id=6229757149, region="EUW")
    ranks, winrates, mean_kdas, mean_gpms, mean_css = features(match)
    print(0)