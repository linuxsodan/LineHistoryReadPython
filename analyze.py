#!/usr/bin/env python3
import ipadic
import MeCab
import sys
import pickle
from pprint import pprint
import re


if len(sys.argv) != 2:
    print("usage: " + sys.argv[0] + " [PICKLE FILE]")
    sys.exit(1)

talks = {}
with open(sys.argv[1], mode="rb") as f:
    talks = pickle.load(f)

wday = ["月", "火", "水", "木", "金", "土", "日"]
ext_name = ['System', 'Unknown', 'Auto-reply']

char_cnt = {}
stamp_cnt = {}
name_cnt = {}
date_cnt = {}
wday_cnt = {}
domain_cnt = {}
photo_cnt = 0
movie_cnt = 0
file_cnt = 0

for talk in talks:

    if talk['name'] in ext_name:
        continue

    if talk['comm'] == "[[投票]*]":
        continue

    if talk['comm'] == "[スタンプ]":
        if talk['name'] in stamp_cnt:
            stamp_cnt[talk['name']] += 1
        else:
            stamp_cnt[talk['name']] = 0
        continue

    if talk['comm'] == "[ファイル]":
        file_cnt += 1
        continue
    if talk['comm'] == "[写真]":
        photo_cnt += 1
        continue
    if talk['comm'] == "[動画]":
        movie_cnt += 1
        continue
    if talk['comm'] == "[ボイスメッセージ]":
        continue

        ############################

    # name cnt
    if talk['name'] in name_cnt:
        name_cnt[talk['name']] += 1
    else:
        name_cnt[talk['name']] = 0

    # date cnt
    date_str = talk['date'].strftime("%Y-%m-%d")
    if date_str in date_cnt:
        date_cnt[date_str] += 1
    else:
        date_cnt[date_str] = 0

    # weekday cnt
    wday_str = wday[talk['date'].weekday()] + "曜日"
    if wday_str in wday_cnt:
        wday_cnt[wday_str] += 1
    else:
        wday_cnt[wday_str] = 0

    #####
    comm = talk['comm']
    comm = comm.rstrip()
    comm = comm.replace('\n', ' ').replace('\r', '')
    # c = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '[URL]', c)
    url_prefix = re.search(r'(http|https)+:\/{2}[\d\w-]+(\.[\d\w-]+)*', comm)
    # URL除去
    comm = re.sub(
        r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', comm)
    if url_prefix:
        domain = url_prefix.group(0).split("/")[2]
        if domain in domain_cnt:
            domain_cnt[domain] += 1
        else:
            domain_cnt[domain] = 0

    # char length
    if talk['name'] in char_cnt:
        char_cnt[talk['name']] += len(comm)
    else:
        char_cnt[talk['name']] = len(comm)

char_cnt = sorted(char_cnt.items(), key=lambda e: e[1], reverse=True)
stamp_cnt = sorted(stamp_cnt.items(), key=lambda e: e[1], reverse=True)
name_cnt = sorted(name_cnt.items(), key=lambda e: e[1], reverse=True)
wday_cnt = sorted(wday_cnt.items(), key=lambda e: e[1], reverse=True)
domain_cnt = sorted(domain_cnt.items(), key=lambda e: e[1], reverse=True)

maxv = 5
print("=============================================================")
print("文字数ランキング")
i = 0
for k, v in char_cnt:
    print(str(v) + "\t" + k)
    i += 1
    if i > maxv:
        break
print("=============================================================")
print("スタンプランキング")
i = 0
for k, v in stamp_cnt:
    print(str(v) + "\t" + k)
    i += 1
    if i > maxv:
        break
print("=============================================================")
print("投稿数ランキング")
i = 0
for k, v in name_cnt:
    print(str(v) + "\t" + k)
    i += 1
    if i > maxv:
        break
print("=============================================================")
print("投稿曜日ランキング")
i = 0
for k, v in wday_cnt:
    print(str(v) + "\t" + k)
    i += 1
    if i > maxv:
        break
print("=============================================================")
print("投稿URLドメインランキング")
i = 0
for k, v in domain_cnt:
    print(str(v) + "\t" + k)
    i += 1
    if i > maxv:
        break
print("=============================================================")
print("photo: "+str(photo_cnt))
print("file: "+str(file_cnt))
print("movie: "+str(movie_cnt))
