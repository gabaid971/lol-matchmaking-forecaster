import random
from sortedcontainers import SortedList
import arrow

from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch, set_riot_api_key


def filter_match_history(summoner, patch):
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

    
def collect_matches(initial_summoner_name, region, nb_of_games):
    summoner = Summoner(name=initial_summoner_name, region=region)
    patch = Patch.from_str("12.22", region=region)

    unpulled_summoner_ids = SortedList([summoner.id])
    pulled_summoner_ids = SortedList()

    unpulled_match_ids = SortedList()
    pulled_match_ids = SortedList()

    while unpulled_summoner_ids and len(pulled_match_ids) < nb_of_games:
        # Get a random summoner from our list of unpulled summoners and pull their match history
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region)
        matches = filter_match_history(summoner=new_summoner, patch=patch)
        unpulled_match_ids.update([match.id for match in matches])
        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.add(new_summoner_id)
        count = 0
        while unpulled_match_ids and count < 10:
            # Get a random match from our list of matches
            new_match_id = random.choice(unpulled_match_ids)
            new_match = Match(id=new_match_id, region=region)
            for participant in new_match.participants:
                if (
                    participant.summoner.id not in pulled_summoner_ids
                    and participant.summoner.id not in unpulled_summoner_ids
                ):
                    unpulled_summoner_ids.add(participant.summoner.id)
            # The above lines will trigger the match to load its data by iterating over all the participants.
            # If you have a database in your datapipeline, the match will automatically be stored in it.
            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.add(new_match_id)
            count += 1
    return pulled_match_ids


if __name__ == "__main__":
    set_riot_api_key("RGAPI-6a92f2a7-9ffc-41c8-a2e6-da45a1d1d8f8")
    match_ids = collect_matches("Ckronikkss", "EUW", 30)
    print(len(match_ids))