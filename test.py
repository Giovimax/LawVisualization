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
import Dash
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
def p(*args):
    lv.pp(*args,file="log.txt")

#%%
p("Creating df, G, RawToPathDict")
df, G, RawToPathDict = importCodes("codice_civile.codice")
p("Done")
#%%
def populateGraphRaw(G,df,ToPathDict):
    for linkList in df["path_from_link"]:
        node = tuple(linkList)
        name = None
        if node[-1] in ToPathDict: #sets the name as pretty name if possible
            name = ToPathDict[node[-1]]
        G.add_node(node,name=name)

#%%
p("Populating graph...")
populateGraphRaw(G,df,RawToPathDict)
p("Done.")
#%%

#a = dict()
#for node in G.nodes():
#    for n,i in enumerate(node[:-1]):
#        try:
#            if i not in a[n]:
#                a[n].append(i)
#        except:
#            a[n]=[i]
#%%
p("Adding edges.")
#I want to create a way to color the nodes 
for nodeA in G.nodes:
    for nodeB in G.nodes:
        shared = 0
        if nodeA != nodeB:
            for i in nodeA:
                if i in nodeB:
                    shared+=1
            if shared > 0:
                G.add_edge(nodeA,nodeB,weight=shared)
p("Done.")
#%%
p("Calculating positions...")
pos = nx.kamada_kawai_layout(G)
p("Done.")              
#%%
p("Saving Data/newMethodTest ...")
with open("Data/newMethodTest","b+w") as f:
    pickle.dump(pos,f)
p("Saving Done.")

#%%Setting pos as attribute
try:
    pos
except:
    with open("Data/newMethodTest","b+r") as f:
        pos = pickle.load(f)
nx.set_node_attributes(G,pos,name="pos")

#%%
p("Starting dashification and saving...")
tosave = Dash.dashify(G)
with open("Data/newMethodTestDash","b+w") as f:
    pickle.dump(tosave,f)
p("Done.")