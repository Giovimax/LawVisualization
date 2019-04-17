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


#%%
if __name__=="__main__":
    art1 = "https://www.brocardi.it/codice-civile/libro-primo/titolo-i/art1.html"
    
    pass