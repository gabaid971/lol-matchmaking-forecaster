from cassiopeia.core import Summoner, MatchHistory, LeagueSummonerEntries, LeagueEntries
from cassiopeia import set_riot_api_key, Patch
from utils import RomanNumeralToDecimal
import arrow


def get_summoner_winrate(summoner):
    if len(summoner.league_entries) > 0:
        league = summoner.league_entries[0]
        wins, losses = league.wins, league.losses
        winrate = 0.5 if (wins + losses)==0 else wins / (wins + losses)
        return winrate
    else:
        return 0.5


def get_summoner_rank(summoner):
    if len(summoner.league_entries) > 0:
        league = summoner.league_entries[0]
        tier_conversion = {'IRON':0, 'BRONZE':4, 'SILVER':8, 'GOLD':12, 'PLATINIUM':16, \
            'DIAMOND':20, 'MASTER':21, 'GRANDMASTER':22, 'CHALLENGER':23}
        tier, division = tier_conversion[league.tier.value], RomanNumeralToDecimal(league.division.value)
        return tier + (4 - division)
    else:
        return 0


def get_summoner_match_history(summoner, patch):
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()
    match_history = MatchHistory(
        puuid=summoner.puuid,
        continent="EUROPE",
        start_time=patch.start,
        end_time=end_time,
        queue="RANKED_SOLO_5x5",    
    )
    return match_history

#MatchHistory(continent=self.region.continent, puuid=self.puuid)
if __name__ == "__main__":
    set_riot_api_key("RGAPI-1078aab9-7d07-4ab4-ac8a-6fc5ddb5a6fc")
    summoner_name = "Garenoir"
    region = "EUW"
    patch = Patch.from_str("13.1", region=region)
    summoner = Summoner(name=summoner_name, region=region)
    rank = get_summoner_rank(summoner)
    winrate = get_summoner_winrate(summoner)
    match_history = get_summoner_match_history(summoner, patch)
    print(0)