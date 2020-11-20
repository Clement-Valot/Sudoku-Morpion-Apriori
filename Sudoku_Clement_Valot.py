# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:38:57 2020

@author: valcr
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random

from ortools.sat.python import cp_model

def Coloration():
    model = cp_model.CpModel()
    
    NSW=model.NewIntVar(1,3,'NSW')
    V=model.NewIntVar(1,3,'V')
    NT=model.NewIntVar(1, 3,'NT')
    WA=model.NewIntVar(1,3,'WA')
    Q=model.NewIntVar(1,3,'Q')
    SA=model.NewIntVar(1,3,'SA')
    
    model.Add(NSW!=Q)
    model.Add(NSW!=SA)
    model.Add(NSW!=V)
    model.Add(SA!=Q)
    model.Add(SA!=NT)
    model.Add(SA!=V)
    model.Add(SA!=WA)
    model.Add(WA!=NT)
    model.Add(NT!=Q)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
        print('NSW: %i' % solver.Value(NSW))
        print('V: %i' % solver.Value(V))
        print('NT: %i' % solver.Value(NT))
        print('Q: %i' % solver.Value(Q))
        print('WA: %i' % solver.Value(WA))
        print('SA: %i' % solver.Value(SA))

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count 
    
def message_crypte():
    model = cp_model.CpModel()
    M=model.NewIntVar(0,9,'M')
    O=model.NewIntVar(0,9,'O')
    N=model.NewIntVar(0,9,'N')
    E=model.NewIntVar(0,9,'E')
    Y=model.NewIntVar(0,9,'Y')
    S=model.NewIntVar(0,9,'S')
    R=model.NewIntVar(0,9,'R')
    D=model.NewIntVar(0,9,'D')
    
    model.Add(1000*(S+M)+100*(E+O)+10*(N+R)+E+D==10000*M+1000*O+100*N+10*E+Y)
    model.AddAllDifferent([M,O,N,E,Y,S,R,D])
    
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([M,O,N,E,Y,S,R,D])
    status = solver.SearchForAllSolutions(model, solution_printer)
    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())
   
def Reines(echec_dim):
    model = cp_model.CpModel()
    queens=[model.NewIntVar(0,echec_dim-1,'Q%i' % i) for i in range (1,echec_dim+1)]
    
    model.AddAllDifferent(queens)
    for i in range(echec_dim):
    # Note: is not used in the inner loop.
        diag1=[]
        diag2=[]
        for j in range(echec_dim):
            # Create variable array for queens(j) + j.
            q1 = model.NewIntVar(0, 2 * echec_dim, 'diag1_%i' % i)
            diag1.append(q1)
            model.Add(q1 == queens[j] + j)
            # Create variable array for queens(j) - j.
            q2 = model.NewIntVar(-echec_dim, echec_dim, 'diag2_%i' % i)
            diag2.append(q2)
            model.Add(q2 == queens[j] - j)
        model.AddAllDifferent(diag1)
        model.AddAllDifferent(diag2)
    
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(queens)
    status = solver.SearchForAllSolutions(model, solution_printer)
    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())

