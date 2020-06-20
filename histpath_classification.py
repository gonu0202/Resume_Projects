from skimage import data,filters
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from sklearn.datasets import load_sample_image
from sklearn.feature_extraction import image
import os
import skimage
import cv2
from cv2 import watershed
import numpy as np
import matplotlib
import argparse
from scipy import ndimage

from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

from keras.layers import Input, Dense, Flatten,Activation
from keras.models import Model,load_model,Sequential


#next
from os import listdir
from os.path import isfile,join
p = []
path=r'C:\Users\ANIKET KUMAR\Desktop\iitbhu_intern\DATASET\fold3\test\separated200x\Benign'
files = [f for f in listdir(path) if isfile(join(path,f))] 
for image_file in files:
        x = cv2.imread(os.path.join(path,image_file))
        #print(x.shape)
        x = cv2.resize(x,(350,230))
        gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray,(350 , 230))     
        t = filters.threshold_otsu(gray)
        ret,G = cv2.threshold(gray,t,255,cv2.THRESH_BINARY)
        ret,G_inv = cv2.threshold(gray,t,255,cv2.THRESH_BINARY_INV) 
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(G_inv,cv2.MORPH_OPEN,kernel,iterations = 2)
        sure_bg = cv2.dilate(opening,kernel,iterations=3)
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers+1
        markers[unknown==255] = 0
        markers = cv2.watershed(x,markers)
        x[markers == -1] = [255,0,0]
        B = x
        B = cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
        th1 = cv2.adaptiveThreshold(B,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        th2 = cv2.adaptiveThreshold(B,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                
        patches = image.extract_patches_2d(th1, (32, 32),30,)
        patches = patches.reshape(len(patches), np.prod(patches.shape[1:]))
        p.append(patches)
print(len(p))
print(len(p[0]))

p1 = []
path=r'C:\Users\ANIKET KUMAR\Desktop\iitbhu_intern\DATASET\fold3\test\separated200x\Malignant'
files = [f for f in listdir(path) if isfile(join(path,f))] 
for image_file in files:
        x = cv2.imread(os.path.join(path,image_file))
        #print(x.shape)
        x = cv2.resize(x,(350,230))
        gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray,(350 , 230))     
        t = filters.threshold_otsu(gray)
        ret,G = cv2.threshold(gray,t,255,cv2.THRESH_BINARY)
        ret,G_inv = cv2.threshold(gray,t,255,cv2.THRESH_BINARY_INV) 
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(G_inv,cv2.MORPH_OPEN,kernel,iterations = 2)
        sure_bg = cv2.dilate(opening,kernel,iterations=3)
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers+1
        markers[unknown==255] = 0
        markers = cv2.watershed(x,markers)
        x[markers == -1] = [255,0,0]
        B = x
        B = cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
        th1 = cv2.adaptiveThreshold(B,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        th2 = cv2.adaptiveThreshold(B,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                
        patches = image.extract_patches_2d(th1, (32, 32),30,)
        patches = patches.reshape(len(patches), np.prod(patches.shape[1:]))
        p1.appen(patches)
print(len(p1))
print(len(p1[0]))



#next
x_b = p
x_b = np.asarray(x_b, dtype=np.float32)
x_b = x_b/255
x_b = x_b.reshape(len(p)*len(p[0]), 1024)
#print(x_b.shape)
y_b =np.asarray([np.zeros(len(p)*len(p[0]))])
Benign=np.concatenate((x_b,y_b.T),axis=1)

x_m = p1
x_m = np.asarray(x_m, dtype=np.float32)
x_m = x_m/255
x_m = x_m.reshape(len(p1)*len(p1[0]), 1024)
#print(x_m.shape)
y_m =np.asarray([np.ones(len(p1)*len(p1[0]))])
Malignant=np.concatenate((x_m,y_m.T),axis=1)

test_data=np.concatenate((Malignant,Benign),axis=0)
#np.random.shuffle(test_data)
xtest = test_data[:,:-1]
ytest = test_data[:,-1]
print(ytest[:5])
print(xtest.shape)
#print(Malignant_100.shape)



#next
from sklearn import metrics

scaler = StandardScaler()
xt = encoder.predict(xtest)
scaler.fit(xt)
ypred = clf.predict(scaler.transform(xt))
print("Accuracy per patch of image: ",metrics.accuracy_score(ytest, ypred))



cm=0
c=0
x=0
y=0
cbt=0
for i in range(len(ytest)):
    y = y+1
    if(ytest[i] == 0.0):
        cbt = cbt+1
    if (ypred[i] == ytest[i]):
        x = x+1
    if (y == 30):
        if(x>=15):
            c = c+1
            if(ytest[i-1] == 1.0):
                cm = cm+1
            else:
                cb = cb+1
        x=0
        y=0
        
#print(ypred[1000])
total = (len(ytest))/30
cbt = cbt/30
cmt = (total-cbt)
print('Accuracy per image classification: ', c/total)
print('Accuracy of benign image: ', cb/cbt)
print('Accuracy of Malignant image: ', cm/cmt)
