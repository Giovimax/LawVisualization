#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:17:21 2019

@author: giovimax
"""

import bs4 as bs
import pandas as pd 
import requests as re
import networkx as nx 


#%%

def crawlBoccardi(link,raw=True,links = True, complex_ = False):
    """function that takes the link of the page and returns a tuple with a 
    dict with the item and the next link"""
    #
    toret = dict()
    #
    re_page = re.get(link)
    bs_page = bs.BeautifulSoup(re_page.text,'html.parser')
    content = bs_page.find("div",class_="g_content")
    
    #estrazione del path
    breadcrumbContents = content.find("div",id="breadcrumb").findAll("span")[1:]
    path = []
    for i in breadcrumbContents:
        try:
            path.append(i.find("a").text)
        except:
            pass
    
    #
    commi = content.find("div",class_="corpoDelTesto dispositivo").findAll("p",class_="comma")
    note = content.findAll("div", class_="corpoDelTesto nota")

        #
    if links:
        link_commi, link_note = [] , []
        for i in commi:
            for j in i.find_all("a",href=True):
                link_commi.append(j["href"])
        for i in commi:
            for j in i.find_all("a",href=True):
                link_note.append(j["href"])
        toret["link_commi"] = link_commi
        toret["link_note"] = link_note
    
        #
    """bs4 objects make the serialization of objects impossible, in order to 
     temporarly work efficiently with test data, the option raw if 
     False converts the objects into strings"""   
    if not raw:
        commi = [i.text for i in commi]
        note = [i.text for i in note]
    else:
        pass
    
    #main toret
    toret["path"] = path
    toret["text"] = commi
    toret["notes"] = note
    toret["link"] = link
    
    #complex_
    if complex_:
        path_from_link = link.split("/")[3:]
        path_from_link[-1] = path_from_link[-1].split(".")[0]
        toret["path_from_link"] = path_from_link
    else:
        pass
    
    #for next_page
    try:
        next_page = "https://www.brocardi.it" + content.find("a",class_="navigazione-succ")["href"]
    except:
        print("no more pages")
        next_page = False
    #
    return (toret,next_page)

#%%
def clearLink(link,noExtension=True):
    """returns a cleaned list of each section of the link, also excludes 
    empty strings and deletes the extension at the end of the link"""
    l = link.split("/") 
    if 'www.brocardi.it' in l:
        l = l[3:]
    if l[0] == "":
        l = l[1:]
    else:
        pass
    if noExtension:
        l[-1] = l[-1].split(".")[0]
    else:
        pass
    for n,i in enumerate(l):
        if i == "":
            l.pop(n)
    return l

#%%
def genRawToPathDict(df):
    """take the df for one code and combines the well formatted names of 
    the code's sections from the page and the paths from the link.
    The Function returns a DICTIONARY stuctured -> "raw-path":"Clear Path"."""
    toret = dict()
    for i in range(len(df)):#for row in df
        path, link = df.loc[i,["path","link"]]#unpacks and assigns 
        #preparation 
        #cl
        cl = clearLink(link)#stands for clear link
        for n, i in enumerate(cl):
            if i == 'www.brocardi.it': #removes everything before and the domain 
                cl = cl[n+1:]
                break
        #path
        path = path[1:] #removes the useless part
        #main
        for k,v in zip(cl,path): 
            if k not in toret:
                toret[k] = v
    return toret

#%%
def rawToPath(rawlist,rawToPatDict): 
    #uses the rawToPatDict dict to substitute matching vals
    rawlistcopy = list(rawlist)
    for i, l in enumerate(rawlist):
        if l in rawToPatDict:
            rawlistcopy[i] = rawToPatDict[l]
        else:
            pass
    return rawlistcopy

#%%
def addItemAsNode(G,link,ToPatDict):
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
            if node[-1] in ToPatDict: #sets the name as pretty name if possible
                name = ToPatDict[node[-1]]
            #adding node
            G.add_node(node,name=name)
            #creating edges
            if n != 0:
                G.add_edge(node,iterable[n-1])
            else:
                pass
#%%
#actual population of the network
def populateGraph(G,df,verbose=False):
    print("Starting...")
    if verbose:
        print("Mode is verbose")
    for link in df["link"]:
        addItemAsNode(G,link)
        if verbose:
            print("added %s"%link)
    print("Finished.")
  

#%%
if __name__=="__main__":
    art1 = "https://www.brocardi.it/codice-civile/libro-primo/titolo-i/art1.html"
    
    pass