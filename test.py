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
from numpy import sin, cos, deg2rad
#%%
"""brief instructions:
    the program automatically searches for all.txt and tries to load it, this 
    file must contain a pickled version of the df with the data of the articles.
    If the file is not found, it creates it with che canonical function 
    crawlBoccardi.
    The code can function with the while: and the flag "status" or with the 
    for loop with the range funct if only a fraction of the articles is needed.
"""

#%%

## FIXME: ?
## XXX: ?
## HINT: ?
## TIP: ?
##@todo: ?

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
            lv.populateGraph(G,df,RawToPathDict)
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
#%% p plain
def p(*args):
    print(*args)

#%% p complete
def p(*args):
    lv.pp(*args,file="log.txt")

#%%Creating df, G, RawToPathDict
p("Creating df, G, RawToPathDict")
df, G, RawToPathDict = importCodes("codice_civile.codice")
p("Done")


#%%Populating graph...
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
#%%Adding edges.
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
#%%Calculating positions
p("Calculating positions...")
pos = nx.kamada_kawai_layout(G)
p("Done.")              
#%%Saving Data/newMethodTest ...
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

#%%Starting dashification and saving...
p("Starting dashification and saving...")
tosave = Dash.dashify(G)
with open("Data/newMethodTestDash","b+w") as f:
    pickle.dump(tosave,f)
p("Done.")

#%% Color assignment
#(R, G, B) = (256*cos(x), 256*cos(x + 120), 256*cos(x - 120))
entPerLib = dict() #dict with the number of entries for each book 
for i in df["path_from_link"]:
    i = tuple(i[1:2])
    if i not in entPerLib.keys():
        entPerLib[i]= 1
    else:
        entPerLib[i] += 1
entPerLib = pd.Series(entPerLib)
totEnt = entPerLib.sum()
entPerLib = entPerLib.apply(lambda x: x/totEnt*360)
cumulative = 0
for i in entPerLib.keys():
    cumulative += entPerLib[i]
    entPerLib[i] = cumulative
#%% toHEX function
def toHEX(x):
    #TODO: review this function, probably it does not work
    x = deg2rad(x)
#    print(x)
    rgb = tuple([i for i in map(lambda x: int(128+round(x*128)), [cos(x), cos(x + 120), cos(x - 120)])])
#    print(rgb)
    toret = '#%02x%02x%02x' % rgb
    return toret[:7]
#%%
colourScheme = entPerLib.apply(toHEX)

#