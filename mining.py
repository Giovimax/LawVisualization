#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:50:58 2019

@author: giovimax
"""

import requests as re 
import bs4 as bs
import LawVis as lv
import time
import datetime
import pickle 
now = datetime.datetime.now
#%%
def retrieveg_content(link):
    re_ = re.get(link)
    bs_ = bs.BeautifulSoup(re_.text,'html.parser')
    return bs_.find("div",class_="g_content")

def childFromParentFinder(child,parent):
    """finds out if parent is in child"""
    if parent in child:
        return True
    else:
        return False
def genChildFromParentFinder(parent):
    """builds a function that identifies if a child is from a specific parent"""
    parent_end = lv.clearLink(parent)[-1]
    def func(child):
        return childFromParentFinder(child,parent_end)
    return func


#%%
link_fonti = "https://www.brocardi.it/fonti.html"
bs_content_fonti = retrieveg_content(link_fonti)
bs_lista_fonti = bs_content_fonti.findAll("ul",class_="lista-fonti")
list_fonti_utili = bs_lista_fonti[:2]
list_href_fonti_utili = []
for i in list_fonti_utili:
    for j in i.findAll(href=True):
        list_href_fonti_utili.append(j)
list_href_fonti_utili = [i for i in map(lambda x: x["href"],list_href_fonti_utili)]

#%%
#testing on one instance
#l = list_href_fonti_utili[0]
#dominio = "https://www.brocardi.it"
#b_content = retrieveg_content(dominio+l)
#
#b_first_section_title = b_content.find("div",class_="section-title")
#
#c = b_first_section_title.find("a",href=True)["href"]
#
#c_content = retrieveg_content(dominio+c)
#
#find_c_child = genChildFromParentFinder(c)
#c_first_section_title = [i for i in map(lambda x: x["href"],c_content.findAll("a",href=find_c_child))]
#for i in c_first_section_title:
#    if ".html" in i:
#        print(i)
#        break
#%%
def firstLink(listaFonti,delay=0.1):
    dicttoret = {}
    dominio = "https://www.brocardi.it"
    def recursiveFristLinkSearch(fonte,tested = []):
        #print(fonte)
 
        def listChilds(fonte,):
            #link preparation
            dominio_fonte = None
            if dominio not in fonte:
                dominio_fonte = dominio + fonte
            else:
                dominio_fonte = fonte      
            #print(fonte)
            
            fonte_content = retrieveg_content(dominio_fonte)
            fonte_child_finder = genChildFromParentFinder(fonte)
            toret = [i for i in map(lambda x: x["href"],fonte_content.findAll("a",href=fonte_child_finder))]
            return toret
        
        fonte_list_childs = listChilds(fonte)
        time.sleep(delay)
        
        #print(fonte_list_childs)
        for i in fonte_list_childs:
            if i not in tested:
                tested.append(i)
                #print(i)
                if ".html" in i:
                    return i
                else:
                    toret = recursiveFristLinkSearch(i,tested)
                    if toret != False:
                        return toret
                    else:
                        return False
            else:
                pass
        else:
            return False
            
            
                
    for fonte in listaFonti:
        key = fonte.slpit("/")
        dicttoret[fonte] = recursiveFristLinkSearch(fonte)
    
    return dicttoret 

#%%
dictFonti = firstLink(list_href_fonti_utili)

#%%

def crawlCode(linkList):
    outputList=[]
    status = True
    while status:
#    for i in range(10):
        item = lv.crawlBoccardi(linkList[-1],raw = False, complex_=True)
        time.sleep(0.1)
        outputList.append(item[0])
        if item[1] == False:
            status = False
        else:
            linkList.append(item[1])
        print(item[0]["path"][-1])
    print("finished")
    return outputList

#%%
try:
    print("Trying opening log...")
    with open("log.txt","b+r") as f:
        log = pickle.load(f)
    print("log opend.")
    print(log)
except:
    print("log not present creating...")
    log = {k:False for k in dictFonti.keys()}



for code in dictFonti:
    if log[code] == False:
        codeName = code.replace("-","_")
        print("Crawling {}...".format(codeName))
        codeList = crawlCode([dictFonti[code]])
        print("Done. Creating file...")
        with open("Data/{}.codice".format(codeName)) as f:
            pickle.dump(codeList,f)
        print("File created. Updating log")
        log[code] = True
        with open("log.txt", "b+w") as f:
            pickle.dump(log,f)
        print("{} extraction completed.")
    else:
        print("{} already done, skipping...".format(code))
print("Done.")
