import pandas as pd

# process vtt to orginized lines by names notated by " : "


def split_name_speech_count(cont_line):
    name_split = cont_line[2].index(":")
    name = cont_line[2][:name_split]

    speak_split = name_split + 2
    speak = cont_line[2][speak_split:]

    count = len(speak.split())

    split_line = (cont_line[0], cont_line[1], name, speak, count)
    return split_line


def align_full_line_time(time_line):
    count = 0
    org_list = []
    cont_line = []

    for line in time_line:
        line = list(line)
        count += 1
        if count != len(time_line):  # used to remove last line
            if ":" in line[2]:  # check if named person
                colen_index = line[2].index(":")  # add name to list
                if colen_index <= 30:  # check if name is too long
                    if cont_line != []:  # check if new line should be started
                        split_line = split_name_speech_count(cont_line)
                        org_list.append(split_line)
                        cont_line = line
                    else:
                        cont_line = line
                else:
                    cont_line[1] = line[1]
                    cont_line[2] += " " + line[2]
            elif org_list == []:  # should only apply before first line finishes
                pass
            else:  # if the line is anything else besides named person
                cont_line[1] = line[1]
                cont_line[2] += " " + line[2]
        else:  # similar code to above, but adds whatever line is present and stops
            org_list.append(split_line)
            if ":" in line[2]:
                colen_index = line[2].index(":")
                if colen_index <= 30:
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)

                    cont_line = line
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)
                else:
                    cont_line[1] = line[1]
                    cont_line[2] += " " + line[2]
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)
            else:
                cont_line[1] = line[1]
                cont_line[2] += " " + line[2]
                split_line = split_name_speech_count(cont_line)
                org_list.append(split_line)

    ep_df = pd.DataFrame(
        org_list, columns=["start_time", "end_time", "name", "speech", "count"]
    )

    return ep_df
