import re

# トーク行チェック
def check_time(row):
    return re.match("^[0-9][0-9]:[0-9][0-9] .+ .+$", row)


# 日時行チェック
def check_date(row):
    return re.match("^[0-9][0-9][0-9][0-9]\.[0-9]+\.[0-9]+ ...$", row)


# 空行チェック
def check_empty_row(row):
    return re.match("^$", row)


# ファイル出力ヘッダー生成
def create_file_header(outputs):
    headers = ["日付", "時刻", "名前", "トーク"]
    outputs.append(",".join(headers))


# ファイル出力列生成
def create_file_row(outputs, talk_row):
    outputs.append(",".join(talk_row))


read_file = "[LINE]LINUX 雑談質問部屋.txt"

f = open(read_file, encoding="utf-8")
rows = f.read().split("\n")
f.close()

outputs = []

# ファイルのヘッダー作成
create_file_header(outputs)

start_talk = False
talk_row = []
talk_date = "2021.11.22 月曜日"

for row in rows:
    if check_time(row):
        if start_talk:
            create_file_row(outputs, talk_row)
        start_talk = True
        talk_row = []
        talk_row.append(talk_date)
        talk_row.extend(row.split(" "))
        continue
    if start_talk:
        talk_row[3] += row
        continue
    if check_date(row):
        start_talk = False
        talk_date = row
        continue
    if check_empty_row(row):
        start_talk = False
        continue
create_file_row(outputs, talk_row)

outputs_csv = "\n".join(outputs)

with open("test.csv", "w", encoding="utf-8") as f:
    f.write(outputs_csv)
