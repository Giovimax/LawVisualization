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
#try:
#    link,todf
#except:
#    link = ['https://www.brocardi.it/codice-civile/libro-primo/titolo-i/art1.html']
#    todf = []
#
#if "all.txt" not in listdir("Data/"):
#    print("no all.txt, creating and dumping")
#    #safety mesure        
#    status = True#flag for the while:
#    
#    while status:
##    for i in range(10):
#        item = lv.crawlBoccardi(link[-1],raw = False, complex_=True)
#        sleep(0.1)
#        todf.append(item[0])
#        if item[1] == False:
#            status = False
#        else:
#            link.append(item[1])
#        print(item[0]["path"][-1])
#    print("finished")
#    df = pd.DataFrame(todf)
#    
#    with open("all.txt","b+w") as file:
#        pickle.dump(df,file)
#else:
#    print("loading all.txt")
#    with open("Data/all.txt","b+r") as file:
#        df = pickle.load(file)
#        
#

#%%
#CREATION OF THE NETWORK OBJECT
#g = nx.Graph()
#
##%%
#rawToPatDict = lv.genRawToPathDict(df)
##%%
#
## FIXME: ?
## XXX: ?
## HINT: ?
## TIP: ?
##@todo: ?
#
##advanced method with function
#lv.populateGraph(g,df,rawToPatDict)
# 
#
#
##%%
#lv.linksFromCommi(g,df,rawToPatDict)
##%%
#print("Drawing...")
#nx.draw(g, with_labels=False)

#%%new stuff
def importCodes(*args,df=True,G=True):
    Codici = "Data/Codici/"
    allList = []
    RawToPathDict = False
    for code in listdir(Codici):
        if len(args)!=0 and code in args:
            with open(Codici+code,"b+r") as f:
                allList = allList + pickle.load(f)
    if df:
        df = pd.DataFrame(allList)
        if G:
            G = nx.Graph()
            RawToPathDict = lv.genRawToPathDict(df)
#            lv.populateGraph(G,df,RawToPathDict)
#            lv.linksFromCommi(G,df,RawToPathDict,weight=1)
    else:
        return allList
    return (df,G,RawToPathDict)
##%%
##df, G = importAll()
#Codici = "Data/Codici/"
#allList = []
#for code in listdir(Codici):
#    with open(Codici+code,"b+r") as f:
#        allList = allList + pickle.load(f)
#df = pd.DataFrame(allList)
#G = nx.Graph
#RawToPathDict = lv.genRawToPathDict(df)
#lv.populateGraph(G,df,RawToPathDict)
#lv.linksFromCommi(G,df,RawToPathDict,weight=1)
#%%
df, G, RawToPathDict = importCodes("codice_civile.codice")
#%%
def populateGraphRaw(G,df,ToPathDict):
    for linkList in df["path_from_link"]:
        node = tuple(linkList)
        name = None
        if node[-1] in ToPathDict: #sets the name as pretty name if possible
            name = ToPathDict[node[-1]]
        G.add_node(node,name=name)

#%%
a = dict()
for node in G.nodes():
    for n,i in enumerate(node[:-1]):
        try:
            if i not in a[n]:
                a[n].append(i)
        except:
            a[n]=[i]
#%%
#I want to create a way to color the nodes 
