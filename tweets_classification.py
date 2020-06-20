from google.colab import files
file=files.upload()
#!unzip glove.6B.50d.zip

import nltk
nltk.download('stopwords')
import nltk
nltk.download('punkt')

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation

import os
import sys
import pandas as pd

from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
# data processing, CSV file I/O (e.g. pd.read_cs)
import io
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop = set(stopwords.words('english'))

from __future__ import print_function

import math
import os
import sys
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from keras.initializers import Constant

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation


from google.colab import files
file=files.upload()

#names = ['ID', 'TEXT', 'created-at', 'label']
dataset = pd.read_csv('labelled data 2.csv')
print (dataset.shape)
print(dataset.head(5))



#next
for i in range(37354):
  dataset['TEXT'][i] =' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",dataset['TEXT'].str.lower().values[i]).split())#punctuation removal
  dataset['TEXT'][i] = ''.join([i for i in dataset['TEXT'][i] if not i.isdigit()]) #sentence after digits removal
  stop_words = set(stopwords.words('english')) 


#next
embeddings_index = {}
f = open('glove.6B.50d.txt')
for line in f:
    values = line.split(' ')
    word = values[0] ## The first entry is the word
    coefs = np.asarray(values[1:], dtype='float32') ## These are the vecotrs representing the embedding for the word
    embeddings_index[word] = coefs
f.close()

print('GloVe data loaded'),embeddings_index["earthquake"]
#print coefs.size
#print("Total Words in DataSet:",len(embeddings_index))


#next
n_posts = 10000
j=0
l=0
input_matrix = np.zeros((n_posts,50))
for k in range(n_posts):
    
      text = dataset['TEXT'].values[k]
      tk = word_tokenize(text)
      x = 0
      i=0
    
      for w in tk:
          #if w not in stopwords:
          embedding_vector = embeddings_index.get(w)
          if embedding_vector is not None:
              i=i+1
              x = x+embedding_vector
      if i == 0:
          input_matrix [j] = np.zeros((50))
          j = j+1
      elif i or i != 0:
          l=l+1
          input_matrix [j] = x/i
          j = j+1

print(l)
print(input_matrix)
print(input_matrix.shape)


#next
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

df = pd.DataFrame(input_matrix) # load the dataset as a pandas data frame
y = dataset['label'].values[:n_posts] # define the target variable (dependent variable) as y
for i in range(n_posts):
    if y[i]==2:
        y[i] = 1
    else:
        y[i] = 0

# create training and testing vars
xtrain, xtest, ytrain, ytest = train_test_split(df, y, test_size=0.2)

xtrain = xtrain.values
xtest = xtest.values
print(xtrain.shape)
print(ytest)


#next
xtrain.reshape(int(n_posts*0.8),1,50,1)
xtest.reshape(int(n_posts*0.2),1,50,1)
data=xtrain.reshape(int(n_posts*0.8),1,50,1)

#main thing
lab=[]
for i in range(int(n_posts*0.8)):
    if ytrain[i]==1:
            lab.append([1,0])
    else:
        lab.append([0,1])
        
lab=np.array(lab)
#labels=lab.reshape(800,1,2)
labels = lab.reshape(int(n_posts*0.8),1,2)


model=Model(inputs=inputs,outputs=pred)
model.compile(optimizer='adagrad',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(data, labels,batch_size=16,epochs=5)
