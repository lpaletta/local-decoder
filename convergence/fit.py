import numpy as np
from scipy.stats import linregress

def get_cutoff(df):
    TIME_MIN_FIT = 180
    for distance, group in df.groupby("n"):
        logical_error_mean = (group.loc[group["T"] >= TIME_MIN_FIT, "pL"]).mean()
        cond = (group["pL"]) >= (1 * logical_error_mean / 2)

        # Ensure ordered by time
        group_sorted = group.sort_values("T")

        # True only if condition holds for this row AND all later rows
        steady_from_here = cond.iloc[::-1].cummin().iloc[::-1]

        time_cutoff = group_sorted.loc[steady_from_here, "T"].min()

        df.loc[df["n"] == distance, "logical_error_mean"] = logical_error_mean
        df.loc[df["n"] == distance, "time_cutoff"] = time_cutoff

def fit_cutoff(df):
    df_fit = df[df["T"] == df["T"].max()]
    X = df_fit["n"].to_numpy()
    Y = df_fit["time_cutoff"].to_numpy()
    slope, intercept, *_ = linregress(X, Y)
    df["time_cutoff_fit"] = slope * df["n"] + intercept