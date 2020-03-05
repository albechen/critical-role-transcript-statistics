import os
import pandas as pd
import time
from .a_clean_vtt import remove_blank_num, extract_time_line
from .b_sort_vtt_lines import align_full_line_time


def combine_two_part_ep(C1_C2, file1, file2, ep_num):
    join_ep = []
    path_1 = "data_raw/%s_vtt/%s" % (C1_C2, file1)
    path_2 = "data_raw/%s_vtt/%s" % (C1_C2, file2)
    with open(path_1, "r", encoding="latin-1") as p1_ep:
        p1_ep = p1_ep.read().splitlines()
        with open(path_2, "r", encoding="latin-1") as p2_ep:
            p2_ep = p2_ep.read().splitlines()
            join_ep = p1_ep + p2_ep
    with open(
        "data_raw/%s_vtt/%s_%s.vtt" % (C1_C2, C1_C2, ep_num), "w", encoding="latin-1"
    ) as comb_ep:
        for line in join_ep:
            comb_ep.write("%s\n" % line)


def rename_vtt(C1_C2):
    for filename in os.listdir("data_raw/%s_vtt" % C1_C2):
        if "Episode" in filename or "Epsiode" in filename:
            str_file = str(filename)
            envtt_index = str_file.index(".en.vtt")
            str_file = str_file[:envtt_index].split()
            if "Episode" in filename:
                ep_index = str_file.index("Episode")
            else:
                ep_index = str_file.index("Epsiode")
            ep_num = str_file[ep_index + 1]
            if C1_C2 == "C1":
                if ep_num in [31, 33, 35]:
                    pass
                else:
                    rename_file = C1_C2 + "_" + ep_num + ".vtt"
                    rename_file = str(rename_file)
                    os.rename(
                        os.path.join("data_raw/%s_vtt" % C1_C2, filename),
                        os.path.join("data_raw/%s_vtt" % C1_C2, rename_file),
                    )
            else:
                if "-" in ep_num:
                    dash_index = ep_num.index("-")
                    ep_num = ep_num[:dash_index]
                    rename_file = C1_C2 + "_" + ep_num + ".vtt"
                    rename_file = str(rename_file)
                    os.rename(
                        os.path.join("data_raw/%s_vtt" % C1_C2, filename),
                        os.path.join("data_raw/%s_vtt" % C1_C2, rename_file),
                    )
                else:
                    rename_file = C1_C2 + "_" + ep_num + ".vtt"
                    rename_file = str(rename_file)
                    os.rename(
                        os.path.join("data_raw/%s_vtt" % C1_C2, filename),
                        os.path.join("data_raw/%s_vtt" % C1_C2, rename_file),
                    )
        else:
            pass


def preprocess_df(raw_file):
    removed_file = remove_blank_num(raw_file)
    time_line = extract_time_line(removed_file)
    aligned_df = align_full_line_time(time_line)
    return aligned_df


def episode_extract(C1_C2, start_ep, end_ep):
    all_ep_df = pd.DataFrame()
    end_ep += 1
    ep_list = list(range(start_ep, end_ep))
    start_time = time.time()

    for ep in ep_list:
        path = "data_raw/%s_vtt/%s_%s.vtt" % (C1_C2, C1_C2, ep)
        try:
            with open(path, "r", encoding="latin-1") as ep_raw:
                ep_raw = ep_raw.read().splitlines()
                ep_df = preprocess_df(ep_raw)
                ep_df["episode"] = ep
                all_ep_df = all_ep_df.append(ep_df)
        except:
            pass
        if int(ep) % 10 == 0:
            print(
                "Completed: ep %s (%s min)"
                % (ep, round(((time.time() - start_time) / 60), 2))
            )
            start_time = time.time()
        if int(ep) == end_ep - 1:
            print("Completed: all")

    return all_ep_df
