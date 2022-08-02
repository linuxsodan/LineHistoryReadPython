import re
import datetime
from pprint import pprint

ja_weekday = ['月','火','水','木','金','土','日']
LF_terminator = "\n"

# 日時行チェック
def get_date_line(line,today):
        s = line.split('(')
        if len(s) != 2:
            return False, None
        ss = s[1].rstrip(')')
        if not ss in ja_weekday:
            return False, None
        try:
            t = datetime.datetime.strptime(s[0],"%Y/%m/%d").date()
            return True, t
        except ValueError:
            return False, None

def get_line_with_time_and_name(line):
    s = line.split("\t")
    if len(s) != 3:
        return False, None, None, None
    try:
        t = datetime.datetime.strptime(s[0],"%H:%M").time()
    except ValueError:
        return False, None, None, None
    return True, t, s[1], s[2]

def get_line_with_time_and_system_msg(line):
    s = line.split("\t")
    if len(s) != 2:
        return False, None, None
    try:
        t = datetime.datetime.strptime(s[0],"%H:%M").time()
    except ValueError:
        return False, None, None
    return True, t, s[1]
    





def get_date_from_line(line):
    return datetime.datetime.strptime(line.split('(')[0],"%Y/%m/%d").date()
def get_time_from_line(line):
    return datetime.datetime.strptime(line.split('(')[0],"%H:%M").time()

def parser(data):

    rows = data.splitlines()

    room = re.sub('^\[LINE\]\ ','',rows.pop(0))
    room = re.sub('のトーク$','',room)
    # pprint(room)

    save_date = re.sub("^保存日時：","",rows.pop(0))
    save_date = datetime.datetime.strptime(save_date,"%Y/%m/%d %H:%M")
    # pprint(save_date)
    
    today = datetime.date.today()
    if save_date.year > today.year:
        print("Error: Invalid File. save_date.year="+save_date.year)
        return

    rows.pop(0) # Blank Line
    current_date = get_date_from_line(rows.pop(0))
    current_talk = {}
    current_talk_str = []
    talks =[]
    
    previous_line_is_empty = False
    
    for row in rows:
        flag, new_date = get_date_line(row,today)
        if previous_line_is_empty and flag:
            current_date = get_date_from_line(row)
            flag = False
            continue

        flag, new_time, new_name, new_comm = get_line_with_time_and_name(row);
        if flag:
            if current_talk_str:
                if len(current_talk_str) > 1:
                    # Note: Multiple lines are quoted with "" for some reason,
                    current_talk_str[0] = current_talk_str[0].lstrip('"')
                    current_talk_str[-1] = current_talk_str[-1].rstrip('"')
                    comm = LF_terminator.join(current_talk_str)
                else:
                    comm = current_talk_str[0]
                combined_date = datetime.datetime.combine(current_date, current_time)
                talks.append({'date':combined_date,'name':current_name,'comm':comm})
                current_talk_str = []
            current_time = new_time
            current_name = new_name
            current_talk_str.append(new_comm)
            flag = False
            continue
        
        flag, new_time, new_msg = get_line_with_time_and_system_msg(row)
        if previous_line_is_empty and flag:
            if current_talk_str:
                if len(current_talk_str) > 1:
                    # Note: Multiple lines are quoted with "" for some reason,
                    current_talk_str[0] = current_talk_str[0].lstrip('"')
                    current_talk_str[-1] = current_talk_str[-1].rstrip('"')
                    comm = LF_terminator.join(current_talk_str)
                else:
                    comm = current_talk_str[0]
                combined_date = datetime.datetime.combine(current_date, current_time)
                talks.append({'date':combined_date,'name':current_name,'comm':comm})
                current_talk_str = []
            current_time = new_time
            current_name = "System"
            current_talk_str.append(new_msg)
            flag = False
            continue
        
        if previous_line_is_empty:
            # Note: append blank. after join with LF.
            current_talk_str.append("")
            previous_line_is_empty = False

        if re.match("^$",row):
            previous_line_is_empty = True
            continue
        
        current_talk_str.append(row)
    return talks


            
            


