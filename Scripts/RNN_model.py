import os
from six.moves import cPickle
from Generator import MyInputGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, Input, Bidirectional
from keras.optimizers import Adam
from keras.metrics import categorical_accuracy



class RNN_Model(object):

	"""docstring for Model"""
	def __init__(self, rnn_size, batch_size,
						 num_epochs, learning_rate, steps_per_epoch
						 ,seq_length, vocab_size, sequences_step, modelDir, modelName = 'md' ):

				self.rnn_size = rnn_size
				self.batch_size = batch_size
				self.num_epochs = num_epochs
				self.learning_rate = learning_rate
				self.steps_per_epoch = steps_per_epoch
				self.seq_length = seq_length
				self.vocab_size = vocab_size
				self.sequences_step = sequences_step
				self.modelDir = modelDir
				self.modelName = modelName
				self.md = self.Create_model()


	def __bidirectional_lstm_model(self, rnn_size, seq_length, vocab_size,learning_rate):
	    print('Build LSTM model.')
	    model = Sequential()
	    model.add(Bidirectional(LSTM(rnn_size, activation="relu"),input_shape=(seq_length, vocab_size)))
	    model.add(Dropout(0.6))
	    model.add(Dense(vocab_size))
	    model.add(Activation('softmax'))
	    
	    optimizer = Adam(lr=learning_rate)
	    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
	    print("model built!")

	    return model

	def Create_model(self):
		return bidirectional_lstm_model(self.rnn_size, self.seq_length,
												 self.vocab_size, self.learning_rate)

	def __input_generator(self):
		
		global vocab
		Generator = MyInputGenerator('../Discours_text/', vocab, self.seq_length,
											 self.sequences_step, self.num_epochs, 
											 batch_size = self.batch_size)
		Generator = Generator.__iter__()
		return Generator


	def train(self):

		Generator = self.__input_generator()

		history = self.md.fit(Generator,
                 				batch_size = None,
                 				shuffle = True,
                				epochs = self.num_epochs,
                 				steps_per_epoch = self.steps_per_epoch)  

	def save(self):
		self.md.save(os.path.join(self.modelDir, self.modelName+'.h5'))




if __name__ == '__main__':

			with open('../pkl_files/words_vocab_v2.pkl', 'rb') as f:
			data = cPickle.load(f)

			words, vocab, seq_length, sequences_step, vocab_size  = data

			rnn_size = 256 # size of RNN
			batch_size = 32 # minibatch size
			num_epochs = 3 # number of epochs
			learning_rate = 0.001 #learning rate
			steps_per_epoch = len(os.listdir('../Discours_text/'))


			params = {'rnn_size':rnn_size,
						 	'batch_size': batch_size,
						 	'num_epochs': num_epochs,
						 	'learning_rate': learning_rate,
						 	'steps_per_epoch':steps_per_epoch,
							'seq_length':seq_length,
							'vocab_size':vocab_size,
							'sequences_step':sequences_step,
							'modelDir': '../Models/'}


			RNN_Model = RNN_Model(params)
			RNN_Model.train()
			RNN_Model.save()

