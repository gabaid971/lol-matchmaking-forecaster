from cassiopeia.core import Summoner, MatchHistory, LeagueSummonerEntries, LeagueEntries
from cassiopeia import set_riot_api_key, Patch
from params import riot_params
from utils import RomanNumeralToDecimal, team_position_frequency
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


def get_summoner_historical_features(summoner, patch, max_matches=None):
    match_history = get_summoner_match_history(summoner, patch)
    total_matches = len(match_history) if max_matches is None else min(len(match_history), max_matches)
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_gold = 0
    total_time = 0
    total_cs = 0
    #total_damages = 0
    team_positions = []
    count = 0
    for match in match_history:
        if (max_matches is None) or (count < max_matches):
            participant = match.participants[summoner]
            total_kills += participant.stats.kills
            total_deaths += participant.stats.deaths
            total_assists += participant.stats.assists
            total_gold += participant.stats.gold_earned
            total_time += participant.stats.time_played
            total_cs += participant.stats.total_minions_killed
            #total_damages += participant.stats.total_damage_dealt
            team_positions.append(participant.team_position.name)
            count += 1
    if total_deaths == 0:
        mean_kda = (total_kills + total_assists)
    else:
        mean_kda = (total_kills + total_assists) / total_deaths
    mean_gpm = total_gold / (total_time / 60)
    mean_cs = total_cs / total_matches
    #mean_damages = total_damages / total_damages
    team_position_frequencies = team_position_frequency(team_positions, max_matches)
    return mean_kda, mean_gpm, mean_cs, team_position_frequencies


if __name__ == "__main__":
    set_riot_api_key(riot_params())
    summoner_name = "Garenoir"
    region = "EUW"
    patch = Patch.from_str("13.1", region=region)
    summoner = Summoner(name=summoner_name, region=region)
    rank = get_summoner_rank(summoner)
    winrate = get_summoner_winrate(summoner)
    match_history = get_summoner_match_history(summoner, patch)
    mean_kda, mean_gpm, mean_cs = get_summoner_historical_features(summoner, patch)
    print(0)