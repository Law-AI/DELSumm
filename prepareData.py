#!/usr/bin/python3
import argparse

import sys, os
import nltk
import json

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type = str, help = 'Folder containing documents to be summarized')
parser.add_argument('--prep_path',  type = str, help = 'Path to store the prepared data in json format')


args = parser.parse_args()

BASEPATH = args.data_path
writepath = args.prep_path


separator = "\t"

FILES = []
FILES2 = os.listdir(BASEPATH)
for f in FILES2:
        FILES.append(f)
DATA_FILES = {}
for F in FILES:
    ifname = os.path.join(BASEPATH,F)
    
    #print(F)
    fp = open(ifname,'r')
    dic = {}
    for l in fp:
        try:
            wl = l.split(separator)
            CL = wl[1].strip(' \t\n\r')
            TEXT = wl[0].strip(' \t\n\r')
            TEXT = TEXT.replace("sino noindex makedatabase footer start url", "")
            if TEXT:
                if dic.__contains__(CL)==True:
                    temp = dic[CL]
                    temp.append(TEXT)
                    dic[CL] = temp
                else:
                    dic[CL] = [TEXT]
        except Exception as e:
            print(e)
    
    f_d = {}
    for cl,sentences in dic.items():
        temp = []
        for s in sentences:
            tokens = nltk.word_tokenize(s)
            t = (s,tokens,nltk.pos_tag(tokens))
            temp.append(t)
        f_d[cl] = temp

    DATA_FILES[F.split('.txt')[0].strip(' \t\n\r')] = f_d
    print('Complete {}'.format(F))

with open(writepath+'prepared_data.json','w') as legal_f:
    json.dump(DATA_FILES,legal_f,indent=4)
