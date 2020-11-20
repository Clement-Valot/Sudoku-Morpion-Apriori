# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:00:19 2020

@author: valcr
"""
def Apriori():
    tab=[[1,2,5],[1,3,5],[1,2],[1,2,3,4,5],[1,2,4,5],[2,3,5],[1,5]]
    itemset=[[1],[2],[3],[4],[5]]
    nbr_singletons=len(itemset)
    while (len(itemset)!=0):
        Occur=Occurences(tab,itemset)
        RealItemset=Regle(Occur,itemset,3)
        if(len(itemset)!=0):
            Final_itemset=list(RealItemset)
        itemset=CreerCouples(RealItemset, nbr_singletons)         
    print(Final_itemset)


def CreerCouples(itemset, nbr_singletons): 
    All_itemset=[]
    for i in range (0,len(itemset)): # On parcourt chaque singleton de l'itemset (1,2,3,4 et 5) 
        for j in range (i+1, nbr_singletons+1):
            tab=list(itemset[i])
            if(Absence(itemset[i],j)==True): #On vérifie si on ne répète pas un même chiffre dans un ensemble
                if(len(tab)>1):
                    if(j>tab[-1]):
                        tab.append(j)
                        All_itemset.append(tab)
                else:
                    tab.append(j)
                    All_itemset.append(tab)              
    return All_itemset

def Absence(tab,j): #Vérifie si un chiffre appartient déjà à l'ensemble pour éviter les répétitions
    Abs=True
    for i in range(0,len(tab)):
        if(j==tab[i]):
            Abs=False
    return Abs
        
def Occurences(tab,itemset): # Compte le nombre d'occurences d'un ensemble de itemset dans tab
    Occu=[]
    for i in range (0,len(itemset)):
        k=0
        for j in range (0,len(tab)):
            if(ElementIn(itemset[i],tab[j])==True):
                 k=k+1
        Occu.append(k)
    return Occu # retourne un tableau d'entiers : le premier correspond au nombre de fois
                # où l'on retrouve le premier élément d'itemset dans tab     

def ElementIn(Element,tab): # Vérifie si Element appartient bien à tab
    In=False # On commence par égaliser In à False
    k=0 # k va correspondre au nombre de fois qu'un chiffre de Element est trouvé dans tab
    for i in range (0,len(Element)):
        for j in range (0,len(tab)):
            if(Element[i]==tab[j]):
                k=k+1 # Si un chiffre de Element est trouvé dans tab, on incrémente k
                if(k==len(Element)): # SI k est égal à la taille de Element, cela signifie
                    In=True         # que tous les chiffres de Element sont dans tab
                    break           # donc Element appartient bien a tab
        if(k==len(Element)): 
            break  # On sait déjà que Element appartient à tab donc on break pour sortir           
    return In      # de la première boucle for

def Regle(Occu,itemset, Eps): # On vérifie si les ensembles d'itemset vérifie la règle
    RealItemset=[] # On crée un nouveau tableau qui contiendra les bonnes valeurs d'itemset
    for i in range (0,len(Occu)): #On parcourt la table d'occurence des ensembles d'itemset
        if(Occu[i]>=Eps): #Si l'occurence est supérieure ou égale à une valeur fixée (=3)
            RealItemset.append(itemset[i]) #Alors on place cette valeur d'itemset dans RealItemset
    return RealItemset
        
    
if __name__=='__main__' :
    Apriori()
    