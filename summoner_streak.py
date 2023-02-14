import pickle
import pandas as pd
import numpy as np
from cassiopeia import set_riot_api_key, Patch
from cassiopeia.core import Summoner
from sortedcontainers import SortedList
from match_stats import features
from params import riot_params
from summoner_stats import get_summoner_match_history

def history_outcomes(summoner, start, end):
    df = pd.DataFrame()
    match_history = get_summoner_match_history(summoner, start, end)
    for match in match_history:
        ranks, winrates, mean_kdas, mean_gpms, mean_css, autofills, win, match_ids = features(match, SortedList([match.id]))
        avg_rank_blue_team = np.mean(ranks[0:5])
        avg_rank_red_team = np.mean(ranks[5:10])
        avg_winrate_blue_team = np.mean(winrates[0:5])
        avg_winrate_red_team = np.mean(winrates[5:10])
        avg_kda_blue_team = np.mean(mean_kdas[0:5])
        avg_kda_red_team = np.mean(mean_kdas[5:10])
        avg_gpm_blue_team = np.mean(mean_gpms[0:5])
        avg_gpm_red_team = np.mean(mean_gpms[5:10])
        avg_cs_blue_team = np.mean(mean_css[0:5])
        avg_cs_red_team = np.mean(mean_css[5:10])
        autofill_blue_team = sum(autofills[0:5])
        autofill_red_team = sum(autofills[5:10])
        new_row = {"avg_rank_blue_team" : avg_rank_blue_team, 
            "avg_rank_red_team" : avg_rank_red_team,
            "avg_winrate_blue_team" : avg_winrate_blue_team,
            "avg_winrate_red_team" : avg_winrate_red_team,
            "avg_kda_blue_team" : avg_kda_blue_team,
            "avg_kda_red_team" : avg_kda_red_team, 
            "avg_gpm_blue_team" : avg_gpm_blue_team,
            "avg_gpm_red_team" : avg_gpm_red_team,
            "avg_cs_blue_team" : avg_cs_blue_team,
            "avg_cs_red_team" : avg_cs_red_team,
            "autofill_blue_team" : autofill_blue_team,
            "autofill_red_team" : autofill_red_team}
        df = df.append(new_row, ignore_index=True)  
    return df

def predicted_outcome(df):
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model.predict_proba(df)


if __name__=="__main__":
    set_riot_api_key(riot_params()[0])
    summoner_name = "Garenoir"
    region = "EUW"
    summoner = Summoner(name=summoner_name, region=region)
    patch = Patch.from_str("13.1", region=region)
    start = patch.start
    end = patch.end
    df = history_outcomes(summoner, start, end)
    a = predicted_outcome(df)
    print(a)