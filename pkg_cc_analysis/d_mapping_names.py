import pandas as pd


def mapping_names(all_ep_df):
    laura_name_list = ['all', 'laura', 'vex', '-laura']
    matt_name_list = ['all', 'matt', 'matthew', 'decide', '-matt', 'sherri', 'allura', 'gilmore', 'Adra', 'kima', 'kaylee', 'fast', 'uriel', 'balgus', 'mat', 'caught up']
    marisha_name_list = ['all', 'marisha', 'keyleth', '-marisha']
    sam_name_list = ['all', 'sam', 'scanlan', '-sam']
    taliesin_name_list = ['all', 'taliesin', 'percy', '-taliesin']
    liam_name_list = ['all', 'liam', 'vax', '-liam']
    travis_name_list = ['all', 'travis', 'grog', '-travis']
    ashley_name_list = ['all', 'ashley', 'pike', '-ashley']
    orion_name_list = ['orion', 'tiberius', '-orion']
    guest_name_list = ['zac', 'will', 'mary', 'patrick', 'felicia', 'wil', 'chris', 'jon', 'joe', 'darin', 'noelle', 'kit', 'jason', 'patrick rothfuss']
    break_name_list = ['ify', 'dan', 'brian', 'loves in his life', 'ivan', 'kevin', 'this wonderful show are']

    name_list = [laura_name_list, matt_name_list, 
        marisha_name_list, sam_name_list, taliesin_name_list, 
        liam_name_list, travis_name_list, ashley_name_list, 
        orion_name_list, guest_name_list]

    names = ['laura', 'matt', 
        'marisha', 'sam', 'taliesin', 
        'liam', 'travis', 'ashley', 
        'orion', 'guest']

    for names, name_list in zip(names, name_list):
        all_ep_df[names] = all_ep_df['name'].map(lambda y: 1 if any(word in name_list for word in y.split()) else 0)
    
    return all_ep_df


def combine_name_list(named_mapped_df):
    names = ['laura', 'matt', 
        'marisha', 'sam', 'taliesin', 
        'liam', 'travis', 'ashley', 
        'orion', 'guest']
    named_mapped_df['person_check'] = named_mapped_df[names].sum(axis=1)
    org_names_df = pd.DataFrame()

    for name in names:
        filtered_names_df = named_mapped_df.loc[named_mapped_df[name] == 1]
        filtered_names_df = filtered_names_df[['name', 'speech', 'count', 'episode', 'total_time', 'start_time', 'end_time']]
        filtered_names_df['person'] = name
        org_names_df = org_names_df.append(filtered_names_df)
    
    no_assigned_person = named_mapped_df.loc[named_mapped_df['person_check'] == 0]
    no_assigned_person = no_assigned_person[['name', 'speech', 'count', 'episode', 'total_time', 'start_time', 'end_time']]
    no_assigned_person['person'] = 'no_one'
    org_names_df = org_names_df.append(no_assigned_person)

    return org_names_df