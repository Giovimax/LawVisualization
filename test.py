#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:44:06 2019

@author: giovimax
"""
import bs4 as bs
import pandas as pd 
import requests as re
import LawVis as lv
import networkx as nx 
import pickle 
from os import listdir
from time import sleep
#%%
"""brief instructions:
    the program automatically searches for all.txt and tries to load it, this 
    file must contain a pickled version of the df with the data of the articles.
    If the file is not found, it creates it with che canonical function 
    crawlBoccardi.
    The code can function with the while: and the flag "status" or with the 
    for loop with the range funct if only a fraction of the articles is needed.
"""
if "Data/all.txt" not in listdir():
    print("no all.txt, creating and dumping")
    #safety mesure
    try:
        link,todf
    except:
        link = ['https://www.brocardi.it/codice-civile/libro-primo/titolo-i/art1.html']
        todf = []
        
    status = True#flag for the while:
    
    while status:
#    for i in range(10):
        item = lv.crawlBoccardi(link[-1],raw = False, complex_=True)
        sleep(0.1)
        todf.append(item[0])
        if item[1] == False:
            status = False
        else:
            link.append(item[1])
        print(item[0]["path"][-1])
    print("finished")
    df = pd.DataFrame(todf)
    
    with open("all.txt","b+w") as file:
        pickle.dump(df,file)
else:
    print("loading all.txt")
    with open("all.txt","b+r") as file:
        df = pickle.load(file)
        


#%%


#extraction of the dict from raw to path
#rawToPatDict = dict()
#"""A dict that contains the particle names from the link as keys and the 
#name extracted from the path in the website as value, it is needed to map 
#more readeable names over the raw ones"""
#for i in range(len(df)):#for row in df
#    path, link = df.loc[i,["path","link"]]#unpacks and assigns 
#    #preparation 
#    #cl
#    cl = lv.clearLink(link)
#    for n, i in enumerate(cl):
#        if i == 'www.brocardi.it': #removes everything before and the domain 
#            cl = cl[n+1:]
#            break
#    #path
#    path = path[1:] #removes the useless part
#    #main
#    for k,v in zip(cl,path): 
#        if k not in rawToPatDict:
#            rawToPatDict[k] = v
        # ^ depreciated by genRawToPathDict


#%%
#CREATION OF THE NETWORK OBJECT
g = nx.Graph()

#%%
rawToPatDict = lv.genRawToPathDict(df)
#%%

# FIXME: ?
# XXX: ?
# HINT: ?
# TIP: ?
#@todo: ?

#advanced method with function

 

#%%
#nx.draw(g, with_labels=True)


