# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:47:19 2021

@author: Paheli
"""
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:05:13 2021

@author: Paheli
"""
import re
import string
import os
from tqdm import tqdm

all_acts = open("current-acts.txt","r")
actlist = set()
tokens = {}
for line in all_acts.readlines():
        line = line.rstrip("\n")
        a = []
        line = line.translate(str.maketrans('', '', string.punctuation.replace(",","")))  # remove punctuation from a line
        #print(line)
        if line != "Constitution of India 1950":
            a.append(line)
            new = line[:line.rindex(" ")]
            a.append(new)
            #new = line[:line.rindex(" ")+1]+line[line.rindex(" ")+2:]
            #a.append(new)
            tokens[line] = a
            
            actlist.add(line)
tokens["Constitution of India, 1950"] = ["Constitution of India, 1950", "Constitution of India", "Constitution"]

tokens["Code of Criminal Procedure, 1898"] = ["Code of Criminal Procedure, 1898","Criminal Procedure Code, 1898", "Cr.PC, 1898", "Cr.P.C., 1898"\
    "Criminal Procedure Code, 1898", "Cr.PC, 1898", "Cr.P.C., 1898", "Cr.P.C", "Cr.P.C.", "Cr.PC", "Criminal Procedure Code"]
    
tokens["Code of Criminal Procedure, 1973"] = ["Code of Criminal Procedure, 1973","Criminal Procedure Code, 1973", "Cr.PC, 1973", "Cr.P.C., 1973"\
    "Criminal Procedure Code, 1973", "Cr.PC, 1973", "Cr.P.C., 1973"]
    
tokens["Code of Civil Procedure, 1908"] = ["Code of Civil Procedure, 1908","Code of Civil Procedure", "Civil Procedure Code", \
        "Code of Civil Procedure", "Civil Procedure Code","CPC","C.P.C","civil procedure code"]
    
tokens["Indian Penal Code, 1860"] = ["Indian Penal Code, 1860","Indian Penal Code"',', "Penal Code"',', "IPC"',', "IPC"',', "I.P.C"',', "I.P.C"',',\
        "I.P.C."',', "I.P.C."',', "I. P. C.","penal code"]

    
abbrv = {"s.": "section", "ss.": "section", "art.": "article", "arts.": "article"}



name1 = "article"
name2 = "articles"
name3 = "section"
name4 = "sections"


def get_statute_mention(line):
    answer = set()
    line = line.rstrip("\n")
    #line,lab = line.split("$$$")
    text = line
    flag = 0
    #for act in actlist:
    for name,variations in tokens.items():
        for var in variations:
            if var and var in text:
                #flag = 1
                #text = text.replace(var,name)
                
                act = var
                if "of the "+act in text:
                    act = "of the "+act
                if "of "+act in text:
                    act = "of "+act
                
                #print(text+"  ====  "+act)
                
                if "u/" in text:
                    text = text.replace("u/","under ")
                    matched = []
                    for a in abbrv.keys():
                        if re.search(rf".*{a}.*", text):
                            matched.append(a)
                    #true = ""
                    if matched:
                        true = matched[0]
                        big = len(matched[0])
                        for m in matched:
                            if len(m)>big:
                                true = m
                                big = len(m)
                            
                        ff = abbrv[true]
                
                if "constitution" in act:
                    if name1 in text  and name2 not in text:
                        reg = re.compile(rf"{name1}\s(.*?)\s{act}")
                        
                        matchResult = reg.search(text)
                        if matchResult:
                            #print(name1+" "+matchResult.group(1)+" "+act)
                            a = name1+" "+matchResult.group(1)+" "+act
                            if (len(a.split(" "))<50):
                                #fw.write(file+"\t"+line+"\t"+lab+"\t"+a+"\t"+str(len(a.split(" ")))+"\n")
                                answer.add(a)
                        
                    elif name2 in text:
                        reg = re.compile(rf"{name2}\s(.*?)\s{act}")
                        matchResult = reg.search(text)
                        if matchResult:
                            #print(name2+" "+matchResult.group(1)+" "+act)
                            a = (name2+" "+matchResult.group(1)+" "+act)
                            if (len(a.split(" "))<50):
                                #fw.write(file+"\t"+line+"\t"+lab+"\t"+a+"\t"+str(len(a.split(" ")))+"\n")
                                answer.add(a)
                        #print(reg.findall(text))
                         #text = re.sub(rf"{name2}\s(.*?)\s{act}","ACT",text)
                   
                else:
                    if name3 in text and name4 not in text:  
                        reg = re.compile(rf"{name3}\s(.*?)\s{act}")
                        matchResult = reg.search(text)
                        if matchResult:
                             #print(name3+" "+matchResult.group(1)+" "+act)
                             a = (name3+" "+matchResult.group(1)+" "+act)
                             if (len(a.split(" "))<50):
                                 #fw.write(file+"\t"+line+"\t"+lab+"\t"+a+"\t"+str(len(a.split(" ")))+"\n")
                                 answer.add(a)
                        #print(reg.findall(text))
                        #text = re.sub(rf"{name3}\s(.*?)\s{act}","ACT",text)
                    elif name4 in text:
                         reg = re.compile(rf"{name4}\s(.*?)\s{act}")
                         matchResult = reg.search(text)
                         if matchResult:
                             #print(name4+" "+matchResult.group(1)+" "+act)
                             a = (name4+" "+matchResult.group(1)+" "+act)
                             if (len(a.split(" "))<50):
                                 answer.add(a)
                             #    fw.write(file+"\t"+line+"\t"+lab+"\t"+a+"\t"+str(len(a.split(" ")))+"\n")
                             
    return answer