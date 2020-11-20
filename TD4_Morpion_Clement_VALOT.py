# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:18:32 2020

@author: valcr
"""
IA="O"
Human="X"
vide="-"
nbr_cases=[]

#On intialise une matrice (le morpion) de largeur 3 et de hauteur 3
#On a donc une liste de listes, chaque liste réprésentant une ligne
def Initialiser_Morpion(lignes, colonnes):
    nbr_cases.append(lignes*colonnes)
    morpion=[]
    for i in range (lignes):
        liste=[]
        for j in range (colonnes):
            liste.append(vide)
        morpion.append(liste)
    return morpion


#Simple méthode qui affiche le morpion.
#On crée notre string Affichage et on ajoute les valeurs du morpion avant de le
#retourner et de le print() pour l'afficher               
def Affichage(morpion):
    Affichage=""
    for i in range (len(morpion)):
        #Dès qu'on change de i, on change de ligne donc on saute une ligne avec \n
        Affichage+=("\n")
        for j in range (len(morpion[i])):
            Affichage+=morpion[i][j]
            #On met un espace entre chaque valeur du morpion
            Affichage+=" "
    return Affichage

#Compte le nombre de cases vides restantes dans le morpion
#Cette fonction va être utile pour repérer qui est en train de jouer (si c'est
#l'humain qui joue, alors on a un nombre pair de cases remplies (ou impair de 
#cases vides) et inversement si c'est l'humain); on peut également l'utiliser
#pour la fonction utility pour pondérer le choix de l'un ou l'autre par le 
#nombre de cases vides (plus il y a de cases vides à un état final, meilleure
#est l'utilité retournée)
def Count_cases_remplies(morpion):
    count=0
    for i in range (len(morpion)):
        for j in range (len(morpion[i])):
            if(morpion[i][j]!=vide):
                count+=1
    return count
    
#liste les actions possibles  
#Les actions possibles sont toutes les cases du morpion qui n'ont pas encore 
#été utilisées c'est à dire qui sont vides.
#On va retourner une liste de coordonnées valides
def Action (morpion):
    list_coord_valides=[]
    for i in range (len(morpion)):
        for j in range (len(morpion[i])):
            if(morpion[i][j]==vide):
                list_coord_valides.append([i,j])
    return list_coord_valides
   
             
#applique l'action dans l'etat donné du morpion
#action correspond aux coordonnées de la case à remplir
def Result(morpion,action):
    #On check d'abord si l'action fait bien partie des actions possibles
    if(action in Action(morpion)):
        #Cette variable représente le tour Imaginaire auquel cette action est
        #réalisée. On en a besoin pour déterminer quel joueur joue et ainsi 
        #déterminer quel symbole placer lors de cette action. On appelle cette
        #variable Imtour pour bien montrer que ce n'est pas le tour réel du jeu,
        #mais bien un tour imaginaire durant lequel le programme teste les
        #différentes possibilités de placement.
        Imtour=Count_cases_remplies(morpion)+1
        #On met +1 par souci de réalisme car le tour 0 n'existe pas.
        if(Imtour%2==1):
            morpion[action[0]][action[1]]=Human
        else:
            morpion[action[0]][action[1]]=IA
        return morpion

#Cette méthode est l'inverse de la méthode Result: elle place un vide à la position
#action. On en a besoin pour faire les tests de tous les différents choix que 
#peuvent faire l'Humain et l'IA. En effet, lorsque l'on teste différentes positions,
#on doit modifier le morpion pour aller plus loin dans l'hypothèse et atteindre
#un état final pour renvoyer une utilité. Mais lorsque l'on est allé au bout 
#d'une branche de l'arbre, il faut revenir en arrière pour tester d'autres 
#combinaisons. Mais comme on a modifié directement le morpion, on a plus en 
#mémoire son ancienne version et c'est pour cela qu'il nous suffit juste
#de lui enlever l'action qu'il vient de réaliser pour revenir à son état précédent.
def Undo(morpion, action):
    morpion[action[0]][action[1]]=vide
    return morpion
    

#test si s est terminal (fin de jeu)
#On a deux possibilités:
#   Soit le jeu se termine avec un gagnant et dans ce cas soit on a 3 symboles
#   consécutifs (différents de vide) sur une même ligne, colonne ou diagonale
#
#   Soit on a pas de gagnant et dans ce cas les neufs cases du morpion ne sont 
#   pas vides (remplis par X ou O)
def Terminal_Test(morpion):
    #On initialise donc Terminal à False et si on valide une des conditions,
    #on le change à True
    Terminal=False   
    if(Meme_Ligne(morpion)==True or
         Meme_Colonne(morpion)==True or
         Meme_Diagonale(morpion)==True):
        Terminal=True
    elif (Count_cases_remplies(morpion)==nbr_cases[0]):
        Terminal=True
    return Terminal

#Les 3 méthodes suivantes servent à la méthode Terminal_Test
def Meme_Ligne(morpion):
    Terminal=False
    for i in range (0,len(morpion)):
        if(morpion[i][0]!=vide and 
           morpion[i][0]==morpion[i][1] and 
           morpion[i][1]==morpion[i][2]):
            Terminal=True
            break
    return Terminal  

def Meme_Colonne(morpion):
    Terminal=False
    for j in range (0,len(morpion)):
        if(morpion[0][j]!=vide and 
           morpion[0][j]==morpion[1][j] and 
           morpion[1][j]==morpion[2][j]):
            Terminal=True
            break
    return Terminal

def Meme_Diagonale(morpion):
    Terminal=False  
    if(morpion[0][0]!=vide and 
       morpion[0][0]==morpion[1][1] and 
       morpion[1][1]==morpion[2][2]):
        Terminal=True
    elif(morpion[0][2]!=vide and 
         morpion[0][2]==morpion[1][1] and 
         morpion[1][1]==morpion[2][0]):
        Terminal=True
    return Terminal
    

#attribue une valeur à l'etat du morpion
def Utility(morpion, joueur):
    utility=0
    #S'il y a un gagnant, on pondère l'utilité avec le nombre de cases vides 
    #restantes car plus il y en a, plus les choix ont été efficients pour l'un
    #ou l'autre des joueurs
    if((Meme_Ligne(morpion)==True or 
        Meme_Colonne(morpion)==True or 
        Meme_Diagonale(morpion)==True) and 
        joueur==IA):
        utility=-1*(nbr_cases[0]+1-Count_cases_remplies(morpion))
    elif((Meme_Ligne(morpion)==True or
         Meme_Colonne(morpion)==True or
         Meme_Diagonale(morpion)==True) and
         joueur==Human):
        utility=1*(nbr_cases[0]+1-Count_cases_remplies(morpion))
    #Si aucune des conditions si dessus n'a été rencontrées et que le morpion
    #n'a plus de cases vides, alors il y a égalité
    elif (Count_cases_remplies(morpion)==nbr_cases[0]):
        #Aucun gagnant donc utilité nulle 
        utility=0
    return utility

#cette méthode peut renvoyer plusieurs choses:
#   Dans un premier temps, si l'état du morpion est final, elle renvoie une 
#utilité relative à cet état
#   Dans un second temps, si l'état n'est pas final et qu'on est à une profondeur
#d'arbre supérieure à 1, elle renvoie la valeur de Max
#   Enfin, si l'état n'est pas final et qu'on est à la profondeur 1, elle renvoie
#la valeur de l'action correspondant au plus grand max trouvé. Pour ce faire, 
#on met en paramètre return_action définit par défault sur False et lorsque l'on 
#appelle pour la première fois cette méthode dans MiniMax, on met true en paramètres;
#et lorsque l'on appelle Min_Value et Max_Value par récurrence, on ne met rien.
def Max_Value(morpion, A, B, return_action=False):
    if(Terminal_Test(morpion)==True):
        return Utility(morpion, IA)
    #On définit le Max comme le négatif du nombre total de cases du morpion
    Max=-nbr_cases[0]
    #On parcourt chaque action possible du morpion
    for action in Action(morpion):
        value_temp=int(Min_Value(Result(morpion, action), A, B))
        #Si notre valeur temporaire issue de Min_Value est supérieure à notre 
        #Max, alors Max prend la valeur de cette valeur temporaire et next_move
        #prend la valeur de l'action dont on étudie l'utilité (on ne renvoie
        #cette valeur de l'action que si on est à la profondeur 1 de l'arbre)
        if(Max<value_temp):
            Max=value_temp
            next_move=action
        #Pour revenir à l'état précédent
        Undo(morpion, action)
        #Elagage alpha-Beta
        A=max(A,Max)
        if(Max>=B):
            return Max 
    if(return_action):
        return next_move
    return Max

#cette méthode peut renvoyer plusieurs choses:
#   Dans un premier temps, si l'état du morpion est final, elle renvoie une 
#utilité relative à cet état
#   Dans un second temps, si l'état n'est pas final et qu'on est à une profondeur
#d'arbre supérieure à 1, elle renvoie la valeur de Min
#   Enfin, si l'état n'est pas final et qu'on est à la profondeur 1, elle renvoie
#la valeur de l'action correspondant au plus petit min trouvé. Pour ce faire, 
#on met en paramètre return_action définit par défault sur False et lorsque l'on 
#appelle pour la première fois cette méthode dans MiniMax, on met true en paramètres;
#et lorsque l'on appelle Min_Value et Max_Value par récurrence, on ne met rien.
def Min_Value(morpion, A, B, return_action=False):
    if(Terminal_Test(morpion)==True):
        #Etant donné que lorsque l'on rentre dans Min_Value, on a fait le Result
        #du morpion en ajoutant une X pour l'humain
        return Utility(morpion, Human)
    #On définit le Min comme le nombre total de cases du morpion
    Min=nbr_cases[0]
    #On parcourt chaque action possible du morpion
    for action in Action(morpion):
        value_temp=int(Max_Value(Result(morpion, action), A, B))
        #Si notre valeur temporaire issue de Max_Value est inférieure à notre 
        #Min, alors Min prend la valeur de cette valeur temporaire et next_move
        #prend la valeur de l'action dont on étudie l'utilité (on ne renvoie
        #cette valeur de l'action que si on est à la profondeur 1 de l'arbre)
        if(Min>value_temp):
            Min=value_temp
            next_move=action
        
        Undo(morpion,action)
        #Elagage alpha-Beta
        B=max(B, Min)        
        if(Min<=A):
            return Min   
    if(return_action):
        return next_move
    return Min

#MiniMax va choisir, en fonction de Joueur (rentré en paramètre) laquelle des
#deux fonctions effectuer
def MiniMax(morpion, Joueur):
    if(Joueur==Human):
        return Max_Value(morpion, -nbr_cases[0], nbr_cases[0], True)
    elif(Joueur==IA):
        return Min_Value(morpion, -nbr_cases[0], nbr_cases[0], True)

if __name__=='__main__' :
    morpion=Initialiser_Morpion(3, 3)
    #morpion=[['O','X','-'],['-','-','-'],['-','X','-']]
    tour=1
    while(Terminal_Test(morpion)==False):
        #Pour choisir si on veut jouer avec les X ou les O, il suffit de changer
        #la valeur à laquelle doit être égale tour modulo 2:
        # 0 si on veut joueur en premier avec les X
        # 1 si on veut joueur en deuxième avec les O
        if(tour%2==0):joueur=IA
        else: joueur=Human
        print("tour:",tour)
        if(joueur==Human):
            #On suggère le meilleur move possible
            print("Le meilleur play serait de placer la X à la position ",
                  MiniMax(morpion,joueur))
            print("Où voulez-vous placer le X?")
            print("Entrez le numéro de ligne")
            ligne=int(input())
            print("Entrez le numéro de colonne")
            colonne=int(input())
            #Si les coordonnées rentrées par l'utilisateur ne font pas partie
            #des actions possibles, on les lui redemande 
            while([ligne,colonne] not in Action(morpion)):
                print("Ces coordonnées ne sont pas valides.")
                print("Entrez le numéro de ligne")
                ligne=int(input())
                print("Entrez le numéro de colonne")
                colonne=int(input())
            Result(morpion, [ligne,colonne])
        else:
            Result(morpion,MiniMax(morpion, joueur))
        print(Affichage(morpion))
        tour=tour+1
    #On affiche un message de fin 
    if(Utility(morpion, joueur)>0):
        print("Les X ont gagné !!")
    elif(Utility(morpion, joueur)<0):
        print("Les O ont gagné !!")
    else:
        print("Personne n'a gagné...")
    
    