#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:56:43 2019

@author: giovimax
"""

import pickle 
from os import listdir
import pandas as pd
import LawVis as lv
import networkx as nx
#%%
#retrieving data and creating df
DataFolder = "Data/"
if "df" not in listdir(DataFolder):
    full_list = []
    for code in listdir(DataFolder):
        print("opening:%s..."%code)
        if ".codice" in code:
            print("Opening.")
            with open(DataFolder+code,"b+r") as file:
                data = pickle.load(file)
                full_list += data
                print("%s loaded."%code)
        else:
            print("Skipping.")
    print("Loading process done. Creating df")
    df = pd.DataFrame(full_list)
    print("Done.")
    #creating full file
    with open(DataFolder+"df","b+w") as file:
        print("Dumping...")
        pickle.dump(df,file)
        print("Done.")
    print("Creation finished.")
else:
    print("no df file, creating...")
    with open(DataFolder+"df","b+r") as file:
        
        df = pickle.load(file)
        print("Done.")
#%%
#populting network
        
#creating Graph opject
g = nx.Graph()

#cheching for RawToPathDict
RawToPathDict = None
if "RawToPathDict" not in listdir(DataFolder):
    print("RawToPathDict not in %s, creating..."%DataFolder)
    RawToPathDict = lv.genRawToPathDict(df)
    print("Dumping...")
    with open(DataFolder+"RawToPathDict","b+w") as file:
        pickle.dump(RawToPathDict,file)
        print("Dumping done.")
else:
    print("RawToPathDict in %s, loading..."%DataFolder)
    with open(DataFolder+"RawToPathDict","b+r") as file:
        RawToPathDict = pickle.load(file)
        print("Loading done.")

#actual population
print("Populating Graph...")
lv.populateGraph(g,df)
print("Done.")


        