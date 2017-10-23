import linggle_api
import NetSpeakAPI
from itertools import *
from collections import defaultdict, Counter
import BncTagger
import re
all_classify = {'direction', 'period of time', 'doing something', 'some amount', 'somehow', 'someone', 'some place', 'something', 'sometime', 'so/sth', 'so', 'sth'}

classify = {'some place'}

other_classify = all_classify - classify

print other_classify
det = ['your', 'an', 'all', 'more', 'we','which', 'their', 'our', 'other', 'they', 'my', 'any', 'his', 'her', 'no', 'its', 'what', 'some', 'us', 'these', 'them', 'such', 'most', 'said', 'each', 'a', 'the']

punc = {'.', ',', ':', ';', '!', '?', '-', '(', '[', '{', '...'}

idx = defaultdict(lambda: [])
inverted_idx = defaultdict(lambda: defaultdict(int))


def stringCMP(query, newstring):
	ptr1 = 0
	ptr2 = 0
	ans = ""
	flag = False
	if ' '.join(query) == 'cross from ?det. n. * to ?det. n. *': flag = True
	while True:
		if ptr1 >= len(query) or ptr2 >=len(newstring): break
		#if flag:
			#print query[ptr1], newstring[ptr2]
			#raw_input()
		if query[ptr1] == '?det.':
			if newstring[ptr2] in det:
				ptr1 += 1
				ptr2 += 1
			else:
				ptr1 += 1

		elif query[ptr1] == 'n.':
			#print 'n.: ', newstring[ptr2]
			poss = BncTagger.search_tag(newstring[ptr2])

			for pos in poss:
				if pos[0] == 'n' and pos[1] > 0.5:
					ans = newstring[ptr2]

			#print 'ans: ', ans
			ptr1+=1
			ptr2+=1
			#flag = True

		elif query[ptr1] == '*':
			container = []
			if ptr1 == len(query)-1:
				ptr1 += 1
				container = newstring[ptr2:]
			else:

				while query[ptr1+1] != newstring[ptr2]:
					if ptr2 == len(newstring)-1: break
					container.append(newstring[ptr2])
					ptr2 += 1
				ptr1 += 1
			if len(container):
				newWord = ""
				for x in container:
					tag = BncTagger.search_tag(x)
					for pos in tag:
						if pos[0] == 'n' and pos[1] > 0.5:
							newWord = x
						else: break

				if not newWord == "":
					ans = newWord

		elif query[ptr1] == newstring[ptr2]:
			ptr1+=1
			ptr2+=1
		else: 
			break;


	return ans


#SE = NetSpeakAPI.NetSpeak()

noun = Counter()

data = open("MHDAI.index2.txt").readlines()
cnt = 0
for line in data:
	line = line[:-1]
	word = line.split()[0]
	sentence = ' '.join(line.split()[1:])
	#print sentence
	for cls in classify:
		if cls in sentence:
			print cnt, sentence
			cnt += 1
			parenthesis = sentence[sentence.find("(")+1:sentence.find(")")] if sentence.find("(") != -1 else None

			sentence_list = []

			if parenthesis != None:
				flag = 0
				for clss in classify:
					if clss in parenthesis:
						sentence = (sentence[:sentence.find("(")] + sentence[sentence.find("(")+1:sentence.find(")")] + sentence[sentence.find(")") + 1:]).strip()
						sentence_list.append(sentence)
						flag = 1
						break
				

				if flag == 0:		
					for clss in other_classify:
						if clss in parenthesis:
							sentence = (sentence[:sentence.find("(")] + sentence[sentence.find(")")+1:]).strip()
							sentence_list.append(sentence)
							flag = 1
							break

				if flag == 0:
					sentence_list.append((sentence[:sentence.find("(")] + sentence[sentence.find(")")+1:]).strip())
					sentence_list.append((sentence[:sentence.find("(")] + sentence[sentence.find("(")+1:sentence.find(")")] + sentence[sentence.find(")") + 1:]).strip())

			else:
				sentence_list.append(sentence)


			for sent in sentence_list:
				query = sent.replace(cls, '?det. n. *')

				num_list = [ i for i, d in enumerate(query.split()) if 'n.' in d ]
				res = linggle_api.linggleit(query)

				flag =0 
				if res == None: continue
				for (sen, (times, percent)) in res:
					if '<' in percent: continue
					flag = 1
					ans = stringCMP(query.split(), sen.split())
					noun[ans] += 1
				if flag == 1:
					pass

f = open("place.txt", "w")
for (word, cnt) in noun.most_common(161):
	f.write(word + "\n")


