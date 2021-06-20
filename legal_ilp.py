# -*- coding: utf-8 -*-
"""
Created on Thu May  6 10:53:48 2021

@author: Paheli
"""
#!/usr/bin/python3

import sys
from collections import Counter
import re
from gurobipy import *
import gzip
import os
import time
import codecs
import math
import networkx as nx
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic, genesis
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
import argparse
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from itertools import cycle
from operator import itemgetter
import math
import json
from isStatute_isPrecedent import *
from mention_statute_sentence import get_statute_mention
lmtzr = WordNetLemmatizer()
WORD = re.compile(r'\w+')
class keyvalue(argparse.Action):
    # Constructor calling
    def __call__( self , parser, namespace,
                 values, option_string = None):
        setattr(namespace, self.dest, dict())
          
        for value in values:
            # split it into key and value
            key, value = value.split('=')
            # assign into dictionary
            getattr(namespace, self.dest)[key] = int(value)
            

WT1 = 1
WT2 = 1
WT3 = 1
cachedstopwords = stopwords.words("english")
AUX = ['be','can','cannot','could','am','has','had','is','are','may','might','dare','do','did','have','must','need','ought','shall','should','will','would','shud','cud','don\'t','didn\'t','shouldn\'t','couldn\'t','wouldn\'t']
NEGATE = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
              "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
              "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
              "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
              "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
              "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
              "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
              "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]
POS_TAGS = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','PRP','PRP$','RB','RBR','RBS','RP','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']


def get_legal_word(sen,LEG):
    temp = []
    for k in LEG.keys():
        if k in sen.lower() and k not in temp:
            temp.append(k)
    return temp


def compute_summary(args):

    ifname = args.prep_path
    SUMMARY_PATH = args.summary_path
    CLASS_WEIGHT = args.class_weights
    nos = args.class_sents
    
    with open(ifname,'r') as fp:
        dic = json.load(fp)

    for k,v in CLASS_WEIGHT.items():
        print('Weight for class {} is {}'.format(k,v))

    print('Total number of documents:{}'.format(len(dic.keys())))
       
    SUMMARY_LENGTH = {}
    fp = open(args.length_file,'r')
    for l in fp:
        wl = l.split('\t')
        docid = wl[0].strip(' \t\n\r')
        word_length = int(wl[1])
        SUMMARY_LENGTH[docid.replace(".txt","")] = word_length

    fp.close()

    
    LEGALDICT = {}
    fp = open('dict_words.txt','r')
    for l in fp:
        LEGALDICT[l.strip(' \t\n\r').lower()] = 1
    fp.close()

    for k,v in dic.items():
        print('Document ID {}'.format(k))
        t0 = time.time()
        T = {}
        TW = {}
        CT = {}
        index = 0
        content_count = {}
        CLASS_INDEX = 0
        NOS = {}
        MAP = {}
        #Ts = SUMMARY_LENGTH[k][1] #word limit
        Ts = SUMMARY_LENGTH[k]
        #Ts = 2000
        print('Summary Length: {}'.format(Ts))
        
        for ck,cv in v.items():
            CL_WEIGHT = CLASS_WEIGHT[ck]
            NUMBER_OF_SENTENCES = 0
            LENGTH_SEGMENT = 0
            for x in cv:
                #get_statute_mention(x[0].strip(' \t\n\r'))
                #sys.exit(0)
                if len(x[0].split())>4:
                    LENGTH_SEGMENT+=1
            #NOS[CLASS_INDEX] = NUMBER_OF_SENTENCES
            MAP[CLASS_INDEX] = ck
            if nos!=None :
                if ck in nos.keys():
                    NOS[CLASS_INDEX] = nos[ck]
                else:
                    NOS[CLASS_INDEX] = args.default_sents
            else:
                NOS[CLASS_INDEX] = args.default_sents
            #if NUMBER_OF_SENTENCES<2:
            #    print('Problem with document {} and class {} with number of sentences {}'.format(k,ck,NUMBER_OF_SENTENCES))
            #    continue
            position = 1
            for x in cv:
                if len(x[0].split())>4:
                    content = set()
                    All = set()
                    sentence = x[0]
                    L = 0
                    tokens = x[2]
                    SEN_TEMP = ''
                    for y in tokens:
                        if y[1] in POS_TAGS:
                            L+=1
                            All.add(y[0].lower())
                            SEN_TEMP = SEN_TEMP + y[0].lower() + ' '
                        if y[1]=='NN' or y[1]=='NNP':
                            content.add(y[0].lower())
                        elif y[1]=='NNS' or y[1]=='NNPS':
                            try:
                                w = lmtzr.lemmatize(y[0].lower())
                                word = w.lower()
                            except Exception as e:
                                word = y[0].lower()
                            content.add(word)
                        else:
                            pass
                    LEGAL_WORD = get_legal_word(SEN_TEMP.strip(),LEGALDICT)
                    STATUTE_WORD = get_statute_mention(x[0].strip(' \t\n\r'))
                    if STATUTE_WORD : print(STATUTE_WORD)
                    for y in content:
                        content_count[y] = args.content_weight
                    for y in LEGAL_WORD:
                        All.add(y.lower())
                        content.add(y.lower())
                        content_count[y.lower()] = args.legal_weight
                    for y in STATUTE_WORD:
                        All.add(y.lower())
                        content.add(y.lower())
                        content_count[y.lower()] = args.legal_weight
                    KSS = should_select(TW,All)
                    if KSS==1:
                        NUMBER_OF_SENTENCES+=1
                        if ck=='Final Judgement' or ck=='Issue':
                            T[index] = [sentence,content,L,CL_WEIGHT,CLASS_INDEX]
                            TW[index] = All
                            index+=1
                        elif ck=='Fact':
                            T[index] = [sentence,content,L,CL_WEIGHT*(1/position),CLASS_INDEX]
                            TW[index] = All
                            index+=1
                        elif ck=='Statute':
                            ST = isStatute(sentence,'current-acts.txt')
                            T[index] = [sentence,content,L,CL_WEIGHT*ST,CLASS_INDEX]
                            TW[index] = All
                            index+=1
                        elif ck=='Precedent':
                            PR = isPrecedent(sentence)
                            T[index] = [sentence,content,L,CL_WEIGHT*PR,CLASS_INDEX]
                            TW[index] = All
                            index+=1
                        elif ck=='Ratio':
                            PR = isPrecedent(sentence)
                            ST = isStatute(sentence,'current-acts.txt')
                            T[index] = [sentence,content,L,CL_WEIGHT*position,CLASS_INDEX]
                            TW[index] = All
                            index+=1
                        else:
                            T[index] = [sentence,content,L,CL_WEIGHT,CLASS_INDEX]
                            TW[index] = All
                            index+=1
                    position+=1
           
            CLASS_INDEX+=1
	########################################## Summarize Tweets #############################################################

        L = len(T.keys())
        print('Number of tweets: {}'.format(L))
        tweet_cur_window = {}
        for i in range(0,L,1):
            temp = T[i]
            tweet_cur_window[i] = [temp[0].strip(' \t\n\r'),int(temp[2]),temp[1],float(temp[3]),int(temp[4])] # tweet, length, content, score, class
        
        #print(tweet_cur_window[0])

        print('Number of classes: ',CLASS_INDEX)
        print('Sentence Limit: {}'.format(NOS))
        print('Class Mapping: {}'.format(MAP))
        #print(NOS)
        ofname = os.path.join(SUMMARY_PATH,k + '.txt')
        optimize(tweet_cur_window,content_count,ofname,Ts,CLASS_INDEX,NOS)
        t1 = time.time()
        print('Summarization done: ',ofname,' ',t1-t0)
        #sys.exit(0)
                
    print('Done with documents')
    #sys.exit(0)

