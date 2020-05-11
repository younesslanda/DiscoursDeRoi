import pandas as pd 
import os 

class mainClass():

	def __init__(self, Dir, dataDir, column):
		self.dir = Dir
		self.data = pd.read_csv(dataDir)
		self.column = column
		self.index = 0

	def to_files(self):
		for text in self.data[self.column]:
			with open(self.dir+'/'+str(self.index), 'w') as out_file:
				out_file.write(text)
			self.index += 1 
			
	def make_dir(self):
		try:
			os.mkdir(self.dir)
		except OSError:
			pass


if __name__ == '__main__':
	inst = mainClass('Discours_text', 'My_Data.csv', 'Discour')
	inst.make_dir()
	inst.to_files()





