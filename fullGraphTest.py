#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:26:24 2019

@author: giovimax
"""
#%%imports
from os import listdir 
import pickle
import pandas as pd
import networkx as nx
import LawVis as lv
import Dash
import datetime
now = datetime.datetime.now 
from test import addWeightedEdges
#%%
def P(*args):
    lv.pp(*args,file="log_full_graph")
#%% Loading data from files
P("Starting Full Graph production")
Codici = "Data/Codici/"
cc = ['costituzione.codice',
'codice_del_turismo.codice',
'codice_del_consumo.codice',]
full_list = []
P("loading codici...")
for code in listdir(Codici):
    with open(Codici+cc,"b+r") as f:
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
dashObj = Dash.dashify(G)
endTime = now()
P("dashObj calculated, time:",endTime-startTime)
with open("Data/three_code_test.dashTuple","b+w") as f:
    pickle.dump(dashObj,f)
P("File dumped, end.")
    




