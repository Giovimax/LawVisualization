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
import colorutils
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
    #TODO: add the option to load multiple codes
    """Imports a SINGLE CODE from the data"""
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
def colourSchemeMaker(df,subCategoriesSlice=slice(1,3)):
    """Takes the df and produces a dict with a colour related to a relevant
    portion of the path"""
#TODO: evaluate if preserve proportional version or drop it 
    # toHEX function
    def toHEX(deg):
        c = colorutils.Color(hsv=(deg,1,1))
        return c.hex

    #Color assignment
    #(R, G, B) = (256*cos(x), 256*cos(x + 120), 256*cos(x - 120))
    entPerLib = dict() #dict with the number of entries for each book 
    for path in df["path_from_link"]:
#    #    print(path)
        path = tuple(path[subCategoriesSlice])#selects the first two relevant parts of the path
#    #    print(path)
#        if path not in entPerLib.keys():
#            entPerLib[path]= 1
#        else:
#            entPerLib[path] += 1
        
        #creating non proportional colouring 
        if path not in entPerLib:
            entPerLib[path] = 0
    entPerLib = pd.Series(entPerLib)
#    totEnt = entPerLib.sum()
#    entPerLib = entPerLib.apply(lambda x: x/totEnt*360)
    cumulative = 0
    fraction = 360/len(entPerLib)
    for entry in entPerLib.keys():
#        cumulative += entPerLib[entry]
#        entPerLib[entry] = cumulative
        #non proportional version
        entPerLib[entry] = cumulative
        cumulative += fraction
    return entPerLib.apply(toHEX)
#%% p plain
def p(*args):
    print(*args)

##%% p complete
#def p(*args):
#    lv.pp(*args,file="log.txt")

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
def addWeightedEdges(G):
    """Adds an edge between each node wieghted by the number of shared 
    subcategories so that the weight is highter the more close in the book the 
    articles are"""
    for nodeA in G.nodes:
        for nodeB in G.nodes:
            shared = 0
            if nodeA != nodeB:
                for i in nodeA[:]:#TODO: parametrize this 
                    if i in nodeB:
                        shared+=1
                if shared > 0:
                    G.add_edge(nodeA,nodeB,weight=shared)
addWeightedEdges(G)
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

##%%Creating colour scheme
#colourScheme = colourSchemeMaker(df,1)
##%%Starting dashification and saving...
#p("Starting dashification and saving...")
#tosave = Dash.dashify(G,colourScheme)
#with open("Data/newMethodTestDash_1","b+w") as f:
#    pickle.dump(tosave,f)
#p("Done.")
#

#%%
##TODO: make sense of this mess
#Gsimplified = nx.Graph()#creating new graph
#simplifiedNodes = {} #container for node congregations
#for node in G.nodes:
#    relNode = node[1:3]#selects only macro category of nodes
#    if relNode not in simplifiedNodes:
#        simplifiedNodes[relNode] = {"size":1,}#adds a dictionary with a counter
#    else:
#        simplifiedNodes[relNode]["size"] += 1#simply updates the counter
#        
#for node in simplifiedNodes:#populates the graph with nodes
#    Gsimplified.add_node(node,size=simplifiedNodes[node]["size"])
#
##%%
#for i in simplifiedNodes:
#    simplifiedNodes[i]["links"] = {}#creates a dict to store the number of links 
#    
#for row in df.loc[:,:]:
#    linkList =[]#stores the prepared links from the notes
#    for link in row["link_commi"]:
#        if "dizionario" not in link and "nota" not in link and "codice-civile"  in link:#selecting only relevant links
#            link = tuple(lv.clearLink(link))[1:3]#cuts useless part
#            linkList.append(link)#ads to list
#    path = row["path_from_link"][1:3]#selects simplifiedNodes key for this row
#    for link in linkList:#dumps links into simplifiedNodes
#        #saves the number of links 
#        if link in simplifiedNodes[path]["links"]:#nel sottogruppo del nodo corrente
#            simplifiedNodes[path]["links"][link] +=1
#        else:
#            simplifiedNodes[path]["links"][link] =1
#    pass
#%%
"""Plan to update df:
    create enought lists to fitt all the levels
    create a list for each level of the path 
    for each row add 
    add the lists as co
    """
ll = [[] for i in range(5)]#list of all the lists
for path_from_link in df.iloc[:,5]:#for row in path_from_link
    core = path_from_link[1:-1]
    for n in range(4):
        try:
            ll[n].append(core[n])
        except:
            ll[n].append(None)
    ll[-1].append(path_from_link[-1])
    
#%%
try:
    copy
except:
    from copy import copy
testdf = copy(df)
for n, i in enumerate(ll):
    testdf[n]=i

testdf = testdf.set_index([0,1,2,3,4])

def artToIndex(art):
    """Thakes the raw name of the article and transforms it into a tuple 
    that can be used with the dataframe"""
    return (slice(None),slice(None),slice(None),slice(None),art)