# vtt.org_df_person_episode_lines(C1_org_name, 'sam', 4)
def org_df_person_episode_lines(org_name, name, ep):
    test = org_name.loc[(org_name["person"] == name) & (org_name["episode"] == ep)]
    print("total time: ", sum(test["total_time"]))
    return test


# vtt.serach_vtt('C2', 1, 90, '[groovy critical role theme]')
def serach_vtt(C1_C2, start_ep, end_ep, search_string):
    end_ep += 1
    ep_list = list(range(start_ep, end_ep))

    for ep in ep_list:
        path = "data_raw/%s_vtt/%s_%s.vtt" % (C1_C2, C1_C2, ep)
        try:
            with open(path, "r", encoding="latin-1") as ep_raw:
                ep_raw = ep_raw.read().splitlines()
                for line in ep_raw:
                    line = line.lower()
                    if search_string in line:
                        print("in ep:", ep)
                        pass
        except:
            pass

