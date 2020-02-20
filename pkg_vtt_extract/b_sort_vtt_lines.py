import pandas as pd


def split_name_speech_count(cont_line):
    name_split = cont_line[2].index(':')
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
        if count != len(time_line):
            if ':' in line[2]:
                colen_index = line[2].index(':')
                if colen_index <= 30:
                    if cont_line != []:
                        split_line = split_name_speech_count(cont_line)
                        org_list.append(split_line)
                        cont_line = line
                    else:
                        cont_line = line
                else:
                    cont_line[1] = line[1]
                    cont_line[2] += ' ' + line[2]
            elif org_list == []:
                pass
            else:
                cont_line[1] = line[1]
                cont_line[2] += ' ' + line[2]
        else:
            org_list.append(split_line)
            if ':' in line[2]:
                colen_index= line[2].index(':')
                if colen_index <= 30:
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)

                    cont_line = line
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)
                else:
                    cont_line[1] = line[1]
                    cont_line[2] += ' ' + line[2]
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)
            else:
                cont_line[1] = line[1]
                cont_line[2] += ' ' + line[2]
                split_line = split_name_speech_count(cont_line)
                org_list.append(split_line)

    ep_df = pd.DataFrame(org_list, columns =['start_time', 'end_time', 'name', 'speech', 'count'])

    return ep_df