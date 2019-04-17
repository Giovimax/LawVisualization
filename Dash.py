#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 21:59:53 2019

@author: giovimax
"""

import plotly.plotly as py
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from json import dumps #testing selection
import networkx as nx
import pandas as pd
import pickle
from os import listdir


#%%

data, layout = None, None
print("Cheching Data")
if "Data" not in listdir():
    
    print("no Data folder in working directory, doing calculations")
    print("Loading graph from gg...")
    with open("gg","b+r") as f:
        G = pickle.load(f)
        print("gg loaded.")
    #%%
    #graph

    
    try:
        print("trying loading pos")
        with open("Data/pos","b+r") as f:
            pos = pickle.load(f)
            print("pos loaded")
    except:
        print("pos not found in Data/pos, creating...")
        print("generating graph")
        pos = nx.drawing.layout.kamada_kawai_layout(G)
        print("graph generated")
        with open("Data/pos","b+w") as f:
            pickle.dump(pos,f)
    finally:
        print("pos file management completed")
            

    nx.set_node_attributes(G,pos,name="pos")
    
    dmin=1
    ncenter=[i for i in G.nodes][0]
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    
    p=nx.single_source_shortest_path_length(G,ncenter)
    
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')
    
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
    
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
    #    hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))
    
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace["text"] += tuple([G.nodes[node]["name"]])
        
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = '# of connections: '+str(len(adjacencies[1]))
    #    node_trace['text']+=tuple([node_info])
        
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    #%%    
    data=[edge_trace, node_trace]
    layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
else:
    print("Data folder found, loading...")
    for d in listdir("Data"):
        print(d)
        with open("Data/"+d,"b+r") as file:
            print("opening",d)
            a = pickle.load(file)
            if d == "data":
                data = a
            if d == 'layout':
                layout = a
#            else:
#                raise ValueError
#%%
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']#import style
app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
        html.H3("Test"),
        dcc.Graph(figure={"data":data,"layout":layout},style={'height': 800},)
        ])
#%%
app.run_server(debug=True)
