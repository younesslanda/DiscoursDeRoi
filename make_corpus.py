import re  
import pandas as pd  
from time import time  
import nltk


df = pd.read_csv("My_Data.csv")

tk = nltk.tokenize.LineTokenizer() 
stop_words = set(nltk.corpus.stopwords.words('french'))

def preprocessing(text):
    
    lines = tk.tokenize(text)
    clean = [re.sub("[^\w']+", ' ', str(row), flags=re.UNICODE).lower() for row in lines]
    liste = [[word for word in elem.split(" ") if not word in stop_words and word != '' ] for elem in clean]
    final_list = [' '.join(line) for line in liste if len(line)>2]
    
    return final_list


def write_list_to_file(list, file_name):
    with open('Word2Vec_input/'+file_name, 'a') as out_file:
        for text in list:
                 out_file.write(text+'\n')



