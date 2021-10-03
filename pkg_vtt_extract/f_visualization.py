import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator

from .e_agg_df_count import group_by_person_episode, count_per_episode


def lineplot_per_ep(org_names, matt_nomatt, C1_C2):
    person_episode_group = group_by_person_episode(org_names)

    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    if matt_nomatt == "nomatt":
        person_episode_group = person_episode_group.loc[
            person_episode_group["person"] != "matt"
        ]

    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 5))
    ax = sns.lineplot(
        x="episode",
        y="time_count",
        data=person_episode_group,
        hue="person",
        marker=".",
        palette=palette,
    )

    if C1_C2 == "C1":
        ax.set(xlim=(1, 115))
    else:
        ax.set(xlim=(1, 128))

    ax.legend(bbox_to_anchor=(1, 1))
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Seconds per Episode")
    ax.title.set_text("%s: Seconds per Episode" % C1_C2)

    path = "images/lineplot_per_ep" + "_" + C1_C2 + "_" + matt_nomatt + ".png"
    plt.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)


def lineplot_cont_count(org_names, matt_nomatt, C1_C2):
    person_episode_group = group_by_person_episode(org_names)
    count_per_ep = count_per_episode(person_episode_group)

    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    if matt_nomatt == "nomatt":
        count_per_ep = count_per_ep.loc[count_per_ep["person"] != "matt"]

    sns.set_style("whitegrid")

    plt.figure(figsize=(7, 5))
    ax = sns.lineplot(
        x="episode",
        y="cont_time_count",
        data=count_per_ep,
        hue="person",
        palette=palette,
    )

    if C1_C2 == "C1":
        ax.set(xlim=(1, 115))
    else:
        ax.set(xlim=(1, 128))

    ax.legend(bbox_to_anchor=(1, 1))
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Total Seconds")
    ax.title.set_text("%s: Total Seconds per Episodes" % C1_C2)

    path = "images/lineplot_cont" + "_" + C1_C2 + "_" + matt_nomatt + ".png"
    plt.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)


def densityplot_time_per_ep2(org_name, C1_C2):
    person_episode_group = group_by_person_episode(org_name)
    names = ["matt", "laura", "sam", "marisha", "travis", "liam", "taliesin", "ashley"]

    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    for name in names:
        color = palette[name]

        if name != "matt":
            ax0 = sns.kdeplot(
                person_episode_group["time_count"][
                    (person_episode_group["person"] == name)
                ],
                legend=False,
                shade=True,
                color=color,
                ax=ax[0],
            )
            ax0.set_xlim(left=0)
            ax0.set_xlabel("Seconds per Episode")
            ax0.title.set_text("%s: Time Spoken Distribution" % C1_C2)

        ax1 = sns.kdeplot(
            person_episode_group["time_count"][
                (person_episode_group["person"] == name)
            ],
            legend=True,
            shade=True,
            color=color,
            ax=ax[1],
        )
        ax1.legend(names)
        ax1.set_xlim(left=0)
        ax1.set_xlabel("Seconds per Episode")
        ax1.title.set_text("%s: Time Spoken Distribution" % C1_C2)

    path = "images/density_time_per_ep" + "_" + C1_C2 + ".png"
    fig.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)


def densityplot_time_per_ep(org_name, matt_nomatt, C1_C2):
    person_episode_group = group_by_person_episode(org_name)
    names = ["matt", "laura", "sam", "marisha", "travis", "liam", "taliesin", "ashley"]

    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    if matt_nomatt == "nomatt":
        person_episode_group = person_episode_group.loc[
            person_episode_group["person"] != "matt"
        ]
        names = ["laura", "sam", "marisha", "travis", "liam", "taliesin", "ashley"]

    plt.figure(figsize=(7, 5))
    for name in names:
        color = palette[name]
        ax = sns.kdeplot(
            person_episode_group["time_count"][
                (person_episode_group["person"] == name)
            ],
            shade=True,
            color=color,
        )
    ax.legend(names)
    ax.set_xlim(left=0)
    ax.set_xlabel("Seconds per Episode")

    ax.title.set_text("%s: Time Spoken Distribution" % C1_C2)

    path = "images/density_time_per_ep" + "_" + C1_C2 + "_" + matt_nomatt + ".png"
    plt.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)


def density_subjectivity2(pol_sub_df, C1_C2):
    names = ["matt", "laura", "sam", "marisha", "travis", "liam", "taliesin", "ashley"]

    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    for name in names:
        color = palette[name]

        ax0 = sns.kdeplot(
            pol_sub_df["Polarity"][(pol_sub_df["person"] == name)],
            legend=False,
            shade=True,
            color=color,
            ax=ax[0],
        )
        ax0.set_xlabel("Polarity")
        ax0.title.set_text("%s: Polarity Distribution" % C1_C2)

        ax1 = sns.kdeplot(
            pol_sub_df["Subjectivity"][(pol_sub_df["person"] == name)],
            legend=True,
            shade=True,
            color=color,
            ax=ax[1],
        )
        ax1.legend(names)
        ax1.set_xlabel("Subjectivity")
        ax1.title.set_text("%s: Subjectivity Distribution" % C1_C2)

    path = "images/density_sentiment" + "_" + C1_C2 + ".png"
    plt.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)


def density_subjectivity(pol_sub_df, C1_C2, Polarity_Subjectivity):
    names = ["matt", "laura", "sam", "marisha", "travis", "liam", "taliesin", "ashley"]

    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    plt.figure(figsize=(7, 5))
    for name in names:
        color = palette[name]
        ax = sns.kdeplot(
            pol_sub_df[Polarity_Subjectivity][(pol_sub_df["person"] == name)],
            shade=True,
            color=color,
        )
    ax.legend(names)
    ax.set_xlabel(Polarity_Subjectivity)

    ax.title.set_text("%s: %s Distribution" % (C1_C2, Polarity_Subjectivity))

    path = (
        "images/density_sentiment" + "_" + C1_C2 + "_" + Polarity_Subjectivity + ".png"
    )
    plt.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)


def lineplot_sentiment(pol_sub_df, C1_C2, Polarity_Subjectivity):
    pol_sub_df = pol_sub_df.loc[
        (pol_sub_df["person"] != "unassigned") & (pol_sub_df["person"] != "guest")
    ]
    palette = {
        "laura": "C0",
        "matt": "C7",
        "marisha": "C2",
        "sam": "C3",
        "taliesin": "C4",
        "liam": "C5",
        "travis": "C1",
        "ashley": "C6",
        "orion": "C8",
        "guest": "C9",
        "unassigned": "k",
    }

    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 5))
    ax = sns.lineplot(
        x="episode",
        y=Polarity_Subjectivity,
        data=pol_sub_df,
        hue="person",
        marker=".",
        palette=palette,
    )

    if C1_C2 == "C1":
        ax.set(xlim=(1, 115))
    else:
        ax.set(xlim=(1, 128))

    ax.legend(bbox_to_anchor=(1, 1))
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.set_xlabel("Episodes")
    ax.set_ylabel(Polarity_Subjectivity)
    ax.title.set_text("%s: %s per Episode" % (C1_C2, Polarity_Subjectivity))

    path = (
        "images/lineplot_sentiment" + "_" + C1_C2 + "_" + Polarity_Subjectivity + ".png"
    )
    plt.savefig(path, dpi=500, bbox_inches="tight", pad_inches=0.2)
