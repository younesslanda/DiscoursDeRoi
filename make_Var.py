import os
import spacy
import numpy as np
import pandas as pd
import collections
from six.moves import cPickle

wordlist = []

nlp = spacy.load("fr_core_news_sm")
df = pd.read_csv("My_Data.csv")

def create_wordlist(doc):
    wl = []
    nw = ['\n\xa0',
 			'\n\xa0\n',
 			'\n\xa0\n\xa0\n',
 			'\n\xa0\n\xa0\n\xa0\n\xa0\n',
 			'\n\xa0 ',
 			'\n\xa0 \xa0',
 			'\n\xa0\xa0 ',
 			'\n\xa0\xa0\xa0 ',
 			'\n\xa0\xa0\xa0\xa0 ',
 			'\n\xa0\xa0\xa0\xa0\xa0 ',
 			'\x1c',"\n","\n\n",'\u2009','\xa0','\xa0 ']
    
    for word in doc:
        if word.text not in nw:
            wl.append(word.text.lower())
    return wl


for text in df["Discour"]:
    doc = nlp(text)
    wl = create_wordlist(doc)
    wordlist = wordlist+wl

word_counts = collections.Counter(wordlist)
vocabulary_inv = list(sorted(list(word_counts.keys())))

vocab = {x: i for i, x in enumerate(vocabulary_inv)}
words = [x[0] for x in word_counts.most_common()]

with open(os.path.join("pkl_files/words_vocab.pkl"), 'wb') as f:
    cPickle.dump((words, vocab, vocabulary_inv), f, -1)    


#create sequences
seq_length = 30
sequences_step = 1
vocab_size = len(words)


sequences = []
next_words = []
for i in range(0, len(wordlist) - seq_length, sequences_step):
    sequences.append(wordlist[i: i + seq_length])
    next_words.append(wordlist[i + seq_length])


with open(os.path.join("pkl_files/RNN_arg.pkl"), 'wb') as f:
    cPickle.dump((sequences, next_words), f, -1)    


print("**************** DONE ****************")    
