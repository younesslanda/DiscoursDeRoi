import os
import spacy
import numpy as np
import pandas as pd
import collections
from six.moves import cPickle



class make_var(object):
	"""docstring for make_var"""
	def __init__(self, Dir, seq_length, sequences_step):

		self.df = pd.read_csv("My_Data.csv")
		self.nlp = spacy.load("fr_core_news_sm")
		self.Dir = Dir
		self.sequences_step = sequences_step
		self.seq_length = seq_length
		self.wordlist = []
		
	def __create_wordlist(self, doc):
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

	def main(self):
		for fname in os.listdir(self.Dir):
			with open(os.path.join(self.Dir,fname) , 'r', errors='ignore') as f:
				txt = f.read()
			doc = self.nlp(txt)
			self.wordlist = self.wordlist+self.__create_wordlist(doc)

		word_counts = collections.Counter(self.wordlist)
		vocabulary_inv = list(sorted(list(word_counts.keys()))) 
		vocabulary_inv = vocabulary_inv[9:]

		vocab = {x: i for i, x in enumerate(vocabulary_inv)}
		words = [x[0] for x in word_counts.most_common()]

		vocab_size = len(words)

		return words, vocab, self.seq_length, self.sequences_step, vocab_size
	


if __name__ == '__main__':
	
	obj = make_var('./Discours_text/',30, 1)   
	var = obj.main()
	
	with open(os.path.join("pkl_files/words_vocab_v2.pkl"), 'wb') as f:
		cPickle.dump(var, f)    


  
