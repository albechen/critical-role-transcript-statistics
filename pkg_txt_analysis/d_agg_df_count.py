def group_by_person_episode(org_names_df):
    person_episode_group = org_names_df.groupby(['person', 'episode']).agg({'count': ['count', 'sum']})
    person_episode_group = person_episode_group.unstack(level=1, fill_value=0).stack()
    person_episode_group = person_episode_group.unstack(level=-1, fill_value=0).stack().reset_index()
    person_episode_group.columns = ['person', 'episode', 'line_count', 'word_count']
    return person_episode_group


def count_per_episode(person_episode_group):
    cont_l_count = []
    cont_w_count = []
    prev_l_count = 0
    prev_w_count = 0
    prev_name = 'ashley'

    for name, w_count, l_count in zip (person_episode_group['person'], 
        person_episode_group['word_count'],
        person_episode_group['line_count']):

        if name == prev_name:
            prev_l_count += l_count
            cont_l_count.append(prev_l_count)

            prev_w_count += w_count
            cont_w_count.append(prev_w_count)
            
            prev_name = name
        else:
            prev_l_count = l_count
            cont_l_count.append(prev_l_count)

            prev_w_count = w_count
            cont_w_count.append(prev_w_count)
            
            prev_name = name

    person_episode_group['cont_line_count'] = cont_l_count
    person_episode_group['cont_word_count'] = cont_w_count
    
    return person_episode_group