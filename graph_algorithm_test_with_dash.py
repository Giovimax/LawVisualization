#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:42:57 2019

@author: giovimax
"""
#%%IMPORTS

from Dash import dashify
import pickle
import networkx as nx
import LawVis as lv
import pandas as pd
import datetime
now = datetime.datetime.now 

#%% Definitions


    
def dashTupleFromGraph(df,layoutFunction,folder,verbose = True,**kwargs):
    """saves dashTuples generated from a df, using the imputted layoutFunction and 
    the used kwargs, saves in the given folder
    for kwargs:
    "secondary_weight" -> the weight of the edges from in text links
    "primary_weight" -> weight from direct edges
    """
    
    #enanced print function
    
    def P(*args):
            if verbose:
                lv.pp(*args,file=folder+"log")
            else:
                pass

    #name of the file
    name = layoutFunction.__name__
    print(kwargs)
    kargs_name = ""
    keys = kwargs.keys()
    vals = [kwargs[k] for k in keys]
    for k, v in zip(keys,vals):
        kargs_name += "__{}_{}".format(k,v)
    filename = name+kargs_name+"_"
    print(filename)
    startTime = now()
    P("Working on",filename,startTime)
    #CREATING GRAPH
    P("CREATING GRAPH")
    #creating rawToPathDict
    P("creating rawToPathDict")
    rawToPathDict = lv.genRawToPathDict(df)
    
    #creating graph
    G = nx.Graph()
    
    #populating graph
    P("populating graph")
    lv.populateGraph(G,df,rawToPathDict,kwargs["primary_weight"])
    
    #additional edges
    P("additional edges")
    lv.linksFromCommi(G,df,rawToPathDict,kwargs["secondary_weight"])
    
    #Computing pos
    prevTime = now()
    P("Computing postion...",prevTime,)
    pos = layoutFunction(G,)
    newTime = now()
    P("Position computed",newTime,newTime-prevTime)
    
    #Computing dashTuple
    prevTime = now()
    P("Starting computing dashTuple",prevTime)
    nx.set_node_attributes(G,pos,name="pos")
    dashTuple= dashify(G)
    
    newTime = now()
    P("Finished computing dashTuple",newTime,newTime-prevTime)
    P("Saving...")
    with open(folder+filename,"b+w") as file:
        pickle.dump(dashTuple,file)
    P("Saving Done! Finished",now(),now()-startTime)
#%%
with open("Data/Codici/codice_civile.codice","b+r") as cc:
    df = pd.DataFrame(pickle.load(cc))
#%% old gnerator 
#dashTupleFromGraph(df,nx.spring_layout,"Data/Graph_tests/",verbose=True,
#                   **{"secondary_weight":1,
#                    "primary_weight":1})
#dashTupleFromGraph(df,nx.spring_layout,"Data/Graph_tests/",verbose=True,
#                   **{"secondary_weight":1,
#                    "primary_weight":0.5})
#dashTupleFromGraph(df,nx.spring_layout,"Data/Graph_tests/",verbose=True,
#                   **{"secondary_weight":1,
#                    "primary_weight":0.1})
#dashTupleFromGraph(df,nx.kamada_kawai_layout,"Data/Graph_tests/",verbose=True,
#                   **{"secondary_weight":1,
#                    "primary_weight":1})
#dashTupleFromGraph(df,nx.kamada_kawai_layout,"Data/Graph_tests/",verbose=True,
#                   **{"secondary_weight":1,
#                    "primary_weight":0.5})
#dashTupleFromGraph(df,nx.kamada_kawai_layout,"Data/Graph_tests/",verbose=True,
#                   **{"secondary_weight":1,
#                    "primary_weight":0.1})
#%%
G = nx.Graph()
lv.populateGraph(G,df)
#%%WORK IN PROGRESS
#maxlen = 0
#for n in G.nodes():
#    if len(n)>naxlen:
#        maxlen = len(n)
#processed = []
#while len(processed) < 3637:
