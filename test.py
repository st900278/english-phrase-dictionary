import linggle_api
import NetSpeakAPI
from itertools import *
from collections import defaultdict, Counter
import BncTagger
import re
import disambiguate

data = open("place.txt", "r").readlines()
data =[x[:-1] for x in data]
'''
x = defaultdict(lambda :defaultdict(bool))
rank = defaultdict(float)
for o in data:
    print o
    for a in data:
        if(x[o][a]):
            continue
        x[o][a] = True
        x[a][o] = True
        d = disambiguate.wordSim(o, a, "n")
        rank[o] += d
        rank[a] += d

print rank
'''
x = sorted(data, key=lambda x:disambiguate.wordSim(x, "place", "n"), reverse=True)

print x[:40]

x = sorted(data, key=lambda x:disambiguate.wordSim(x, "location", "n"), reverse=True)

print x[:40]

