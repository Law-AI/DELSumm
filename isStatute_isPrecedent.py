# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 11:19:18 2020

@author: Paheli
"""
import codecs

def isStatute(sentence,actlist):
    fr = codecs.open(actlist,"r",'utf-8')
    acts = set()
    
    for line in fr.readlines():
        line = line.rstrip("\n")
        line = line.lower()
        act1 = line
        ls = line.rsplit(" ",1)
        act2 = ls[0]
        acts.add(act1)
        acts.add(act2)
        
    acts.add("of the act")
    acts.add("of act")
    acts.add("under Act")
    acts.add("under the Act")
    acts.add("of the said act")
    acts.add("under the said Act")


    
    flag = 0
    for act in acts:
        if act.lower() in sentence.lower():
            flag = 1
            break
    
    return flag


def isPrecedent(sentence):
    if "indlaw sc" in sentence.lower() or " v " in sentence.lower():
        return 1
    else:
        return 0
    
    
#sentence = "1. Three civil appeals, stemming from three revision petitions to the High Court of Orissa under the Orissa Estates Abolition Act, 1951 (Orissa Act I of 1952) (for short, the Act) have reached this Court, thanks to special leave granted to the appellant, who is common in all the cases. The High Court, after deciding various issues, remanded the cases to the Compensation Officer under the Act, after over-ruling most of the contentions pressed before it by the appellant."
#actlist = "current-acts.txt"
#print(isStatute(sentence,actlist))


#sentence = "financial capacity of the appellant, the Tribunal followed Unichem Laboratories v. Their Workmen 1972 Indlaw SC 18(1) where it was held that the gross profits should be computed without making deductions on account of taxation, development rebate and depreciation. "
#print(isPrecedent(sentence))
           
