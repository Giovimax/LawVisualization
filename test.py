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
            lv.populateGraphRaw(G,df,RawToPathDict)
#            lv.linksFromCommi(G,df,RawToPathDict,weight=1)
    else:
        return allList
    return (df,G,RawToPathDict)

#%% def colourSchemeMaker(df):
def colourSchemeMaker(df):
    """Takes the df and produces a dict with a colour related to a relevant
    portion of the path"""

    # toHEX function
    def toHEX(x):
        #TODO: review this function, probably it does not work
        x = deg2rad(x)
    #    print(x)
        rgb = tuple([i for i in map(lambda x: int(128+round(x*128)), [cos(x), cos(x + 120), cos(x - 120)])])
    #    print(rgb)
        toret = '#%02x%02x%02x' % rgb
        return toret[:7]

    #Color assignment
    #(R, G, B) = (256*cos(x), 256*cos(x + 120), 256*cos(x - 120))
    entPerLib = dict() #dict with the number of entries for each book 
    for path in df["path_from_link"]:
    #    print(path)
        path = tuple(path[1:3])#selects the first two relevant parts of the path
    #    print(path)
        if path not in entPerLib.keys():
            entPerLib[path]= 1
        else:
            entPerLib[path] += 1
    entPerLib = pd.Series(entPerLib)
    totEnt = entPerLib.sum()
    entPerLib = entPerLib.apply(lambda x: x/totEnt*360)
    cumulative = 0
    for entry in entPerLib.keys():
        cumulative += entPerLib[entry]
        entPerLib[entry] = cumulative
    return entPerLib.apply(toHEX)
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


##%%Populating graph... IS NOW REDUNDANT
#p("Populating graph...")
#lv.populateGraphRaw(G,df,RawToPathDict)
#p("Done.")

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
##%%Calculating positions
#p("Calculating positions...")

#posDict = nx.kamada_kawai_layout(G)
#p("Done.")              
#%%Saving Data/newMethodTest ...
#p("Saving Data/newMethodTest ...")
#with open("Data/newMethodTest","b+w") as f:
#    pickle.dump(pos,f)
#p("Saving Done.")

#%%Setting pos as attribute
p("Setting pos as attribute...")
try:
    posDict
except:
    with open("Data/newMethodTest","b+r") as f:
        posDict = pickle.load(f)
nx.set_node_attributes(G,values=posDict,name="pos")
p("Done")
#%%Quick fix for broken nodes
#TODO: the issue should have been fixed by the change of populating function, VERIFY IT
posCheck = dict(pos=[],noPos=[])
for node in G.nodes:
    try:
        G.node[node]["pos"]
        posCheck["pos"].append(node)
    except:
        posCheck["noPos"].append(node)
        
G.remove_nodes_from(posCheck["noPos"])#removes the nodes

#%%Creating colour scheme
colourScheme = colourSchemeMaker(df)
#%%Starting dashification and saving...
p("Starting dashification and saving...")
tosave = Dash.dashify(G,colourScheme)
with open("Data/newMethodTestDash","b+w") as f:
    pickle.dump(tosave,f)
p("Done.")



#%%
class codeObj():
    def __init__():
        pass
    pass
