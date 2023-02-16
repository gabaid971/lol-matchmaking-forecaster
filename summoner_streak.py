import pickle
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from cassiopeia import set_riot_api_key, Patch
from cassiopeia.core import Summoner
from match_stats import winning_team
from params import riot_params
from summoner_stats import get_summoner_match_history, get_summoner_rank, get_summoner_winrate


def features_low(match, summoner):
    sides = {"blue": 1, "red": -1}
    ranks = []
    winrates = []
    win = winning_team(match)
    summoner_team = sides[match.participants[summoner].side.name]
    for participant in match.participants:
        summoner = participant.summoner
        ranks.append(get_summoner_rank(summoner))
        winrates.append(get_summoner_winrate(summoner))
    return ranks, winrates, win, summoner_team


def history_outcomes(summoner, start, end):
    df = pd.DataFrame()
    match_history = get_summoner_match_history(summoner, start, end)
    for match in match_history:
        ranks, winrates, win, summoner_team = features_low(match, summoner)
        avg_rank_blue_team = np.mean(ranks[0:5])
        avg_rank_red_team = np.mean(ranks[5:10])
        avg_winrate_blue_team = np.mean(winrates[0:5])
        avg_winrate_red_team = np.mean(winrates[5:10])
        new_row = {
            "match_id" : match.id,
            "date" : match.start,
            "duration" : match.duration,
            "avg_rank_blue_team" : avg_rank_blue_team, 
            "avg_rank_red_team" : avg_rank_red_team,
            "avg_winrate_blue_team" : avg_winrate_blue_team,
            "avg_winrate_red_team" : avg_winrate_red_team,
            "win" : win,
            "summoner_team" : summoner_team
        }
        df = df.append(new_row, ignore_index=True)  
    return df


def predicted_outcome(df):
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    predicted_win = loaded_model.predict_proba(df[["avg_rank_blue_team", "avg_rank_red_team", "avg_winrate_blue_team", "avg_winrate_red_team"]])
    df["predicted_win"] = [proba[1] - proba[0] for proba in predicted_win]
    df["summoner_win"] = df["summoner_team"]*df["win"]
    df["summoner_predicted_win"] = df["summoner_team"]*df["predicted_win"]
    return df


def win_history(summoner_name, patch_name):
    set_riot_api_key(riot_params()[0])
    region = "EUW"
    summoner = Summoner(name=summoner_name, region=region)
    patch = Patch.from_str(patch_name, region=region)
    start = patch.start
    end = patch.end
    df = history_outcomes(summoner, start, end)
    return predicted_outcome(df)


if __name__=="__main__":
    summoner_name = "Garenoir"
    patch_name = "13.1"
    df = win_history(summoner_name, patch_name)