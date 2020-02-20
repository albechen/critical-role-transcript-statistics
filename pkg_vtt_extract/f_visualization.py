import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

from .e_agg_df_count import group_by_person_episode, count_per_episode


def lineplot_per_ep (org_names, matt_nomatt, C1_C2):
    person_episode_group = group_by_person_episode(org_names)

    palette ={'laura':'C0', 
        'matt':'C7', 
        'marisha':'C2', 
        'sam':'C3', 
        'taliesin':'C4', 
        'liam':'C5', 
        'travis':'C1', 
        'ashley':'C6', 
        'orion':'C8', 
        'guest':'C9',
        'unassigned':'k'}

    if matt_nomatt == 'nomatt':
        person_episode_group = person_episode_group.loc[person_episode_group['person'] != 'matt']

    sns.set_style('whitegrid')
    plt.figure(figsize=(15,5))
    ax = sns.lineplot(x="episode", y="time_count", data=person_episode_group, 
        hue='person', marker='.', palette=palette)

    if C1_C2 == 'C1':
        ax.set(xlim=(1, 115))
    else:
        ax.set(xlim=(1, 90))

    ax.legend(bbox_to_anchor=(1, 1))
    ax.xaxis.set_major_locator(MultipleLocator(5))
    

def lineplot_cont_count (org_names, matt_nomatt, C1_C2):
    person_episode_group = group_by_person_episode(org_names)
    count_per_ep = count_per_episode(person_episode_group)

    palette ={'laura':'C0', 
        'matt':'C7', 
        'marisha':'C2', 
        'sam':'C3', 
        'taliesin':'C4', 
        'liam':'C5', 
        'travis':'C1', 
        'ashley':'C6', 
        'orion':'C8', 
        'guest':'C9',
        'unassigned':'k'}

    if matt_nomatt == 'nomatt':
        count_per_ep = count_per_ep.loc[count_per_ep['person'] != 'matt']

    sns.set_style('whitegrid')

    plt.figure(figsize=(7,5))
    ax = sns.lineplot(x="episode", y="cont_time_count", 
        data=count_per_ep, hue='person', palette=palette)

    if C1_C2 == 'C1':
        ax.set(xlim=(1, 115))
    else:
        ax.set(xlim=(1, 90))

    ax.legend(bbox_to_anchor=(1, 1))
    ax.xaxis.set_major_locator(MultipleLocator(10))


def densityplot_time_per_ep (org_name):
    C1_person_episode_group = group_by_person_episode(org_name)
    names = ['matt', 'laura',  
            'sam', 'marisha', 'travis', 
            'liam', 'taliesin', 'ashley']

    palette ={'laura':'C0', 
        'matt':'C7', 
        'marisha':'C2', 
        'sam':'C3', 
        'taliesin':'C4', 
        'liam':'C5', 
        'travis':'C1', 
        'ashley':'C6', 
        'orion':'C8', 
        'guest':'C9',
        'unassigned':'k'}

    plt.figure(figsize=(7,5))
    for name in names:
        color = palette[name]
        g = sns.kdeplot(C1_person_episode_group["time_count"][(C1_person_episode_group["person"] == name)], shade=True, color=color)
    g.legend(names)
    g.set_xlim(left=0)