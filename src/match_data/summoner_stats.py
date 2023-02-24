import sys
sys.path.insert(0, '')
import datetime
from cassiopeia import set_riot_api_key, Patch, Queue
from numpy import NaN
from sortedcontainers import SortedList
from src.match_data.params import riot_params
from cassiopeia.core import Summoner, MatchHistory
from src.utils import RomanNumeralToDecimal, team_position_frequency
import arrow


def get_summoner_winrate(summoner):
    if Queue.ranked_solo_fives in summoner.ranks.keys():
        league = next(x for x in summoner.league_entries if x.queue == Queue.ranked_solo_fives)
        wins, losses = league.wins, league.losses
        winrate = 0.5 if (wins + losses)==0 else wins / (wins + losses)
        return winrate
    else:
        return 0.5


def get_summoner_rank(summoner):
    if Queue.ranked_solo_fives in summoner.ranks.keys():
        league = summoner.ranks[Queue.ranked_solo_fives]
        tier_conversion = {'IRON':0, 'BRONZE':4, 'SILVER':8, 'GOLD':12, 'PLATINUM':16, \
            'DIAMOND':20, 'MASTER':21, 'GRANDMASTER':22, 'CHALLENGER':23}
        tier, division = tier_conversion[league.tier.value], RomanNumeralToDecimal(league.division.value)
        return tier + (4 - division)
    else:
        return 11


def get_summoner_match_history(summoner, start, end):
    match_history = MatchHistory(
        puuid=summoner.puuid,
        continent="EUROPE",
        start_time=start,
        end_time=end,
        queue="RANKED_SOLO_5x5",    
    )
    return match_history


def get_summoner_historical_features(summoner, start, end, match_ids, max_matches=None):
    match_history = get_summoner_match_history(summoner, start, end)
    total_matches = len(match_history) if max_matches is None else min(len(match_history), max_matches)
    if total_matches != 0:
        total_kills = 0
        total_deaths = 0
        total_assists = 0
        total_gold = 0
        total_time = 0
        total_cs = 0
        team_positions = []
        count = 0
        for match in match_history:
            if (max_matches is None) or (count < total_matches):
                if match.duration > datetime.timedelta(seconds=500):
                    match_ids.add(match.id)
                    participant = match.participants[summoner]
                    total_kills += participant.stats.kills
                    total_deaths += participant.stats.deaths
                    total_assists += participant.stats.assists
                    total_gold += participant.stats.gold_earned
                    total_time += participant.stats.time_played
                    total_cs += participant.stats.total_minions_killed
                    team_positions.append(participant.team_position.name)
                    count += 1
                else:
                    total_matches -= 1
        if total_deaths == 0:
            mean_kda = (total_kills + total_assists)
        else:
            mean_kda = (total_kills + total_assists) / total_deaths
        mean_gpm = total_gold / (total_time / 60)
        mean_cs = total_cs / total_matches
        team_position_frequencies = team_position_frequency(team_positions, max_matches)
        return mean_kda, mean_gpm, mean_cs, team_position_frequencies, match_ids
    else:
        return NaN, NaN, NaN, NaN, match_ids


if __name__ == "__main__":
    set_riot_api_key(riot_params()[0])
    summoner_name = "Garenoir"
    region = "EUW"
    patch = Patch.from_str("13.1", region=region)
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()
    start_time = patch.start
    summoner = Summoner(name=summoner_name, region=region)
    rank = get_summoner_rank(summoner)
    winrate = get_summoner_winrate(summoner)
    match_history = get_summoner_match_history(summoner, start_time, end_time)
    mean_kda, mean_gpm, mean_cs, team_position_frequencies, match_ids = get_summoner_historical_features(summoner, start_time, end_time, SortedList([]), 5)