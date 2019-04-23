# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:34:21 2019

@author: Gokmen Oz
"""

#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
#from io import StringIO
import re
import os
import pandas as pd
import numpy as np
import dill
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def pull_top_needs(text):
    pattern='three issues:[\n•]+([A-Za-z ]+)[\n•]+([A-Za-z ]+)[\n•]+([A-Za-z ]+)'
    return re.findall(pattern,text)
    

#needs=dict()
#path=r'C:\Users\Gokmen Oz\SeamSocialLabs\static\statements'
#for boro_year in os.listdir(path):
#    boro=boro_year[:2]
#    year=int(boro_year[-4:])
#    if year==2017:
#        for dist in os.listdir(path+'\\'+boro_year):
#            needs[boro+dist[-6:-4]]=pull_top_needs(convert_pdf_to_txt(path+'\\'+boro_year+'\\'+dist))
#    if year>2017:
#        for dist in os.listdir(path+'\\'+boro_year):
#            needs[boro+dist[-6:-4]].extend(pull_top_needs(convert_pdf_to_txt(path+'\\'+boro_year+'\\'+dist)))


#needs=dill.load(open('static/needs.pkd','rb'))
#dist_needs=dill.load(open('static/dist_needs.pkd','rb'))
#
#for col in needs.columns:
#    for j in range(len(needs[col])):
#        temp=[0]*26
#        for need in dist_needs:
#            for (i,n) in enumerate(needs[col][j]):
#                if need in n:
#                    temp[dist_needs.index(need)]=3-i
#        needs[col][j]=temp
    
X_train=dill.load(open('static/X_train.pkd','rb'))

from functools import reduce

def extend(x,y):
    if type(x)!=list:
        x=list[x]
    if type(y)!=list:
        y=list[y]
    return x+y

def convert_from_array_to_list(X):
    for x in X:
        X[0]=list(reduce(extend,list(x)))
    return X

X=X_train.iloc[:,:-1].values
Y=X_train.iloc[:,-1:].values

X_list=convert_from_array_to_list(X)
Y_list=convert_from_array_to_list(Y)

classifier=KNeighborsRegressor(n_neighbors=5)
classifier.fit(X_list,Y_list)

X_train=X_train.drop(['2017'],axis=1)
X_list=convert_from_array_to_list(X_train.values)
for y in range(2021,2025):
    Y_new=classifier.predict(X_list)
    X_train=X_train.drop([str(y-3)],axis=1)
    X_train[str(y)]=Y_new
    X_list=convert_from_array_to_list(X_train.values)