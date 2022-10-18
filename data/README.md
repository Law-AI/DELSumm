# Introduction

This folder contains dataset of the paper *Incorporating Domain Knowledge for Extractive Summarization of Legal Case Documents* accepted at ICAIL 2021. The dataset contains 50 Indian Supreme Court case documents and their extractive summaries. 

The "judgement" folder contains the full text documents. The format of a full text document is as follows :

```
sentence<TAB>label
```

*label* implies one of the following rhetorical labels :

F : facts, RLC : Ruling by Lower Court, A : Arguments, P : Precedent, S : Statute, R : Ratio of the decision, RPC : Ruling by Present Court/Final judgement.

The "summary" folder contains summaries of the judgements. For each document, there are two summaries written individually by two law experts A1 and A2. 

As an example, consider the document 1953_L_1.txt. We have the full text of the document in the "judgement" folder. The "summary" folder two subfolders "A1" and "A2" .

- judgement/1953_L_1.txt --> contains the judgement document 1953_L_1.txt 

- summary/full/A1/1953_L_1.txt --> contains the summary of 1953_L_1.txt written by A1.

- summary/full/A2/1953_L_1.txt --> contains the summary of 1953_L_1.txt written by A2.


Each summary has the following sections -- 'analysis', 'argument', 'facts', 'judgement', 'statute'. 


The directory structure is as follows :


    .
    ├── judgement                 # folder contains documents           
    ├── summary    
    │   ├── A1                    # folder contains summaries by A1         
    │   ├── A2                    # folder contains summaries by A1
    ├── IN-EXT-length.txt   # text file containing the word and sentence count statistics of the documents
    
The format of the IN-EXT-length.txt file is :

```
filename <TAB> #words in summary
```
