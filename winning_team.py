import pandas as pd
import lazypredict
from lazypredict.Supervised import LazyClassifier, LazyRegressor
from sklearn.model_selection import train_test_split


def team_features(df):
    df["avg_rank_team_1"] = df[["rank_player_1", "rank_player_2", "rank_player_3", "rank_player_4", "rank_player_5"]].mean(axis=1)
    df["avg_rank_team_2"] = df[["rank_player_6", "rank_player_7", "rank_player_8", "rank_player_9", "rank_player_10"]].mean(axis=1)
    df["avg_winrate_team_1"] = df[["winrate_player_1", "winrate_player_2", "winrate_player_3", "winrate_player_4", "winrate_player_5"]].mean(axis=1)
    df["avg_winrate_team_2"] = df[["winrate_player_6", "winrate_player_7", "winrate_player_8", "winrate_player_9", "winrate_player_10"]].mean(axis=1)
    df["avg_kda_team_1"] = df[["mean_kda_player_1", "mean_kda_player_2", "mean_kda_player_3", "mean_kda_player_4", "mean_kda_player_5"]].mean(axis=1)
    df["avg_kda_team_2"] = df[["mean_kda_player_6", "mean_kda_player_7", "mean_kda_player_8", "mean_kda_player_9", "mean_kda_player_10"]].mean(axis=1)
    df["avg_gpm_team_1"] = df[["mean_gpm_player_1", "mean_gpm_player_2", "mean_gpm_player_3", "mean_gpm_player_4", "mean_gpm_player_5"]].mean(axis=1)
    df["avg_gpm_team_2"] = df[["mean_gpm_player_6", "mean_gpm_player_7", "mean_gpm_player_8", "mean_gpm_player_9", "mean_gpm_player_10"]].mean(axis=1)
    df["avg_cs_team_1"] = df[["mean_cs_player_1", "mean_cs_player_2", "mean_cs_player_3", "mean_cs_player_4", "mean_cs_player_5"]].mean(axis=1)
    df["avg_cs_team_2"] = df[["mean_cs_player_6", "mean_cs_player_7", "mean_cs_player_8", "mean_cs_player_9", "mean_cs_player_10"]].mean(axis=1)
    df["nb_autofill_team_1"] = df[["autofill_player_1", "autofill_player_2", "autofill_player_3", "autofill_player_4", "autofill_player_5"]].sum(axis=1)
    df["nb_autofill_team_2"] = df[["autofill_player_6", "autofill_player_7", "autofill_player_8", "autofill_player_9", "autofill_player_10"]].sum(axis=1)
    return df


def train_models(df):
    X = df[["avg_rank_team_1", "avg_rank_team_2", "avg_winrate_team_1",
        "avg_winrate_team_2", "avg_kda_team_1", "avg_kda_team_2",
            "avg_gpm_team_1", "avg_gpm_team_2", "avg_cs_team_1",
                "avg_cs_team_2", "nb_autofill_team_1", "nb_autofill_team_2"]]
    y= df[["win"]]

    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=.5, random_state =123)

    clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
    models, predictions = clf.fit(X_train, X_test, y_train, y_test)
    return models, predictions


if __name__ == "__main__":
    df = pd.read_csv("match_data.csv")
    df = team_features(df)
    models, predictions = train_models(df)
    print(predictions)