import pandas as pd

def calc_time(full_ep_df):
    full_ep_df['start_time'] = [
        (int(ts[:2])*60*60 + int(ts[3:5])*60 + int(ts[6:8]) + int(ts[8:11])/1000)
        for ts in full_ep_df['start_time']]
    full_ep_df['end_time'] = [
        (int(ts[:2])*60*60 + int(ts[3:5])*60 + int(ts[6:8]) + int(ts[8:11])/1000)
        for ts in full_ep_df['end_time']]
    
    full_ep_df['total_time'] = full_ep_df['end_time'] - full_ep_df['start_time']
    return full_ep_df

def mapping_names(all_ep_df, C1_C2):
    laura_name_list = ['all', 'laura', 'vex', '-laura']
    matt_name_list = ['all', 'matt', 'matthew', 'decide', '-matt', 'sherri', 'allura', 'gilmore', 'Adra', 'kima', 'kaylee', 'fast', 'uriel', 'balgus', 'mat', 'caught up', 'last we left off']
    marisha_name_list = ['all', 'marisha', 'keyleth', '-marisha']
    sam_name_list = ['all', 'sam', 'scanlan', '-sam']
    taliesin_name_list = ['all', 'taliesin', 'percy', '-taliesin']
    liam_name_list = ['all', 'liam', 'vax', '-liam']
    travis_name_list = ['all', 'travis', 'grog', '-travis']
    ashley_name_list = ['all', 'ashley', 'pike', '-ashley']
    orion_name_list = ['orion', 'tiberius', '-orion']
    C1_guest_name_list = ['zac', 'will', 'mary', 'patrick', 'felicia', 'wil', 'chris', 'jon', 'joe', 'darin', 'noelle', 'kit', 'jason', 'patrick rothfuss']
    C2_gues_name_list = ['chris', 'mica', 'ashly', 'khary', 'sumalee', 'deborah', 'mark']
    break_name_list = ['ify', 'dan', 'brian', 'loves in his life', 'ivan', 'kevin', 'this wonderful show are']

    name_list = [laura_name_list, matt_name_list, 
        marisha_name_list, sam_name_list, taliesin_name_list, 
        liam_name_list, travis_name_list, ashley_name_list, 
        orion_name_list]
    if C1_C2 == 'C1':
        name_list = name_list + [C1_guest_name_list]
    else:
        name_list = name_list + [C2_gues_name_list]

    names = ['laura', 'matt', 
        'marisha', 'sam', 'taliesin', 
        'liam', 'travis', 'ashley', 
        'orion', 'guest']
    all_ep_df['name'] = all_ep_df['name'].astype('str')
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


def org_time_person(parsed_df, C1_C2):
    extract_time = calc_time(parsed_df)
    extract_names = mapping_names(extract_time, C1_C2)
    org_names = combine_name_list(extract_names)
    return org_names