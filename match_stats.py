from cassiopeia.core import Summoner, Match, MatchHistory, LeagueSummonerEntries, LeagueEntries
from cassiopeia import set_riot_api_key, Patch


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


if __name__ == "__main__":
    set_riot_api_key("RGAPI-1078aab9-7d07-4ab4-ac8a-6fc5ddb5a6fc")
    match = Match(id=6229757149, region="EUW")
    

    print(0)