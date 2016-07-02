import re,io,os.path,os
from math import log
GREEN = '\033[32m'
ENDC = '\033[0m'

def remove_tag(str):
    alldigit = re.compile(r"^<.+")
    if alldigit.search(str) != None:
        return False
    return True

def create_coupus():
    # coupus = ""
    coupus = []
    filenames = []
    doc_number = 0
    for line in open('./../text_list', "r"):
        filenames.append( line.rstrip() )
        doc_number += 1
        filename = './../TXT/tragedies/'+line.rstrip()
        # print filename
        doc = []
        for line in io.open(filename,"r", encoding="utf-16"):
            if remove_tag(line):
                # remove signiture
                line = re.sub( re.compile("[!-/:-@[-`{-~;?]"), "" , line ).rstrip()
                doc += line.split()
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
    coupus, filenames = create_coupus()
    D = len(filenames)
    print 'DOCUMENT NUMBER: ' + str(D)

    # Julius
    tfs, nj = circulate_tfidf("Julius", coupus)
    idf = log(1.0*D / nj)
    print nj
    print 'IDF: ' + str(idf)
    for (filename,tf) in zip(filenames, tfs):
        print 'file: ' + GREEN + filename.rstrip() + ENDC
        print 'tf: ' + str(tf) + '  tf-idf: ' + str(tf*idf)

    # Brutus
    tfs, nj = circulate_tfidf("Brutus", coupus)
    idf = log(1.0*D / nj)
    print nj
    print 'IDF: ' + str(idf)
    for (filename,tf) in zip(filenames, tfs):
        print 'file: ' + GREEN + filename.rstrip() + ENDC
        print 'tf: ' + str(tf) + '  tf-idf: ' + str(tf*idf)


    # Extra study
    circulate_all_tfidf(filenames,coupus)
