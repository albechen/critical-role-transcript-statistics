import pandas as pd


def split_name_speech_count(cont_line):
    name_split = cont_line.index(':')
    name = cont_line[:name_split]

    speak_split = name_split + 2
    speak = cont_line[speak_split:]

    count = len(speak.split())

    split_line = (name, speak, count)
    return split_line


def extract_lines(raw_lines):
    count = 0
    org_list = []
    cont_line = []
    raw_lines = [t for t in raw_lines if t]

    for line in raw_lines:
        line = line.lower()
        remove_char = ['\'', '\"', '.', ',', '?', '/', '!']
        for char in remove_char:
            line = line.replace(char, '')

        count += 1
        if count != len(raw_lines):
            if ':' in line:
                colen_index= line.index(':')
                if colen_index <= 30:
                    if cont_line != []:
                        split_line = split_name_speech_count(cont_line)
                        org_list.append(split_line)
                        cont_line = line
                    else:
                        cont_line = line
                else:
                    cont_line += ' ' + line
            elif org_list == []:
                pass
            else:
                cont_line += ' ' + line
        else:
            if ':' in line:
                colen_index= line.index(':')
                if colen_index <= 30:
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)

                    split_line = split_name_speech_count(line)
                    org_list.append(split_line)
                else:
                    cont_line += ' ' + line
                    split_line = split_name_speech_count(cont_line)
                    org_list.append(split_line)
            else:
                cont_line += ' ' + line
                split_line = split_name_speech_count(cont_line)
                org_list.append(split_line)

    ep_df = pd.DataFrame(org_list, columns =['name', 'speech', 'count'])

    return ep_df