class VarArraySolutionPrinterSudoku(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__limit=limit
        self.__solution_count = 0
        self.grille_solved=[]

    def on_solution_callback(self):
        self.__solution_count += 1
        if (self.__solution_count>=self.__limit):
            for v in self.__variables:
                self.grille_solved.append(self.Value(v))
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count 

#Méthode qui va initialiser les variables et les contraintes de notre problème
#de Sudoku. Elle prend en paramètres notre grille, sa taille ainsi que le modèle
def var_constraints(grille,taille,model):
    
    for i in range (taille):
        for j in range (taille):
            if(grille[i][j]==0):
                grille[i][j]=model.NewIntVar(1,taille,'')
    
    #Contrainte: tous les chiffres d'une même ligne sont différents            
    for i in range (taille):
        model.AddAllDifferent(grille[i])
     
    #Contrainte: tous les chiffres d'une colonne sont différents
    for j in range (taille):
        #On crée une liste vide qui contiendra tous les chiffres de la colonne
        col=[]
        for i in range (taille):
            #On fait varier l'indice de la ligne sans faire varier la colonne
            col.append(grille[i][j])
        model.AddAllDifferent(col)
    
    #Contrainte: tous les chiffres d'une cellule (carré 3*3) sont différents 
    for i in range (0,taille,3):
        for j in range (0,taille,3):
            cel=[]
            cel.append(grille[i][j])
            cel.append(grille[i][j+1])
            cel.append(grille[i][j+2])
            cel.append(grille[i+1][j])
            cel.append(grille[i+1][j+1])
            cel.append(grille[i+1][j+2])
            cel.append(grille[i+2][j])
            cel.append(grille[i+2][j+1])
            cel.append(grille[i+2][j+2])
            model.AddAllDifferent(cel)         
              
def Sudoku(grille):
    model = cp_model.CpModel()
    
    taille=len(grille)
    var_constraints(grille, taille, model) 
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
        #On affiche la solution si elle existe
        for i in range (taille):
            for j in range (taille):
                if(j==taille-1):
                    print(solver.Value(grille[i][j]))
                else:
                    print(solver.Value(grille[i][j]), end=',')

def Initialiser_grille():
    #On initialise le niveau de difficulté à -1
    difficulte=-1
    #Tant que l'utilisateur ne rentre pas un niveau de difficulté valide
    # (1,2,3,4 ou 5), on lui redemande le niveau de difficulté souhaité
    while(difficulte not in [1,2,3,4,5]):
        difficulte=int(input("Quel niveau de difficulté souhaitez-vous?\n"+
                         "1- Débutant\n"+
                         "2- Facile\n"+
                         "3- Moyen\n"+
                         "4- Difficile\n"+
                         "5- Expert\n"))
    
    #On met la taille de notre tableau à 9
    taille=9
    #On initialise notre table de sudoku en la remplissant de 0
    for i in range (taille):
        for j in range (taille):
            grille[i][j]=0
    
    #On crée le modèle
    model=cp_model.CpModel()
    #On applique les variables et les contraintes
    var_constraints(grille, taille, model)

    #Pour correspondre aux paramètres de la classe, on met les valeurs de la 
    #grille dans une simple liste
    list_entiers=[]
    for line in range(taille):
        for col in range(taille):
            list_entiers.append(grille[line][col])
            
    #On cherche une solution au problème
    solver = cp_model.CpSolver()
    #Etant donné que ortools ressort toujours la même solution de sudoku si on
    #lui donne une grille de 0, il faut que l'on trouve plein de solutions 
    #différentes et qu'on en choisisse une aléatoirement.
    #On fixe notre valeur limite aléatoire
    limit= random.randint(100,5000)
    #On va calculer des solutions différentes du sudoku et les mettre dans une
    # matrice grille à chaque fois (grille_solved) jusqu'à que le nombre de 
    #solutions trouvées dépasse le nombre limit entré en paramètre
    solution_printer = VarArraySolutionPrinterSudoku(list_entiers, limit)
    solver.SearchForAllSolutions(model, solution_printer)
    
    #On remplit notre grille avec les valeurs solutions de grille_solved
    k=0
    for i in range (taille):
        for j in range (taille):
            grille[i][j]=solution_printer.grille_solved[k]
            k+=1
    print()
    
    #On distingue les 5 cas selon le niveau de difficultés choisi
    if(difficulte==1):
        cases_donnees=50
    elif(difficulte==2):
        cases_donnees=40
    elif(difficulte==3):
        cases_donnees=33
    elif(difficulte==4):
        cases_donnees=26
    elif(difficulte==5):
        cases_donnees=17
        
    #le nombre de zéros correspond au nombre de cases total du sudoku (81)
    #moins le nombre de cases données selon le niveau de difficulté
    nbr_zero=81-cases_donnees
    #On crée une liste qui contiendra les coordonnées des cases du sudoku
    #déjà changées en 0 pour éviter de changer 2 fois la même case en 0 et
    #ainsi ne pas avoir un nombre de cases données supérieures à la quantité
    #exigée par le niveau de difficulté
    cases_remplies=[]
    while(nbr_zero>0):
        #On prend des coordonnées de lignes et colonnes aléatoires entre 0 et 8
        i=random.randint(0,8)
        j=random.randint(0,8)
        if([i,j] not in cases_remplies):
            #On rajoute ces coordonnées à la liste des cases déjà changées
            cases_remplies.append([i,j])
            #Puis on change cette case à 0
            grille[i][j]=0
            #On décremente pour la boucle while
            nbr_zero-=1    
    
    #On affiche la grille de sudoku à résoudre c'est à dire avec les cases
    #manquantes
    print()            
    print('Grille de Sudoku n°%i :' % solution_printer.solution_count())
    for i in range (taille):
        for j in range (taille):
            if(j==taille-1):
                print(grille[i][j])
            else:
                print(grille[i][j], end=' ')
                
    #Puis on affiche si l'utilisateur le souhaite, la solution
    print()
    solution=input("Pour afficher la solution, entrez S: ")
    k=0
    if(solution=="S" or solution=="s"):
        for i in range (taille):
            for j in range (taille):
                if(j==taille-1):
                    print(solution_printer.grille_solved[k])
                else:
                    print(solution_printer.grille_solved[k], end=' ')
                k+=1
    else:
        print('Bonne chance!')
                    
if __name__=='__main__' :
    #Coloration()
    #message_crypte()
    #Reines(8)
    grille=[[0,0,5,9,0,0,0,2,0],
            [0,7,0,4,0,0,5,0,0],
            [0,0,9,0,0,0,4,0,3],
            [4,0,2,0,0,0,7,0,0],
            [0,0,0,0,0,1,0,5,0],
            [0,3,0,0,0,6,8,0,0],
            [0,0,0,0,2,0,6,0,0],
            [2,0,0,1,0,8,0,0,5],
            [0,0,7,0,3,0,0,0,0]]
    #Sudoku(grille)
    Initialiser_grille()
        