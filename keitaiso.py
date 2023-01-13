#!/usr/bin/env python3
import sys
import MeCab
import ipadic
from pprint import pprint
import demoji

t = MeCab.Tagger(ipadic.MECAB_ARGS)  # [3]から
l = []
exts = ["助詞", "助動詞", "記号", "動詞", "非自立", "代名詞", "接尾", "数"]
for line in open('comm.lst'):
    s = line.rstrip('\n')  # [5]から
    # s = demoji.replace(string=''.join(s), repl="")
    words = t.parse(s).split('\n')[:-2]
    for e in words:
        word = e.split('\t')
        word_str = word[0]
        wtypes = word[1].split(',')
        # 邪魔なのでちょこちょこ条件加える
        """
        if word_str.find("ありがとう") != -1:
            print(word_str)
            continue
        """
        and_v = set(wtypes) & set(exts)
        if len(and_v) > 0:
            continue

        if not "名詞" in wtypes:
            continue

        # DEBUG: 最頻出の単語がどういうので使われているか
        if False:
            if "Linux" == word_str:
                pprint(word)
                sys.exit(0)

        l.append(word_str.capitalize())

# DEBUG: ここで終了させる場合

wordFreq = {}

for word in l:
    if word in wordFreq:
        wordFreq[word] += 1
    else:
        wordFreq[word] = 1

# 集計した単語の,出現回数を出力
wordFreq = sorted(wordFreq.items(), key=lambda e: e[1], reverse=True)
i = 0
for word, count in wordFreq:
    print(count, word)
    i += 1
    if i > 50:
        break
