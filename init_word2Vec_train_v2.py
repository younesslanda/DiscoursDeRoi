import make_corpus
import os 
import gensim


class MySentences(object):
	
	def __init__(self, dirname):
		self.dirname = dirname
 
	def __iter__(self):
		for fname in os.listdir(self.dirname):
			with open(os.path.join(self.dirname,fname) , 'r', errors='ignore') as f:
				txt = f.read()
			l =  make_corpus.preprocessing(txt)
			for line in l:
				yield line.split()


if __name__ == '__main__':
	sentence = MySentences('./Discours_text/')
	model = gensim.models.Word2Vec(sentence, min_count=3)
	model.save('./discour_de_roi_model_v2')