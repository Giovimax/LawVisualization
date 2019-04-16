#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:44:06 2019

@author: giovimax
"""
import bs4 as bs
import pandas as pd 
import requests as re
from LawVis import *
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
if "all.txt" not in listdir():
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
        item = crawlBoccardi(link[-1],raw = False, complex_=True)
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
rawToPatDict = dict()
"""A dict that contains the particle names from the link as keys and the 
name extracted from the path in the website as value, it is needed to map 
more readeable names over the raw ones"""
for i in range(len(df)):#for row in df
    path, link = df.loc[i,["path","link"]]#unpacks and assigns 
    #preparation 
    #cl
    cl = clearLink(link)
    for n, i in enumerate(cl):
        if i == 'www.brocardi.it': #removes everything before and the domain 
            cl = cl[n+1:]
            break
    #path
    path = path[1:] #removes the useless part
    #main
    for k,v in zip(cl,path): 
        if k not in rawToPatDict:
            rawToPatDict[k] = v
    
def rawToPath(rawlist): #uses the rawToPatDict dict to substitute matching vals
    rawlistcopy = list(rawlist)
    for i, l in enumerate(rawlist):
        if l in rawToPatDict:
            rawlistcopy[i] = rawToPatDict[l]
        else:
            pass
    return rawlistcopy

#%%
#CREATION OF THE NETWORK OBJECT
g = nx.Graph()
#Function that creates additional links (DEPRECIATED)

#for nitem, item in enumerate(df["link_commi"]):
#    item_name = df["path"][nitem][-1]
#    for link in item:
#        link = clearLink(link)
#        if link[0] =='codice-civile':
#            for n,j in enumerate(link):
#                if j not in g.nodes:
#                    g.add_node(j)
#                    if n !=len(link)-1:
#                        g.add_edge(j,link[n-1])
#                    else:
#                        g.add_edge(j,item_name)
#        else:
#            link = link[::-1]
#            for n, j in enumerate(link):
#                if n == 0:
#                    g.add_edge(j,item_name)
#                else:
#                    g.add_edge(j,link[n-1])
#                    

#%%

#g.add_nodes_from([str(i) for i in df["path"]])

#CREATION OF THE GRAPH
#method with path

#for i in df["path"]:
#    for n,j in enumerate(i):
#        if j not in g.nodes:
#            g.add_node(j)
#            if n !=0:
#                g.add_edge(j,i[n-1])
#            else:
#                pass
#        else:
#            pass

# FIXME: ?
# XXX: ?
# HINT: ?
# TIP: ?
#@todo: ?

#advanced method with function
# TODO: make rawToPatDict independent 
def addItemAsNode(G,link):
    #TODO: change link to the list from path_from_dict to diminish processing
    clearLinkList = clearLink(link)#list of relevent items
    
    iterable = []
    """i'm now using as a univoque node the full relevant path of each section 
    of the actutual path of the single object"""
    for n, item in enumerate(clearLinkList):
        iterable.append(tuple(clearLinkList[:n+1]))
        
    for n, node in enumerate(iterable):
        #for each possible node
        if node not in G.nodes:
            #name part
            name = None
            if node[-1] in rawToPatDict: #sets the name as pretty name if possible
                name = rawToPatDict[node[-1]]
            #adding node
            G.add_node(node,name=name)
            #creating edges
            if n != 0:
                g.add_edge(node,iterable[n-1])
            else:
                pass

#actual population of the network
for link in df["link"]:
    addItemAsNode(g,link)
   
##method with link (DOES NOT WORK PROPERLY)
#for i in df["link"]:
#    l = i.split("/")[3:]
#    l[-1] = l[-1].split(".")[0]
#    for n,j in enumerate(l):
#        if j not in g.nodes:
#            g.add_node(j)
#            if n !=0:
#                g.add_edge(j,i[n-1])
#            else:
#                pass
#        else:
#            pass
#%%
#nx.draw(g, with_labels=True)
