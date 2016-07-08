# Created by Phayate
# 5216C024-2
# This script is origin and PUBLIC

import re,io,os.path,os,time,csv
from math import log
import treetaggerwrapper
import cy_ex01 as cyex
hd = os.environ["HOME"]
GREEN = '\033[32m'
ENDC = '\033[0m'

# Remove tag
def remove_tag(str):
    alldigit = re.compile(r"^<.+")
    if alldigit.search(str) != None:
        return False
    return True

# This module executes Morphological analysis
def extract_none(line, tagger):
    words = []
    try:
        tags = tagger.TagText(line)
        for tag in tags:
            list = tag.split("\t")
            # ports of speech
            pos = list[1]
            if pos == 'NN':
                words.append(list[0])
            elif pos == 'NP':
                words.append(list[0])
            # If noun is pluralform...
            elif pos == 'NNS':
                if list[2] != u'<unknown>':
                    words.append(list[2])    # original form
            elif pos == 'NPS':
                if list[2] != u'<unknown>':
                    words.append(list[2])    # original form
    except:
        print line + " couldn't translate because invalid character"
    return words


def create_coupus(is_only_noun):
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR=hd +'/Documents/Tigger')
    coupus = []
    filenames = []
    doc_number = 0
    for line in open('./../text_list', "r"):
        filenames.append( line.rstrip() )
        doc_number += 1
        filename = './../TXT/tragedies/'+line.rstrip()
        print filename
        doc = []
        for line in io.open(filename,"r", encoding="utf-16"):
            if remove_tag(line):
                # remove signiture
                line = re.sub( re.compile("[!-/:-@[-`{-~;?]"), "" , line ).rstrip()
                # Line is converted to list
                if len(line) == 0:
                    pass
                elif is_only_noun:
                    # Morphological analysis
                    ws = extract_none(line, tagger)
                    if len(ws) != 0:
                        doc += ws
                else:
                    # Just convert to list
                    doc += line.split()
        if len(doc) != 0:
            coupus.append(doc)
    return coupus, filenames

def circulate_tfidf(word, docs):
    D= 0
    tfs = []
    for doc in docs:
        #  count frequency
        tf = doc.count(word)
        tfs.append(tf)
        if word in doc:
            D += 1
    return tfs, D

def circulate_idf(word, docs):
    nj = 0
    D = 0
    for doc in docs:
        D += 1
        if word in doc:
            nj += 1
    return log(1.0*D / nj)

def circulate_all_tfidf(filenames, coupus):
    for(filename, doc) in zip(filenames, coupus):
        print '\n' + GREEN + filename + ENDC

        #  to unique
        li_uniq = list(set(doc))
        # count frequency
        dict = {}
        for word in li_uniq:
            dict[word.encode('utf-8')] = doc.count(word) * circulate_idf(word, coupus)
        # sort dictionary to list
        d = sorted(dict.items(), key=lambda x:x[1], reverse=True)
        # print key and value of the top 5
        for k in d[0:5]:
            print k

if __name__ == '__main__':
    start = time.time()
    coupus, filenames = create_coupus(True)
    elapsed_time = time.time() - start
    print ("coupus_time: {0}".format(elapsed_time)) + "[sec]"

    with open('coupus.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(coupus)

    D = len(filenames)
    print 'NUMBER OF DOCUMENT: ' + str(D)

    print "\n\n\n###Julius start!!!###"
    tfs, nj = circulate_tfidf("Julius", coupus)
    if nj != 0:
        idf = log(1.0*D / nj)
    else:
        print 'That keyword has not occurred.'
        idf = 0
    print 'IDF: ' + str(idf)
    for (filename,tf) in zip(filenames, tfs):
        print 'file: ' + GREEN + filename.rstrip() + ENDC
        print 'tf: ' + str(tf) + '  tf-idf: ' + str(tf*idf)

    print "\n\n\n###Burutas start!!!###"
    tfs, nj = circulate_tfidf("Brutus", coupus)
    if nj != 0:
        idf = log(1.0*D / nj)
    else:
        print 'That keyword has not occurred.'
        idf = 0
    print 'IDF: ' + str(idf)
    for (filename,tf) in zip(filenames, tfs):
        print 'file: ' + GREEN + filename.rstrip() + ENDC
        print 'tf: ' + str(tf) + '  tf-idf: ' + str(tf*idf)

    # Extra study
    circulate_all_tfidf(filenames,coupus)

    elapsed_time = time.time() - start
    print ("elapsed_time: {0}".format(elapsed_time)) + "[sec]"
