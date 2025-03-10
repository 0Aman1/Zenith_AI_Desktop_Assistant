__author__ = 'schinnasamy'
import pickle
import os
from django.conf import settings
from urlparse import urljoin
#from django.conf.settings import PROJECT_ROOT

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
path=PROJECT_ROOT+'/Lookup_data_new_v2.pickle'
path=path.replace('\\','/')

with open(path, 'r') as f:
    lookup_model = pickle.load(f)


def Scan(text, tag):
    # print text
    mNgramLst = lookup_model[0]
    mUnigramLst = lookup_model[1]

    Punc_For_Split = [',', '.', ':', '\t', '-']
    for pun in Punc_For_Split:
        text = text.replace(pun, " %s " % pun)
    # print text
    tmpTokens = text.split(" ")
    # track=0
    MatchedString = ""
    for i in range(0, len(tmpTokens)):
        if tmpTokens[i].lower() in mUnigramLst[tag]:
            if not MatchedString:
                list_c = mUnigramLst[tag][tmpTokens[i].lower()]
                List_f = {x: list_c.count(x) for x in list_c}
                list_s = List_f.keys()
                list_r = reversed(list_s)
                for j in list_r:
                    if len(tmpTokens[i:]) >= j:
                        valid_con = " ".join(tmpTokens[i:j + i])
                        if valid_con.lower() in mNgramLst[tag]:
                            MatchedString = valid_con
                            break


    return MatchedString
