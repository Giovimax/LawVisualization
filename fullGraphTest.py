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
import colorutils
#%%
def P(*args):
    print(*args)
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
            shared = 2
            if nodeA != nodeB:
                for i in nodeA:
                    if i in nodeB:
                        shared *= shared 
                    else:#
                        """this avoids adding weight when the nodes do not 
                        share the same root/higher level set"""
                        break
                if  True:
                    G.add_edge(nodeA,nodeB,weight=shared**2)

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
    return entPerLib.apply(toHEX).to_dict()
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
try:
    pos
except:
    pos = nx.kamada_kawai_layout(G)
endTime = now()
P("pos calculated, time:",endTime-startTime)
nx.set_node_attributes(G,pos,name="pos")

with open("Data/three_code_test.pos","b+w") as f:
    pickle.dump(pos,f)#%%Converting to dash object
#%%
P("Calculating dashObj...")
startTime = now()
colourScheme = colourSchemeMaker(df,slice(0,1))
dashObj = Dash.dashify(G,colourScheme)
endTime = now()
P("dashObj calculated, time:",endTime-startTime)
with open("Data/three_code_test.dashTuple","b+w") as f:
    pickle.dump(dashObj,f)
P("File dumped, end.")
    




