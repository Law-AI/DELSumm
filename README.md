# DELSumm : Incorporating Domain Knowledge for Extractive Summarization of Legal Case Documents

## Introduction
This is the repository for the paper titled "Incorporating Domain Knowledge for Extractive Summarization of Legal Case Documents" accepted at the <a href="https://icail.lawgorithm.com.br/">18th International Conference on Artificial Intelligence and Law (ICAIL) 2021</a>.

DELSumm is an unsupervised extractive legal-domain specific algorithm that can summarize case documents. The input to the algorithm is a case document with each sentence labelled by its rhetorical role (Facts, Issue, Final Judgement, Arguments etc.) and a set of guidelines as to how much representation each rhetorical segment should have in the summary, if the summary is expected to contain statute words more than content words and others (details later) along with the desired summary length. DELSumm outputs a summary that adhres to the above guidelines. Its internal working involves Integer Linear Programming (ILP) based optimization setup. Refer to the paper for details.

## Citation
If you use this dataset or the codes, please refer to the following paper:
```
  @inproceedings{bhattacharya-icail2021,
   author = {Bhattacharya, Paheli and Poddar, Soham and Rudra, Koustav and Ghosh, Kripabandhu and Ghosh, Saptarshi},
   title = {{Incorporating Domain Knowledge for Extractive Summarization of Legal Case Documents}},
   booktitle = {{Proceedings of the 18th International Conference on Artificial Intelligence and Law (ICAIL)}},
   year = {2021}
  }
```

## Requirements
- python = 3.7.3
- nltk = 3.5
- sklearn = 0.21.3
- numpy = 1.17.2
- <a href="https://www.gurobi.com/documentation/9.1/quickstart_mac/cs_using_pip_to_install_gr.html">gurobipy</a>

## Running the Code

### Input data format

The document to be summarized should be represented as an individual text file, with one sentence per line. Each sentence should be assigned a rhetorical label. The format of a sentence in the file is : 
  ```
  text <TAB> label
  ```

### Usage

The code expects the input documents to be in a folder (specified by /path/to/input/documents/)
The code outputs the summaries in a folder (specified by /path/to/store/summaries/)

**Step 1** : Run the **prepareData.py** code with the following command line arguments :
(processes the input documents and stores all of them in a .json file)

``python prepareData.py --data_path /path/to/input/documents/ --prep_path /path/to/prepared_data.json``

data_path : path to the directory where the input documents to be summarized are stored
prep_path : path where the prepared data will be stored as .json


**Step 2** : Run the **legal_ilp.py** code for summarizing the documents with the following command line arguments :

``python legal_ilp.py --prep_path /path/to/prepared_data.json --summary_path /path/to/store/summaries/ --length_file length_file.txt --class_weights L1=w1 L2=w2 L3=w3 --class_sents L1=n1 L2=n2 --default_sents n0 --content_weight c --legal_weight l --statute_weight s``

*class_weights* specified in the format label=weight. Each (label,weights) is separated by space. In the above command line, label L1 has weight w1, label L2 has weight w2 and label L3 has weight w3. [must be specified]

*class_sents* specifed in the format label=no.of sents. Each (label,no.of sents) is separated by space. In the above command line, from label L1 minimum n1 no. of sentences should be present, from label L2 a minimum of n2 no.of sentences should be present. [optional]

If not mentioned, a *default minimum number of sentences*, specified by --default_sents (by default 1, otherwise n0) from each segment is selected in the summary. For example, a mimimum of n0 number of sentences is selected for label L3 (since it is not mentioned in class_sents parameter). [optional]

c, l and s are the weights given to the content, legal and statute/law words respectively. The values are 1,3 and 5 by default. [optional]

*length_file* : must be specified

*format of length_file* : a file containing the summary lengths of the documents to be summarized; each line of the file has the following format : document_name<tab>no.of words in summary

### Demo to run on a sample set of documents

``python prepareData.py --data_path docs/ --prep_path docs/``

``python legal_ilp.py --prep_path docs/prepared_data.json --summary_path summary/ --length_file length_file.txt --class_weights F=2 I=3 RLC=1 A=1 P=1 S=1 R=2 RPC=3 --default_sents 1 --content_weight 1 --legal_weight 1 --statute_weight 2``
