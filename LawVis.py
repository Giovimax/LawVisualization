#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:17:21 2019

@author: giovimax
"""
#%% IMPORTS
import bs4 as bs
import pandas as pd 
import requests as re
import networkx as nx 
#%% GUIDES
"""the proces from the df to the complete graph goes like this:
    1)create a rawToPatDict from the function genRawToPathDict
    2)create a graph object
    3)populate the graph using populateGraph
    4)run linksFromCommi to create non direct edges
    5)from Dash import dashify, data, layout = dashify(G)
    6) load and use
    """
#%%
def pp(*args,**kwargs):
    """Prints *args as the standard print but also appends an entry to the only 
    kwarg possible: "file", that is opend in append mode, also records the 
    time of the entry"""
    try:
        if "file" in kwargs:
            file = kwargs["file"]
    except:
        pass
    print(*args)
    with open(file,"a") as f:
        f.write("-Entry- "+str(now())+"\n")
        for a in args:
            f.write(str(a)+" ")
        else:
            f.write("\n")
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

def linkToTouples(link):
    """Takes the link and creates a LIST of TUPLES tha that is shaped like this:
        link = "/codice-di-procedura-civile/libro-primo/titolo-v/art112.html"
        out = [('codice-di-procedura-civile',),
         ('codice-di-procedura-civile', 'libro-primo'),
         ('codice-di-procedura-civile', 'libro-primo', 'titolo-v'),
         ('codice-di-procedura-civile', 'libro-primo', 'titolo-v', 'art112')]
        """
    clearLinkList = clearLink(link)#list of relevent items
    iterable = []
    for n, item in enumerate(clearLinkList):
        iterable.append(tuple(clearLinkList[:n+1]))
    return iterable

#%%
def addItemAsNode(G,link_or_tuple,ToPathDict,weight=1):
    """can take as a second argument a link that will be passed through the 
    function linkToTouples or directly the tuple generated by the same function
    """
    iterable = None #list of tuples, main dataStructure of the function
    #handling link or tuple matter
    if type(link_or_tuple) == str:
        #if link form, creates tuple
        iterable = linkToTouples(link_or_tuple)
    elif type(link_or_tuple) == list:
        #if already tuple, reanames
        iterable = link_or_tuple
    """i'm now using as a univoque node the full relevant path of each section 
    of the actutual path of the single object"""        
    for n, node in enumerate(iterable): #each tuple in the list can be a nodelinksFromCommi
        #for each possible node
        if node not in G.nodes:
            #name part
            name = None
            if node[-1] in ToPathDict: #sets the name as pretty name if possible
                name = ToPathDict[node[-1]]
            #adding node
            G.add_node(node,name=name)
            #creating edges
            if n != 0:
                G.add_edge(node,iterable[n-1],weight=weight)
            else:
                pass
#%%
#actual population of the network
def populateGraph(G,df,ToPathDict=None,weight=1,verbose=False):
    print("Starting to populate graph...")
    if ToPathDict == None:
        ToPathDict = genRawToPathDict(df)
    if verbose:
        print("Mode is verbose")
    for link in df["link"]:
        addItemAsNode(G,link,ToPathDict,weight)
        if verbose:
            print("added %s"%link)
    print("Finished populating.")

#%%
def linksFromCommi(g,df,rawToPatDict,weight=0.5):
    """the infamous function that creates lower ranked nodes from the links in 
    the text of each article"""
    for linkList, itemLink in zip(df["link_commi"],df["link"]):
        #takes the link to identify each article and its lunks from the text
        for linkFromList in linkList:#for each link in text
            #excludes irrelevant links
            if "dizionario" not in linkFromList:
                if "nota" not in linkFromList:
                    #the actual stuff
                    tupleFromLink = linkToTouples(linkFromList)#
                    #recreates the main path
                    if tupleFromLink[-1] not in g.nodes:
                        addItemAsNode(g,tupleFromLink,rawToPatDict)
                    else:
                        pass
                    g.add_edge(tupleFromLink[-1],linkToTouples(itemLink)[-1],weight=weight)
            pass
        pass

#%%
if __name__=="__main__":
    art1 = "https://www.brocardi.it/codice-civile/libro-primo/titolo-i/art1.html"
    
    pass