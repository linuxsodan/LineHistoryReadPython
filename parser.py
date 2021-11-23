import re
from datetime import datetime

# トーク行チェック
def is_talkline(line):
    return re.match("^[0-9][0-9]:[0-5][0-9]\\t.*?\\t.*?$", line)

def is_sysmesg(line):
    return re.match("^[0-9][0-9]:[0-5][0-9]\\t.*$", line)

# 日時行チェック
def is_dateline(line):
    return re.match("^[0-9]{4}/[0-1][0-9]/[0-3][0-9](...)$", line)


# 空行チェック
def is_emptyline(line):
    return re.match("^$", line)


# ファイル出力列生成
#def create_file_row(outputs, talk_row):
    #outputs_csv = "\n".join(outputs)


def line_history_parse(filename):
    f = open(filename, encoding="utf-8")
    lines = f.read().split("\n")
    f.close()

    talks = []
    talk = {}
    talk_date = None
    is_talking = False
    date_str = None

    is_prev_emptyline = False
    is_talking_emptyline = False
    is_talking_dateline = False
    tmp_previous_line = None

    header = lines.pop(0)
    save_date = datetime.strptime(lines.pop(0).split("：")[1],'%Y/%m/%d %H:%M')

    for line in lines:
        #print(line)
        # NOTE: システムメッセージ後の空行と3行目対策
        if is_emptyline(line) and not is_talking:
            continue

        # 前行が日付ラインで現行がタブ文字含むチャット一行目なら...
        if is_talking_dateline and is_talkline(line):
            talks.append(talk)
            is_talking = False
            is_talking_dateline = False
            date_str = tmp_previous_line.split("(")[0] # YYYY/MM/DD
            tmp_previous_line = None
            # このまま is_talklineブロックへ飛ぶ.
        elif is_talking_dateline:
            # 単純な日付ライン（チャットメッセージ上の）なら
            talk["message"].append(tmp_previous_line)
            is_talking_dateline = False
            tmp_previous_line = None

        # 日付チェック
        if is_dateline(line):
            if is_talking:
                # 2行目以降にYYYY/MM/DD(W)が来てしまった場合を想定して次の行を確認。
                is_talking_dateline = True
                tmp_previous_line = line
                continue
            is_talking = False
            date_str = line.split("(")[0] # YYYY/MM/DD
            continue

        # チャット一行目
        if is_talkline(line):
            if is_talking:
                talks.append(talk)
            is_talking = True
            talk = {}
            time_str = line.split("\t")[0]
            date_obj = datetime.strptime(date_str + " " + time_str ,'%Y/%m/%d %H:%M')
            talk["date"] = date_obj
            talk["author"] = line.split("\t")[1]
            talk["message"] = []
            talk["message"].append(line.split("\t")[2])
            continue

        #####
        # ここで、前行が空行なら追加する
        if is_talking_emptyline:
            talk["message"].append("")
            is_taling_emptyline = False

        # チャット二行目以降
        if is_talking:
            if is_emptyline(line):
                is_talking_emptyline = True
            else:
                talk["message"].append(line)
            continue

        # システムメッセージ（タブ二つ）
        if is_sysmesg(line):
            if is_talking:
                talks.append(talk)
            talk = {}
            talk["date"] = date_obj
            talk["time"] = line.split("\t")[0]
            talk["message"] = []
            talk["message"].append(line.split("\t")[1])
            talks.append(talk)
            is_talking = False
            continue

        print("WARNING: unknown line: "+ line)
    return header,save_date,talks
