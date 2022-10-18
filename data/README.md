# Introduction

This folder contains dataset of the paper *Incorporating Domain Knowledge for Extractive Summarization of Legal Case Documents* accepted at ICAIL 2021.

The dataset contains 50 Indian Supreme Court case documents and their extractive summaries. 


The "judgement" folder contains the full text documents. The format of a full text document is as follows :

sentence<TAB>label

label implies one of the following rhetorical labels :
F : facts, RLC : Ruling by Lower Court, A : Arguments, P : Precedent, S : Statute, R : Ratio of the decision, RPC : Ruling by Present Court/Final judgement.

The "summary" folder contains summaries of the judgements.

For each document, there are two summaries written individually by two law experts A1 and A2. Each summary by each law expert is of two types : full & segment-wise.


"full" : a coherent piece of summary.

"segment-wise" : the following segments are considered -- 'analysis', 'argument', 'facts', 'judgement', 'statute'. A "full" summary is broken down into these segments. Each segment is a folder.
For a particular document, appending the "segment-wise" summaries results in a "full" summary. 

As an example, consider the document 1953_L_1.txt. We have the full text of the document in the "judgement" folder. The "summary" folder contains two sub-folders "full" and "segment-wise". Under each subfolder, there are two subfolders "A1" and "A2" .

summary/full/A1/1953_L_1.txt --> contains the full summary of 1953_L_1.txt written by A1.

summary/full/A2/1953_L_1.txt --> contains the full summary of 1953_L_1.txt written by A2.

summary/segment-wise/A1/analysis/1953_L_1.txt --> "analysis" segment of the summary written by A1

summary/segment-wise/A1/argument/1953_L_1.txt -->  "argument" segment of the summary written by A1

summary/segment-wise/A1/facts/1953_L_1.txt -->  "facts" segment of the summary written by A1

summary/segment-wise/A1/judgement/1953_L_1.txt -->  "judgement" segment of the summary written by A1

summary/segment-wise/A1/statute/1953_L_1.txt -->  "statute" segment of the summary written by A1

summary/segment-wise/A2/analysis/1953_L_1.txt --> "analysis" segment of the summary written by A2

summary/segment-wise/A2/argument/1953_L_1.txt -->  "argument" segment of the summary written by A2

summary/segment-wise/A2/facts/1953_L_1.txt -->  "facts" segment of the summary written by A2

summary/segment-wise/A2/judgement/1953_L_1.txt -->  "judgement" segment of the summary written by A2

summary/segment-wise/A2/statute/1953_L_1.txt -->  "statute" segment of the summary written by A2

The directory structure is as follows :


    .
    ├── judgement                 # folder contains documents           
    ├── summary    
    │   ├── full                  # folder contains full summaries
    │   │   ├── A1
    │   │   ├── A2
    │   ├── segment-wise          # folder contains segment-wise summaries
    │   │   ├── A1
    │   │   ├── A2
    ├── IN-EXT-length.txt   # text file containing the word and sentence count statistics of the documents
    
The format of the IN-EXT-length.txt file is :

```
filename <TAB> #words in summary
```
