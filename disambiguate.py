#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

import re, itertools

def sim(x, y):
  return x.wup_similarity(y)

def wordSim(word1, word2, pos):
  simi = [ x.wup_similarity(y) for x in wn.synsets(word1, pos) for y in wn.synsets(word2, pos) ] 
  return max(simi) if simi else 0.0

def mostInfoSubsumer(word1, word2, pos):
    res = []
    for syn1 in wn.synsets(word1, pos):
        for syn2 in wn.synsets(word2, pos):
            res += syn1.lowest_common_hypernyms(syn2)
    if res:
        return max([(s.min_depth(), s) for s in res])[1]
    else:
        return None

def disambGroup(words, senses, pos):

    normalization = [ 0.0 for w in words ]
    support = [ [ 0.0 for syn in wn.synsets(w, pos) ] for w in words ] 
    phi = [ [ 0.0 for syn in wn.synsets(w, pos) ] for w in words ]
     
    num_senses = [ len(support[i]) for i, w in enumerate(words) ]
    #print v
    #print c

    for i,j in itertools.product(range(len(words)), range(len(words))):
        if i >= j:
            continue
        
        cij = mostInfoSubsumer(words[i], words[j], pos)
        vij = wordSim(words[i], words[j], pos)
            
        for k in range(len(senses[i])):
            if cij and cij in senses[i][k].hypernym_paths()[0]:
                try:
                    support[i][k] += vij
                except:
                    pass
        for k2 in range(len(senses[j])):
            if cij and cij in senses[j][k2].hypernym_paths()[0]:
                try:
                    support[j][k2] += vij
                except:
                    pass
        try:
                normalization[i] += vij
                normalization[j] += vij
        except:
                pass
            

    for i, wi in enumerate(words):
        for k in range(len(phi[i])):
            if (normalization[i] > 0.0):
                phi[i][k] = support[i][k] / normalization[i]
            else:
                phi[i][k] = 1. / num_senses[i]

    res = []
    for i, wordSenseScore in enumerate(phi):
        cands = [ (score, senses[i][j]) for j, score in enumerate(wordSenseScore) ]
        if cands:
            sense = max(cands)
            res += [ (words[i], sense[1], sense[0]) ]
    
    return res

if __name__ == '__main__':

    pos = 'n'
    group = ('minor, child, human, health, people, woman, society, juvenile, person, public, fetus, skin, individual, country').split(', ')
    group = [ x.replace(' ', '_') for x in group ]
    senses =  [ wn.synsets(group[i], pos) for i in range(len(group)) ]
    for word, syn, prob in disambGroup(group, senses, pos):
        print '%s %s:\t[%s]\t%s (%5.3f)' % ('-', word, syn.lexname()[5:], syn.definition(), prob)
