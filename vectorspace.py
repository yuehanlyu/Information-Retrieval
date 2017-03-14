from common.models import Document, Token 
from mining.decomposition import decompose
from common.tokenizer import getTokensFromText
from collections import Counter
#from querying.caching import retrieveFromCache 
#from querying.caching import saveToCache 
import re
#import numpy
import math 
import logging 
from email._header_value_parser import TokenList
logger = logging.getLogger("eventbook") 

''' This function is used to compute similarity between texts, in vectorspace
    How use this fucntion:
    
        >>>
        text1="today is a good cloudy day"
        text2="today is a good sunny day"
        docTexts=[]
        docTexts.append(text1)
        docTexts.append(text2)
        similarity=vcspace(docTexts)
        print(similarity)
        >>> [1.0, 0.75, 0.75, 1.0]
        # two texts has 2^2 combinations,
        # the entrance is calculated by formula 6-12 p.p124 IIR
        # I don't calculate term frequency, only count Boolean value. 
        For example, if text1 becomes"today is a good good cloudy day". It has the same vector as the original one.
'''
def vcspace(docTexts):    #original text, a set/list
    
    doclists=[]
    rowlists=[]
    #n=0
    tokenlist=[]
    for text in docTexts:
        text=decompose(text, False)  #every text becomes a list
        list=getTokensFromText(text)       
        doclists.append(list)
        for token in list:
            if token not in tokenlist:
                tokenlist.append(token)
        list=[]
        rowlists.append(list)
    
    for list in rowlists:  #initialize
        i=0
        for i in range(0,len(tokenlist)): 
            list.append(0)
        
    
    textNum=len(doclists) # number of rows
    tokenNum=len(tokenlist) # number of columns 
    i=0
    #print(tokenlist)
    
    n=-1
    for list in doclists:
        n=n+1
        for i in range(0,len(list)):
            if list[i] in tokenlist:
                index=tokenlist.index(list[i])
                rowlists[n][index]=rowlists[n][index]+1   

    k=0
    m=0
    Similarity=[]
    for list1 in rowlists:
        for list2 in rowlists:
            normText1=0
            normText2=0
            for k in range(0,tokenNum):
                normText1=normText1+list1[k]
                normText2=normText2+list2[k]
                #normText1=power(normText1,1.0/2)
                #normText2=power(normText2,1.0/2)
            normText1=normText1**(1./2)
            normText2=normText2**(1./2)
            Similarity.append(0)
            for k in range(0,tokenNum):
                Similarity[m]=Similarity[m]+list1[k]*list2[k]
            Similarity[m]=Similarity[m]/normText1/normText2
            #print(Similarity[m])
            m+=1
    
    return Similarity