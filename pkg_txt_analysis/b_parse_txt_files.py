import pandas as pd
import a_extract_name_line


def combine_two_part_ep(two_part_ep):
    for ep in two_part_ep:
        join_ep = []
        path_1 = ("S1_txt/C1E%s-1_FINAL.txt" % ep)
        path_2 = ("S1_txt/C1E%s-2_FINAL.txt" % ep)
        with open(path_1, "r", encoding="latin-1") as p1_ep:
            p1_ep = p1_ep.read().splitlines()
            with open(path_2, "r", encoding="latin-1") as p2_ep:
                p2_ep = p2_ep.read().splitlines()
                join_ep = p1_ep + p2_ep
        with open("S1/C1E%s_FINAL.txt" % ep, 'w', encoding='latin-1') as comb_ep:
            for line in join_ep:
                comb_ep.write('%s\n' % line)


def episode_extract(start_ep, end_ep):
    all_ep_df = pd.DataFrame()
    end_ep += 1
    ep_list = list(range(start_ep,end_ep))
    ep_zfill = [str(ep).zfill(3) for ep in ep_list]
    
    for ep in ep_zfill:
        path = ("S1_txt/C1E%s_FINAL.txt" % ep)
        with open(path, "r", encoding="latin-1") as ep_raw:
            ep_raw = ep_raw.read().splitlines()
            ep_df = a_extract_name_line.extract_lines(ep_raw)
            ep_df['episode'] = ep
            all_ep_df = all_ep_df.append(ep_df)

    return all_ep_df