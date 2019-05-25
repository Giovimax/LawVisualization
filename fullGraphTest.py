#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:26:24 2019

@author: giovimax
"""
#%%imports
import pickle
import pandas as pd
import networkx as nx
import LawVis as lv
import Dash
import datetime
now = datetime.datetime.now 
#%%
def P(*args):
    lv.pp(*args,file="three_code_test.log")
#%%
def addWeightedEdges(G):
    """Adds an edge between each node wieghted by the number of shared 
    subcategories so that the weight is highter the more close in the book the 
    articles are"""
    for nodeA in G.nodes:
        for nodeB in G.nodes:
            shared = 0
            if nodeA != nodeB:
                for i in nodeA:
                    if i in nodeB:
                        shared+=1
                if shared > 0:
                    G.add_edge(nodeA,nodeB,weight=shared)

#%% Loading data from files
P("Starting Full Graph production")
Codici = "Data/Codici/"
cc = ['costituzione.codice',
'codice_del_turismo.codice',
'codice_del_consumo.codice',]
full_list = []
P("loading codici...")
for code in cc:
    with open(Codici+code,"b+r") as f:
        full_list = full_list + pickle.load(f)
P("codici loaded.")
P("Creating df ,rawToPathDict and Graph obj...")
df = pd.DataFrame(full_list)

G = nx.Graph()

#%%Manipulating 
rawToPathDict = lv.genRawToPathDict(df)
P("df, rawToPathDict and graph done.")
startTime = now()

lv.populateGraphRaw(G,df,rawToPathDict)
addWeightedEdges(G)
P("Calculating pos...")
startTime = now()
pos = nx.kamada_kawai_layout(G)
endTime = now()
P("pos calculated, time:",endTime-startTime)
nx.set_node_attributes(G,pos,name="pos")

with open("Data/three_code_test.pos","b+w") as f:
    pickle.dump(pos,f)#%%Converting to dash object
#%%
P("Calculating dashObj...")
startTime = now()
dashObj = Dash.dashify(G,)
endTime = now()
P("dashObj calculated, time:",endTime-startTime)
with open("Data/three_code_test.dashTuple","b+w") as f:
    pickle.dump(dashObj,f)
P("File dumped, end.")
    




