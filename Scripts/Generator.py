import numpy as np
import spacy
import collections
import time
import os


class MyInputGenerator(object):
	
	def __init__(self, dirname, vocab, seq_length, sequences_step, num_epochs, batch_size=1) :
		self.dirname = dirname
		self.batch_size = batch_size
		self.num_epochs = num_epochs
		self.vocab = vocab
		self.vocab_size = len(vocab)
		self.seq_length = seq_length
		self.sequences_step = sequences_step
		self.nlp = spacy.load("fr_core_news_sm")
 
	def __iter__(self):

		for i in range(self.num_epochs):
			for fname in os.listdir(self.dirname)[1:]:
				yield self.__data_generation(fname)


	

	def __data_generation(self, file):
		'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
		# Initialization


		wordlist = self.__wl(file)
			   
		#seq_length, sequences_step = self.__pre_pro(wordlist)

		sequences, next_words = self.__make_arg(self.seq_length, self.sequences_step, wordlist)

		len_s = len(sequences)

		X, y =  self.__init_X_y(len_s, self.seq_length, self.vocab_size)

		X, y = self.__fill_X_y(X, y, sequences, self.vocab, next_words)


		return X, y

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
				


	def __wl(self, file):

				

		# Generate data
				
				with open(self.dirname+'/'+file, 'r') as f:
						 text = f.read()

				doc = self.nlp(text)
				wordlist = self.__create_wordlist(doc)  

				return wordlist  
				

	def __make_arg(self, seq_length, sequences_step, wordlist):
				sequences = []
				next_words = []
				for i in range(0, len(wordlist) - seq_length, sequences_step):
					sequences.append(wordlist[i: i + seq_length])
					next_words.append(wordlist[i + seq_length])

				return sequences, next_words 



	def __init_X_y(self, len_s, seq_length, vocab_size):
				X = np.zeros((len_s, seq_length, vocab_size), dtype=np.bool)
				y = np.zeros((len_s, vocab_size), dtype=np.bool)
				return X, y
				

	def __fill_X_y(self, X, y, sequences, vocab, next_words):
				for i, sentence in enumerate(sequences):
					for t, word in enumerate(sentence):
						X[i, t, vocab[word]] = 1
					y[i, vocab[next_words[i]]] = 1

				return X, y                                               