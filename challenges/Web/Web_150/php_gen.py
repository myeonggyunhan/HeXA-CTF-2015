# coding: utf-8

DIR = "/home/web50/public_html/"

import random

word_file = open("word.txt")
word_list = word_file.readlines()

text_file = open("big.txt")
all_text = text_file.read()

bList = random.sample(range(1,len(all_text)),len(word_list)-1)
bList.sort()
bList = [0] + bList + [len(all_text)];

i = 1
tmp = word_list[0][:-1]
for word in word_list[1:]:
    word = word[:-1]
    sub_text = all_text[bList[i-1]:bList[i]]
    try :
        idx = random.randrange(len(sub_text))
    except : idx = 0
    text = sub_text[:idx] + "the answer is " + word + " " + sub_text[idx:]

    php_file = open(DIR+tmp+".php", "w")
    php_file.write(text)
    tmp = word
    i += 1

word_file.close()
