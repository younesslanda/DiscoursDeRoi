import gensim
import os

class MySentences(object):
    
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()
  

if __name__ == '__main__':
	
	sentences = MySentences('./Word2Vec_input/') # a memory-friendly iterator
	model = gensim.models.Word2Vec(sentences)

	model.save('./discour_de_roi_model')