def should_select(T,new):
    if len(new)==0:
        return 0
    for i in range(0,len(T),1):
        temp = T[i]
        common = set(temp).intersection(set(new))
        if len(common)==len(new):
            return 0
    return 1

def set_weight(P,L,U):
    min_p = min(P.values())
    max_p = max(P.values())

    x = U - L + 4.0 - 4.0
    y = max_p - min_p + 4.0 - 4.0
    factor = round(x/y,4)

    mod_P = {}
    for k,v in P.iteritems():
        val = L + factor * (v - min_p)
        mod_P[k] = round(val,4)

    count = 0
    return mod_P

def optimize(tweet,con_weight,ofname,L,CLASS_INDEX,NOS):

    ################################ Extract Tweets and Content Words ##############################
    con_word = {}
    tweet_word = {}
    tweet_index = 1
    for  k,v in tweet.items():
        set_of_words = v[2]
        for x in set_of_words:
            if con_word.__contains__(x)==False:
                if con_weight.__contains__(x)==True:
                    p1 = round(con_weight[x],4)
                else:
                    p1 = 0.0
                con_word[x] = p1 * WT2
                
        tweet_word[tweet_index] = [v[1],set_of_words,v[0],v[3],v[4]]  #Length of tweet, set of content words present in the tweet, tweet itself, weight, class index
        tweet_index+=1

    ############################### Make a List of Tweets ###########################################
    sen = list(tweet_word.keys())
    sen.sort()
    entities = list(con_word.keys())
    print('Length: ',len(sen),len(entities))

    ################### Define the Model #############################################################

    m = Model("sol1")

    ############ First Add tweet variables ############################################################

    sen_var = []
    for i in range(0,len(sen),1):
        sen_var.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))

    ############ Add entities variables ################################################################

    con_var = []
    for i in range(0,len(entities),1):
        con_var.append(m.addVar(vtype=GRB.BINARY, name="y%d" % (i+1)))
        
    ########### Integrate Variables ####################################################################
    m.update()

    P = LinExpr() # Contains objective function
    C1 = LinExpr()  # Summary Length constraint
    C4 = LinExpr()  # Summary Length constraint
    C2 = [] # If a tweet is selected then the content words are also selected
    counter = -1
    for i in range(0,len(sen),1):
        P += tweet_word[i+1][3] * sen_var[i]
        #C1 += sen_var[i]
        C1 += tweet_word[i+1][0] * sen_var[i]
        v = tweet_word[i+1][1] # Entities present in tweet i+1
        C = LinExpr()
        flag = 0
        for j in range(0,len(entities),1):
            if entities[j] in v:
                flag+=1
                C += con_var[j]
        if flag>0:
            counter+=1
            m.addConstr(C, GRB.GREATER_EQUAL, flag * sen_var[i], "c%d" % (counter))
                
    for i in range(0,len(entities),1):
        P += con_word[entities[i]] * con_var[i]
        C = LinExpr()
        flag = 0
        for j in range(0,len(sen),1):
            v = tweet_word[j+1][1]
            if entities[i] in v:
                flag = 1
                C += sen_var[j]
        if flag==1:
            counter+=1
            m.addConstr(C,GRB.GREATER_EQUAL,con_var[i], "c%d" % (counter))

    ###################### Add class constraint ############################################

    CC = 0
    while CC < CLASS_INDEX:
        C = LinExpr()
        for i in range(0,len(sen),1):
            temp = tweet_word[i+1]
            if temp[4]==CC:
                C += sen_var[i]
        counter+=1
        m.addConstr(C,GRB.GREATER_EQUAL,NOS[CC], "c%d" % (counter))
        CC+=1

    counter+=1
    m.addConstr(C1,GRB.LESS_EQUAL,L, "c%d" % (counter))


    ################ Set Objective Function #################################
    m.setObjective(P, GRB.MAXIMIZE)

    ############### Set Constraints ##########################################

    fo = codecs.open(ofname,'w','utf-8')
    try:
        m.optimize()
        #print('vars: {}'.format(m.getVars()))
        for v in m.getVars():
            if v.x==1:
                temp = v.varName.split('x')
                if len(temp)==2:
                    X = ''
                    fo.write(tweet_word[int(temp[1])][2])
                    fo.write('\n')
    except GurobiError as e:
        print(e)
        sys.exit(0)

    fo.close()

