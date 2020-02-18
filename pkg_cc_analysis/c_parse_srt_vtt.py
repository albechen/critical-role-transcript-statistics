import pandas as pd
from .a_extract_name_time_line import remove_blank_num, extract_time_line
from .b_align_full_lines import align_full_line_time


def combine_two_part_ep(C1_C2, two_part_ep):
    for ep in two_part_ep:
        join_ep = []
        path_1 = ("data_raw/%s_cc/%sE%s-1_FINAL.vtt" % (C1_C2, C1_C2, ep))
        path_2 = ("data_raw/%s_cc/%sE%s-1_FINAL.vtt" % (C1_C2, C1_C2, ep))
        with open(path_1, "r", encoding="latin-1") as p1_ep:
            p1_ep = p1_ep.read().splitlines()
            with open(path_2, "r", encoding="latin-1") as p2_ep:
                p2_ep = p2_ep.read().splitlines()
                join_ep = p1_ep + p2_ep
        with open("data_raw/%s_cc/%sE%s_FINAL.srt" % (C1_C2, C1_C2, ep), 'w', encoding='latin-1') as comb_ep:
            for line in join_ep:
                comb_ep.write('%s\n' % line)


def preprocess_df(raw_file):
    removed_file = remove_blank_num(raw_file)
    time_line = extract_time_line(removed_file)
    aligned_df = align_full_line_time(time_line)
    return aligned_df


def calc_time(full_ep_df):
    full_ep_df['start_time'] = [
        (int(ts[:2])*60*60 + int(ts[3:5])*60 + int(ts[6:8]) + int(ts[8:13])/1000)
        for ts in full_ep_df['start_time']]
    full_ep_df['end_time'] = [
        (int(ts[:2])*60*60 + int(ts[3:5])*60 + int(ts[6:8]) + int(ts[8:13])/1000)
        for ts in full_ep_df['end_time']]
    
    full_ep_df['total_time'] = full_ep_df['end_time'] - full_ep_df['start_time']
    return full_ep_df


def episode_extract(C1_C2, start_ep, end_ep):
    all_ep_df = pd.DataFrame()
    end_ep += 1
    ep_list = list(range(start_ep, end_ep))
    if 82 in ep_list:
        ep_list.remove(82)
    ep_zfill = [str(ep).zfill(3) for ep in ep_list]
    
    for ep in ep_zfill:
        if C1_C2 == 'C1':
            path = ("data_raw/%s_cc/%sE%s_FINAL.txt" % (C1_C2, C1_C2, ep))
        else:
            path = ("data_raw/%s_cc/%sE%s_FINAL.vtt" % (C1_C2, C1_C2, ep))
        try:
            with open(path, "r", encoding="latin-1") as ep_raw:
                ep_raw = ep_raw.read().splitlines()
                ep_df = preprocess_df(ep_raw)
                ep_df['episode'] = ep
                all_ep_df = all_ep_df.append(ep_df)
            return all_ep_df
        except ValueError:
            pass
        if int(ep) % 10 == 0:
            print ('Completed: ep ', ep)
        if int(ep) == end_ep:
            print ('Completed: ep ', ep)

    all_ep_df = calc_time(all_ep_df)

    return all_ep_df