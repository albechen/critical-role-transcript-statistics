import pandas as pd
import numpy as np
import scipy.stats as sci
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


def sum_sq_and_dof_factors(df, target_col, column):
    ss = 0
    grand_mean = np.mean(df[target_col])
    dof = len(list(df[column].unique())) - 1
    for item in list(df[column].unique()):
        item_set = df[df[column] == item]
        item_mean = np.mean(item_set[target_col])
        ss += (item_mean - grand_mean) ** 2 * len(item_set)
    return [column, ss, dof]


def sum_sq_and_dof_within(df, target_col, col1, col2):
    ss = 0
    dof = 0
    for item1 in list(df[col1].unique()):
        for item2 in list(df[col2].unique()):
            item_set = df[(df[col1] == item1) & (df[col2] == item2)]
            item_mean = np.mean(item_set[target_col])
            dof += len(item_set) - 1
            for item in item_set[target_col]:
                ss += (item - item_mean) ** 2
    return ["within", ss, dof]


def sum_of_squares_total(df, target_col):
    ss = 0
    grand_mean = np.mean(df[target_col])
    for item in df[target_col]:
        ss += (item - grand_mean) ** 2
    return ss


def z_test(df, target_col, item_col, item1, item2):
    df1 = df[df[item_col] == item1]
    df2 = df[df[item_col] == item2]

    mean1 = np.mean(df1[target_col])
    mean2 = np.mean(df2[target_col])
    std1 = np.std(df1[target_col])
    std2 = np.std(df2[target_col])
    n1 = len(df1[item_col])
    n2 = len(df2[item_col])

    z_score = abs((mean1 - mean2 - 0) / np.sqrt(std1 ** 2 / n1 + std2 ** 2 / n2))
    crit_z = sci.norm.ppf(0.975)
    p_score = 2 * (1 - sci.norm.cdf(abs(z_score)))

    return [item1, item2, z_score, crit_z, p_score]


def z_test_array(df, target_col, item_col):
    z_list = []
    for item1 in list(df[item_col].unique()):
        for item2 in list(df[item_col].unique()):
            item_set = z_test(df, target_col, item_col, item1, item2)
            z_list.append(item_set)
    z_df = pd.DataFrame(
        z_list, columns=["item1", "item2", "z_score", "crit_z", "p_score"]
    )
    return z_df


def sort_items_by_mean(df, target_col, item_col):
    mean_list = []
    for item in list(df[item_col].unique()):
        item_df = df[df[item_col] == item]
        mean_item = np.mean(item_df[target_col])
        item_list = [item, mean_item]
        mean_list.append(item_list)
    mean_df = pd.DataFrame(mean_list, columns=["item", "mean"])
    mean_df = mean_df.sort_values(by=["mean"])
    return mean_df


def wide_p_score_df(full_person_ep, campaign_num_or_all):
    if campaign_num_or_all == "all":
        C_person_ep = full_person_ep.copy()
        C_person_ep["person"] = (
            "C"
            + full_person_ep["campaign"].astype(str)
            + " "
            + full_person_ep["person"]
        )
    else:
        C_person_ep = full_person_ep[full_person_ep["campaign"] == campaign_num_or_all]
    long_z_df = z_test_array(C_person_ep, "time_count", "person")
    wide_p_df = long_z_df.pivot(index="item1", columns="item2", values="p_score")

    mean_person = sort_items_by_mean(C_person_ep, "time_count", "person")
    mean_order = list(mean_person["item"])
    wide_p_df = wide_p_df.reindex(columns=mean_order, index=mean_order)

    return wide_p_df


def NonLinCdict(steps, hexcol_array):
    cdict = {"red": (), "green": (), "blue": ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb = matplotlib.colors.hex2color(hexcol)
        cdict["red"] = cdict["red"] + ((s, rgb[0], rgb[0]),)
        cdict["green"] = cdict["green"] + ((s, rgb[1], rgb[1]),)
        cdict["blue"] = cdict["blue"] + ((s, rgb[2], rgb[2]),)
    return cdict


def heatplot_p_scores(full_person_ep, campaign_num_or_all):
    wide_p_df = wide_p_score_df(full_person_ep, campaign_num_or_all)

    hc = ["#FFD4D4", "#FFA9A9", "#FF5B5B", "#FF3F3F"]
    th = [0, 0, 0.05, 1]

    cdict = NonLinCdict(th, hc)
    cm = matplotlib.colors.LinearSegmentedColormap("test", cdict)

    if campaign_num_or_all == "all":
        fig_dim = (8, 8)
    else:
        fig_dim = (5, 5)
    fig, ax = plt.subplots(figsize=fig_dim)

    sns.heatmap(
        wide_p_df,
        annot=True,
        vmin=0.0,
        vmax=1,
        cmap=cm,
        linewidths=0.5,
        cbar=False,
        fmt=".2f",
        ax=ax,
    )
    ax.title.set_text(
        "C(%s): p-score per Cast Members and Season" % campaign_num_or_all
    )

    plt.show()
