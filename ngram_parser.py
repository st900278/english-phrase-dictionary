import linggle_api
import NetSpeakAPI
from itertools import *
from collections import defaultdict
import BncTagger


det = ['your', 'our', 'their', 'his', 'her', 'my', 'its', 'the', 'a', 'an', 'this', 'that', 'these', 'those']

data = set([x[:-1] for x in open("place.txt").readlines()])

gram = open("web1t-small/3gm.small", "r").readlines()


phrase_coll = defaultdict(list)


for phrase in gram:
	#print phrase
	sentence = phrase[:-1].split()

	
	if sentence[-2] in data:
		origin = sentence[-2]
		newsentence = sentence[:-1]
		newsentence[-1] = '(some place)'

		for idx in range(0, len(sentence)-2):
			if sentence[idx] in det:
				newsentence[idx] = ''

		newsentence = [x for x in newsentence if x != ""]


		key = ' '.join(newsentence);


		if len(phrase_coll[key]) == 0:
			phrase_coll[key].append(0)
			phrase_coll[key].append(set())

		phrase_coll[key][0] += int(sentence[-1])
		phrase_coll[key][1].add(origin)


x = sorted(phrase_coll.items(), key=lambda x: x[1], reverse=True)

f = open("result7.txt", "w")
for (key, value) in x[:1000]:
	f.write(key + '\n')

gram = open("web1t-small/4gm.small", "r").readlines()

phrase_coll = defaultdict(list)

for phrase in gram:
	# print phrase
	sentence = phrase[:-1].split()

	if sentence[-2] in data:
		origin = sentence[-2]
		newsentence = sentence[:-1]
		newsentence[-1] = '(some place)'

		for idx in range(0, len(sentence) - 2):
			if sentence[idx] in det:
				newsentence[idx] = ''

		newsentence = [x for x in newsentence if x != ""]

		key = ' '.join(newsentence);

		if len(phrase_coll[key]) == 0:
			phrase_coll[key].append(0)
			phrase_coll[key].append(set())

		phrase_coll[key][0] += int(sentence[-1])
		phrase_coll[key][1].add(origin)

x = sorted(phrase_coll.items(), key=lambda x: x[1], reverse=True)

for (key, value) in x[:1000]:
	f.write(key + '\n')

gram = open("web1t-small/5gm.small", "r").readlines()

phrase_coll = defaultdict(list)

for phrase in gram:
	# print phrase
	sentence = phrase[:-1].split()

	if sentence[-2] in data:
		origin = sentence[-2]
		newsentence = sentence[:-1]
		newsentence[-1] = '(some place)'

		for idx in range(0, len(sentence) - 2):
			if sentence[idx] in det:
				newsentence[idx] = ''

		newsentence = [x for x in newsentence if x != ""]

		key = ' '.join(newsentence);

		if len(phrase_coll[key]) == 0:
			phrase_coll[key].append(0)
			phrase_coll[key].append(set())

		phrase_coll[key][0] += int(sentence[-1])
		phrase_coll[key][1].add(origin)

x = sorted(phrase_coll.items(), key=lambda x: x[1], reverse=True)

for (key, value) in x[:1000]:
	f.write(key + '\n')

f.close()