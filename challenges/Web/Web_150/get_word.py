wordCount = 200

import requests
r = requests.get("http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt")
wordList = r.text.split('\n')

import random
wordSelected = random.sample(wordList, wordCount)
f = open("word.txt","w")
f.write('\n'.join(wordSelected))
