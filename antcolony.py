import numpy as np
from numpy.random import choice as np_choice
class Antcolony(object):
    def _init_(self,distances_table,ants_number,ro,alpha,beta):
        self.distances_table=distances_table
        self.ants_number=ants_number
        self.ro=ro
        self.alpha=alpha
        self.beta=beta

    def gen_paths(self):
        length = len(self.distances_table)
        L = []
        for k in range(0, length):
            L.append(k)
        ret=[]
        start=0
        L.pop(0)
        ret=L
        paths=[]
        paths1=[]
        leng=len(ret)
        for k in range(0,self.ants_number):
            path=[]
            path.append(start)
            while ret!=[]:
                ind=np_choice(np.array(ret),1)
                indice=ret.index(ind)
                path.append(ret[indice])
                ret.pop(indice)
            path.append(start)
            paths.append(path)
            for j in range (1,len(self.distances_table)):
                ret.append(j)
        for k in paths:
            path1=[]
            l=len(k)
            for j in range (0,l-1):
                kha=(k[j],k[j+1])
                path1.append(kha)
            paths1.append(path1)
        print('the paths of the '+str(self.ants_number) +' that exist :')
        print(paths1)
        return paths1
    def pheromones_matrix(self):
        length=len(self.distances_table)
        T=np.ones((length,length))
        L=self.gen_paths()
        M=self.distances_table
        table=[]
        count=0
        for k in L:
            distance=0
            for j in k:
                a=j[0]
                b=j[1]
                distance=distance+1/self.distances_table[a][b]
            table.append(distance)
        for k in L:
            for j in k:
                a=j[0]
                b=j[1]
                T[a][b]=T[a][b]*(1-self.ro)+table[count]
            count=count+1
        print('the pheromone matrix:')
        print(T)
        return T
    def run(self):
        phromones=self.pheromones_matrix()     #lappel de la fct pheromones
        distances=self.distances_table         #lappel de la matrice des distance
        start=0
        L=[]
        chemin=[]
        path=[]
        chemin.append(start)
        for k in range(0,len(self.distances_table)):    #on met les noeud existent dans une table
            L.append(k)
        indice = L.index(start)
        L.pop(indice)   #on elimine le zero car cest le noeud de commancement
        while L!=[]:
            probabilite=0    #initialisation de la probalibilite a calculer pour chaque deplacement
            liste=[]
            somme=0     #initialisation de la somme
            for k in L:      #le calcule de la somme exitent dans le denominateur
                somme=somme+(phromones[start][k]*self.alpha)*1/(distances[start][k]*self.beta)
            for j in L:  #le calcule de la probabilite de deplacement pour chaque noeud allouer
                probabilite=(1/somme)(phromones[start][j]self.alpha)*1/(distances[start][k]*self.beta)
                z=(probabilite,j)
                liste.append(z)    #on met ala table liste le tuple probabilite et le numero du  noeud
            for i in range(0,len(liste)-1):
                for s in range(i+1,len(liste)): #on fait un tri dont on met le tuble qui a la probabilite la plus grande a lindex 0
                    if liste[i][0]<liste[s][0]:
                        liste[i],liste[s]=liste[s],liste[i]
            start=liste[0][1]   #lorsque le tri est fait on prend le numero du noeud de la probabilite la plus grande
            indice=L.index(start)
            chemin.append(start) #on la met a la list chemin
            L.pop(indice) #puis on la elimine de la liste L qui contien les noeuds
        chemin.append(0) # puis on ajoute zero car cest la fin du chemin et la fourmi doit revenir ala premiere place
        for k in range(0,len(chemin)-1):
            z=(chemin[k],chemin[k+1]) #on rend la liste de deolacement sous forme des tuple pour qu'elle soit lisible
            path.append(z)
        print("the chemin is")
        print(path)
        return path
#la creation de notre matrice de temps
import pandas as pd
import numpy as np
df = pd.read_excel("C:\\Users\\21265\\Downloads\\Classeur1.xlsx")
set_up = np.array(pd.DataFrame(df, columns= ['set up time']))
recovery = np.array(pd.DataFrame(df, columns= ['recovery time']))
surgery = np.array(pd.DataFrame(df, columns= ['surgery duration']))
print (len(set_up))
somme=0
distance=[]
for i in range (0,44):
    somme=set_up[i]+recovery[i]+surgery[i]
    distance.append(somme)
print(distance)
matrice_distance=np.ones((44, 44))
for i in range(0,44):
    for j in range(0,44):
        if i==j:
            matrice_distance[i][j]=0
        else:
            matrice_distance[i][j]=distance[i]
print(matrice_distance)
#le test
ant=Antcolony(matrice_distance,100,0.5,1,5)
ant.run()