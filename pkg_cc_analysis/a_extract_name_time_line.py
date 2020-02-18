def is_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False


def remove_blank_num(raw_srt):
    clean_srt = []
    for line in raw_srt:
        raw_srt = [t for t in raw_srt if t]
        line = line.lower()
        remove_char = ['\'', '\"', '.', ',', '?', '/', '!']
        for char in remove_char:
            line = line.replace(char, '')
        if is_int(line) == False:
            clean_srt.append(line)
    return clean_srt


def extract_time_line(adj_srt):
    speak = ''
    time_line = []
    start_time = 0
    end_time = 0
    count = 0
    
    for line in adj_srt:
        count += 1
        if count != len(adj_srt):
            if '-->' in line.split():
                if speak != '':
                    comb_set = (start_time, end_time, speak)
                    time_line.append(comb_set)

                start_time_split = line.index('-')-1
                start_time = line[:start_time_split]

                end_time_split = line.index('>')+2
                end_time = line[end_time_split:]

                speak = ''
            else:
                if speak == '':
                    speak = line
                else:
                    speak += ' ' + line
        
        else:
            if speak == '':
                speak = line
            else:
                speak += ' ' + line
            comb_set = (start_time, end_time, speak)
            time_line.append(comb_set)

    return time_line