def compute_tfidf_NEW(word,tweet_count,PLACE):
    score = {}
    discard = []
    THR = 5
    N = tweet_count + 4.0 - 4.0
    for k,v in word.iteritems():
        D = k.split('_')
        D_w = D[0].strip(' \t\n\r')
        D_t = D[1].strip(' \t\n\r')
        if D_w not in discard:
            tf = v
            w = 1 + math.log(tf,2)
            df = v + 4.0 - 4.0
            try:
                y = round(N/df,4)
                idf = math.log10(y)
            except Exception as e:
                idf = 0
            val = round(w * idf, 4)
            if D_t=='P' and tf>=THR:
                score[k] = val
            elif tf>=THR and D_t=='S':
                score[k] = val
            elif tf>=THR and len(D_w)>2:
                score[k] = val
            else:
                score[k] = 0
        else:
            score[k] = 0
    return score

def numToWord(number):
    word = []
    if number < 0 or number > 999999:
        return number
        # raise ValueError("You must type a number between 0 and 999999")
    ones = ["","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
    if number == 0: return "zero"
    if number > 9 and number < 20:
        return ones[number]
    tens = ["","ten","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
    word.append(ones[int(str(number)[-1])])
    if number >= 10:
        word.append(tens[int(str(number)[-2])])
    if number >= 100:
        word.append("hundred")
        word.append(ones[int(str(number)[-3])])
    if number >= 1000 and number < 1000000:
        word.append("thousand")
        word.append(numToWord(int(str(number)[:-3])))
    for i,value in enumerate(word):
        if value == '':
            word.pop(i)
    return ' '.join(word[::-1])

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--prep_path',  type = str, help = 'Path where the prepared data is stored in json format')
    parser.add_argument('--summary_path',  type = str, help = 'Folder to store the summaries of the documents')
    parser.add_argument('--length_file', type = str, help = '.txt file containing the required summary lengths <filename>tab<no.of words>')
    parser.add_argument('--class_weights', nargs='*', action = keyvalue, help = 'Weights of each rhetorical segment, e.g. L1=w1 L2=w2 L3=w3')
    parser.add_argument('--content_weight', default = 1, type = int, help = 'Weights for the content words')
    parser.add_argument('--legal_weight', default = 3, type = int, help = 'Weights for the legal words from a dctionary')
    parser.add_argument('--statute_weight', default = 5, type = int, help = 'Weights to words indicating statutes/laws')
    parser.add_argument('--class_sents', nargs='*', action = keyvalue, help = 'Minimum number of sentences to be taken from each rhetorical segment, e.g., L1=n1 L2=n2')
    parser.add_argument('--default_sents', default = 1, type = int, help = 'Default number of sentences to be taken from segments not mentioned in --class_sents e.g. n0')

    
    args = parser.parse_args()
    
    compute_summary(args)
    print('Done')

if __name__=='__main__':
    main()
