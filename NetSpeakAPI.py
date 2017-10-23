#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib
import urllib2

class NetSpeak:
    def __init__(self):
        httplib.HTTPConnection.debuglevel = 1
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)')]
        self.page = None

    def __getPageContent(self,url):
        return self.opener.open(url).read()

    def __rolling(self,url,maxfreq):
        webdata = self.__getPageContent(url+"&maxfreq=%s" % maxfreq)
        if webdata:
            Result = [(data2[2],float(data2[1])) for data2 in [data.split("\t") for data in webdata.strip().split("\n")]]
            lastFreq = int(Result[-1][1])
            if lastFreq != maxfreq:
                return Result + self.__rolling(url,lastFreq)
            else:
                return []
        else:
            return []
    
    def __parseWebData(self, rowdata):
        id, count, ngram = rowdata.split("\t")
        return (ngram, float(count))

    def search(self,query):
        queries = query.lower().split()
        new_query = []
        for token in queries:
            if token.count("|") > 0:
                new_query.append("%5B+"+"+".join(token.split("|"))+"+%5D")
            elif token == "*":
                new_query.append("?")
            else:
                new_query.append(token)
        new_query = "+".join(new_query)
        url = "http://api.netspeak.org/netspeak3/search?query=%s" % (new_query.replace(" ","+"))
        webdata = self.__getPageContent(url)
        if webdata:
            # Result = [ (data2[2],float(data2[1])) for data2 in (data.split("\t") for data in webdata.strip().split("\n")) ]
            Result = map(self.__parseWebData, webdata.strip().split("\n"))
            lastFreq = int(Result[-1][1])
            Result += self.__rolling(url,lastFreq)
            return Result
        else:
            return None

if __name__ == "__main__":

    SE = NetSpeak()
    tests = ['when the break is finished'.split()]
    # tests += ['? is finished'.split()]
    # tests += ['brake is finished'.split()]

    for test in tests:
        for i in range(len(test) - 2):
            res = SE.search(' '.join(test[i:i+3]))
            if res:
                print '\n'.join( '\t'.join( str(y) for y in x ) for x in res )
            else:
                print ' '.join(test[i:i+3]) + '\tnot found'
        print
