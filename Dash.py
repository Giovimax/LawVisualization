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
def dashify(G,):
    """Creates objects for the dash app"""
    #original text of layout
    "Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>"
    #finds center of the graph
    dmin=1
    ncenter=[i for i in G.nodes][0]
    pos = nx.get_node_attributes(G,"pos")
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    #TODO:find out if p is usefull or not
    p=nx.single_source_shortest_path_length(G,ncenter)
    
    #EDGE TRACE
    #creating dataStructure
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')
        
    #TODO: Verify if it's worth using 
    #populationg
#    for edge in G.edges():
#        #gets coordinates of the two nodes
#        x0, y0 = G.node[edge[0]]['pos']
#        x1, y1 = G.node[edge[1]]['pos']
#        weight = G.edges[edge]["weight"]
#
#        #adds x,y data, 
#        #they pair since the index will be the same for x0,y0 and x1,y1
#        edge_trace['x'] += tuple([x0, x1, None])
#        edge_trace['y'] += tuple([y0, y1, None])

    
    #NODE TRACE
    #crating dataStructure
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
            size=5,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=1)))
    #ad hoc function to assign names
    def namer(node):
        name = G.nodes[node]["name"]
        if name != None:
            return name
        else:
            return node
    #populating 
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace["text"] += tuple([namer(node)])
    #TODO: Verify if it's worth using 
    #color and text
#    for node, adjacencies in enumerate(G.adjacency()):
#        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
##        node_info = '# of connections: '+str(len(adjacencies[1]))
#    #    node_trace['text']+=tuple([node_info])
#    #FIGURE, static 
    #creating toreturn components
    data=[edge_trace, node_trace]
    layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Test of the graphs",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    
    return (data,layout)

#%%
if __name__=="__main__":
#%%
#    data, layout = None, None
#    print("Cheching Data")
#    if "ggg"  in listdir("Data/"):
#        
#        print("no Data folder in working directory, doing calculations")
#        print("Loading graph from ggg...")
#        with open("Data/ggg","b+r") as f:
#            G = pickle.load(f)
#            print("ggg loaded.")
#        #%%
#        #graph
#    
#        
#        try:
#            print("trying loading pos")
#            with open("Data/posggg","b+r") as f:
#                pos = pickle.load(f)
#                print("posggg loaded")
#        except:
#            print("pos not found in Data/posggg, creating...")
#            print("generating graph")
#            pos = nx.drawing.layout.kamada_kawai_layout(G)
#            print("graph generated")
#            with open("Data/posggg","b+w") as f:
#                pickle.dump(pos,f)
#        finally:
#            print("posggg file management completed")
#                
#    
#        nx.set_node_attributes(G,pos,name="pos")
#        data, layout = dashify(G)
#    #%%
#    
#    else:
#        print("Data folder found, loading...")
#        for d in listdir("Data"):
#            print(d)
#            with open("Data/"+d,"b+r") as file:
#                print("opening",d)
#                a = pickle.load(file)
#                if d == "data":
#                    data = a
#                if d == 'layout':
#                    layout = a
#    #            else:
#    #                raise ValueError
#%%
    graphDict = dict()

#TO OPEN ALL FILES IN Data/Graph_tests
#    for i in listdir("Data/Graph_tests"):
#        if i != "log":
#            with open("Data/Graph_tests/%s"%i,"b+r") as f:
#                print("Loading %s"%i)
#                graphDict[i] = pickle.load(f)

    with open("Data/newMethodTestDash","b+r") as f:
        print("Loading...")
        graphDict["newMethodTestDash"] = pickle.load(f)
    

    #%%
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']#import style
    app = dash.Dash(external_stylesheets=external_stylesheets)
    app.layout = html.Div([
            html.H3("Test"),
            html.Div([
            dcc.Dropdown(id="graph_algorithm_selector",
                         options=[{"label":i,"value":i} for i in graphDict],
                         value = list(graphDict.keys())[0],
                         ),
                         ]),
            dcc.Graph(id="Graph",style={'height': 800},)
            ])
#%%
    @app.callback(
            Output(component_id="Graph",component_property="figure"),
            [Input(component_id="graph_algorithm_selector",component_property="value")],
            )
    def updateFigure(key):
        return {"data":graphDict[key][0],"layout":graphDict[key][1]}


    #%%
    app.run_server(debug=True)
