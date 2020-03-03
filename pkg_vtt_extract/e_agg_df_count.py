from textblob import TextBlob


def group_by_person_episode(org_names_df):
    person_episode_group = org_names_df.loc[org_names_df['total_time'] <= 120]
    person_episode_group = person_episode_group.groupby(['person', 'episode']).agg({'total_time':['count','sum'], 'count':['sum']})
    
    person_episode_group = person_episode_group.unstack(level=1, fill_value=0).stack()
    person_episode_group = person_episode_group.unstack(level=-1, fill_value=0).stack().reset_index()
    
    person_episode_group.columns = person_episode_group.columns.map('_'.join).str.strip('_')
    person_episode_group['episode'] = person_episode_group['episode'].astype('int')
    person_episode_group = person_episode_group.rename(columns={'total_time_count': 'line_count', 'total_time_sum': 'time_count', 'count_sum': 'word_count'})
    
    return person_episode_group


def group_by_episode(org_names_df):
    org_names_df = org_names_df.loc[org_names_df['person'] != 'unassigned'] 
    person_group = org_names_df.groupby(['episode']).agg({'total_time':['sum']}).reset_index()
    
    person_group.columns = ['episode', 'time_count']
    person_group['episode'] = person_group['episode'].astype('int')
    
    return person_group


def count_per_episode(person_episode_group):
    cont_l_count = []
    cont_w_count = []
    cont_t_count = []
    prev_l_count = 0
    prev_w_count = 0
    prev_t_count = 0
    prev_name = 'ashley'

    for name, w_count, l_count, t_count in zip (person_episode_group['person'],
        person_episode_group['word_count'],
        person_episode_group['line_count'],
        person_episode_group['time_count']):

        if name == prev_name:
            prev_l_count += l_count
            cont_l_count.append(prev_l_count)

            prev_w_count += w_count
            cont_w_count.append(prev_w_count)

            prev_t_count += t_count
            cont_t_count.append(prev_t_count)
            
            prev_name = name
        else:
            prev_l_count = l_count
            cont_l_count.append(prev_l_count)

            prev_w_count = w_count
            cont_w_count.append(prev_w_count)

            prev_t_count = t_count
            cont_t_count.append(prev_t_count)
            
            prev_name = name

    person_episode_group['cont_line_count'] = cont_l_count
    person_episode_group['cont_word_count'] = cont_w_count
    person_episode_group['cont_time_count'] = cont_t_count
    
    return person_episode_group


def sentiment_per_person_and_episode(org_name):
    speech_per_person_ep = org_name.groupby(['episode','person'])['speech'] \
            .apply(lambda x: '. '.join(x))
    speech_per_person_ep = speech_per_person_ep.reset_index()

    speech_per_person_ep['Subjectivity'] = 0
    speech_per_person_ep['Polarity'] = 0

    speech_per_person_ep['Subjectivity'] = speech_per_person_ep['speech'] \
            .apply(lambda x: TextBlob(x).sentiment.subjectivity)
    speech_per_person_ep['Polarity'] = speech_per_person_ep['speech'] \
            .apply(lambda x: TextBlob(x).sentiment.polarity)

    speech_per_person_ep = speech_per_person_ep.loc[
                    (speech_per_person_ep['Polarity'] >= -0.7) & 
                    (speech_per_person_ep['Polarity'] <= 0.7) & 
                    (speech_per_person_ep['Subjectivity'] >= 0.3) & 
                    (speech_per_person_ep['Subjectivity'] <= 0.7)]
    
    return speech_per_person_ep