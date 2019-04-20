#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:42:57 2019

@author: giovimax
"""

from Dash import dashify
import pickle
import networkx as nx
import datetime
now = datetime.datetime.now 
#%%
with open("Data/ggg", "b+r") as f:
    G = pickle.load(f)

#%%
prevTime = now()
print("Starting computing pos_shell",prevTime)
pos_shell = nx.shell_layout(G)
newTime = now()
print("Finished computing pos_shell",newTime,newTime-prevTime)
nx.set_node_attributes(G,pos_shell,name="pos")
prevTime = now()
print("Starting computing dashTuple_shell",prevTime)
dashTuple_shell = dashify(G)
newTime = now()
print("Finished computing dashTuple_shell",newTime,newTime-prevTime)
print("Saving...")
with open("Data/Graph_tests/dashTuple_shell","b+w") as file:
    pickle.dump(dashTuple_shell,file)
print("Saving Done!")

#%%
prevTime = now()
print("Starting computing pos_spring",prevTime)
pos_spring = nx.spring_layout(G)
newTime = now()
print("Finished computing pos_spring",newTime,newTime-prevTime)
nx.set_node_attributes(G,pos_spring,name="pos")
prevTime = now()
print("Starting computing dashTuple_spring",prevTime)
dashTuple_spring = dashify(G)
newTime = now()
print("Finished computing dashTuple_spring",newTime,newTime-prevTime)
print("Saving...")
with open("Data/Graph_tests/dashTuple_spring","b+w") as file:
    pickle.dump(dashTuple_spring,file)
print("Saving Done!")

#%%
prevTime = now()
print("Starting computing pos_spectral",prevTime)
pos_spectral = nx.spectral_layout(G)
newTime = now()
print("Finished computing pos_spectral",newTime,newTime-prevTime)
nx.set_node_attributes(G,pos_spectral,name="pos")
prevTime = now()
print("Starting computing dashTuple_spectral",prevTime)
dashTuple_spectral = dashify(G)
newTime = now()
print("Finished computing dashTuple_spectral",newTime,newTime-prevTime)
print("Saving...")
with open("Data/Graph_tests/dashTuple_spectral","b+w") as file:
    pickle.dump(dashTuple_spectral,file)
print("Saving Done!")
#%%
prevTime = now()
print("Starting computing pos_kamada_kawai",prevTime)
pos_kamada_kawai = nx.kamada_kawai_layout(G)
newTime = now()
print("Finished computing pos_kamada_kawai",newTime,newTime-prevTime)
nx.set_node_attributes(G,pos_kamada_kawai,name="pos")
prevTime = now()
print("Starting computing dashTuple_kamada_kawai",prevTime)
dashTuple_kamada_kawai = dashify(G)
newTime = now()
print("Finished computing dashTuple_kamada_kawai",newTime,newTime-prevTime)
print("Saving...")
with open("Data/Graph_tests/dashTuple_kamada_kawai","b+w") as file:
    pickle.dump(dashTuple_kamada_kawai,file)
print("Saving Done!")
