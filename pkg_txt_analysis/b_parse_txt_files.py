import pandas as pd
from .a_extract_name_line import extract_lines


def combine_two_part_ep(C1_C2, two_part_ep):
    for ep in two_part_ep:
        join_ep = []
        path_1 = ("data_raw/%s_txt/%sE%s-1_FINAL.txt" % (C1_C2, C1_C2, ep))
        path_2 = ("data_raw/%s_txt/%sE%s-2_FINAL.txt" % (C1_C2, C1_C2, ep))
        with open(path_1, "r", encoding="latin-1") as p1_ep:
            p1_ep = p1_ep.read().splitlines()
            with open(path_2, "r", encoding="latin-1") as p2_ep:
                p2_ep = p2_ep.read().splitlines()
                join_ep = p1_ep + p2_ep
        with open("data_raw/%s_txt/C1E%s_FINAL.txt" % (C1_C2, ep), 'w', encoding='latin-1') as comb_ep:
            for line in join_ep:
                comb_ep.write('%s\n' % line)


def episode_extract(C1_C2, start_ep, end_ep):
    all_ep_df = pd.DataFrame()
    end_ep += 1
    ep_list = list(range(start_ep,end_ep))
    ep_zfill = [str(ep).zfill(3) for ep in ep_list]
    
    for ep in ep_zfill:
        path = ("data_raw/%s_txt/%sE%s_FINAL.txt" % (C1_C2, C1_C2, ep))
        with open(path, "r", encoding="latin-1") as ep_raw:
            ep_raw = ep_raw.read().splitlines()
            ep_df = extract_lines(ep_raw)
            ep_df['episode'] = ep
            all_ep_df = all_ep_df.append(ep_df)

    return all_ep_df