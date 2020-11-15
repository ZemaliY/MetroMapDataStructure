#! /usr/local/bin/python
# -*- coding: utf_8 -*-

# import dijkstra
import math
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

##IMPLEMENTATION GRAPHE
class Graphe(object):
    def __init__(self):
        self.graphe = {}

    def ajouteSommet(self, sommet):
        if sommet not in self.graphe.keys():
            self.graphe[sommet] = {}

    def ajouteArrete(self, sommet, sommetVoisin, p):
        if sommet != sommetVoisin:
            try:
                self.graphe[sommetVoisin][sommet] = p
                self.graphe[sommet][sommetVoisin] = p
            except KeyError:
                pass

    def __plotnetwork__(self):
        edgelist = pd.read_csv('GothamCityRail.csv')
        g = nx.Graph()
        for i, elrow in edgelist.iterrows():
            g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())
        # Edge list example
        print(elrow[0])  # node1
        print(elrow[1])  # node2
        print(elrow[2:].to_dict())
        nx.draw(g, with_labels=True, create_using=nx.DiGraph())
        plt.show()

    def getListArreteTrie(self):
        trie=[]
        for sommet in self.graphe:
            for sommet_connection in self.graphe[sommet]:
                if (sommet,sommet_connection,self.graphe[sommet][sommet_connection]) not in trie and (sommet_connection,sommet,self.graphe[sommet][sommet_connection]) not in trie :
                    trie.append((sommet,sommet_connection,self.graphe[sommet][sommet_connection]))
        return sorted(trie, key=lambda item: item[2])

    def __eq__(self, graphe1):
        return self.graphe == graphe1

    def __str__(self):
        return repr(self.graphe)

    def __repr__(self):
        return repr(self.graphe)

#IMPLEMENTATION BINARY TREE
class Node:
    def __init__(self,value,nom):
        self.left = None
        self.right = None
        self.ID = value
        self.name=nom



def insert(root, node):
    if root is None:
        root = node
    else:
        if root.ID < node.ID:
            if root.right is None:
                root.right = node
            else:
                insert(root.right, node)
        else:
            if root.left is None:
                root.left = node
            else:
                insert(root.left, node)

def inorder(root):
    if root:
        inorder(root.left)
        print(str(root.ID)+':'+root.name)
        inorder(root.right)

def search(root, value):
    if root is None or root.ID == value:
        return (str(root.ID)+':'+root.name)
    if root.ID < value:
        return search(root.right, value)
    return search(root.left, value)




#IMPLEMENTATION AVL TREE:

class TreeNode(object):
    def __init__(self, value,nom):
        self.ID = value
        self.name=nom
        self.left = None
        self.right = None
        self.height = 1

class AVL_Tree(object):
    def insert(self, root, valeur,nom):
        if not root:
            return TreeNode(valeur,nom)
        elif valeur < root.ID:
            root.left = self.insert(root.left, valeur,nom)
        else:
            root.right = self.insert(root.right, valeur,nom)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        balance = self.getBalance(root)
        if balance > 1 and valeur < root.left.ID:
            return self.rightRotate(root)
        if balance < -1 and valeur > root.right.ID:
            return self.leftRotate(root)
        if balance > 1 and valeur > root.left.ID:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and valeur < root.right.ID:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):

        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def rightRotate(self, z):

        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):

        if not root:
            return
        print("{0} ".format(str(root.ID)+':'+root.name), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def inorderAVL(self,root):
        if root:
            self.inorderAVL(root.left)
            print(str(root.ID) + ':' + root.name)
            self.inorderAVL(root.right)

#IMPLEMENTATION DJIKSTRA

def dijkstra(matrice, start):
    infini = sum(sum(ligne) for ligne in matrice) + 1
    nb_sommet = len(matrice)

    s_connu = {start : [0,[start]]}
    s_inconnu = {k : [infini, ''] for k in range(nb_sommet) if k != start }

    for suivant in range(nb_sommet):
        if matrice[start][suivant]:

            s_inconnu[suivant] = [matrice[start][suivant], start]

    print('Dans le graphe d\'origine {} de matrice d\'adjacence:'.format(start))
    for ligne in matrice:
        print(ligne)
    print()
    print('Plus court chemins trouvé grace a Dijkstra de ')

    while s_inconnu and any(s_inconnu[k][0] < infini for k in s_inconnu):
        u = min(s_inconnu, key = s_inconnu.get)
        longueur_u, precedent_u = s_inconnu[u]
        for v in range(nb_sommet):
            if matrice[u][v] and v in s_inconnu:
                d = longueur_u + matrice[u][v]
                if d < s_inconnu[v][0]:
                    s_inconnu[v] = [d, u]
        s_connu[u] = [longueur_u, s_connu[precedent_u][1] + [u]]
        del s_inconnu[u]
        print('longueur', longueur_u, ':', ' -> '.join(map(str, s_connu[u][1])))

    for k in s_inconnu:
        print('Il n\' y a pas de chemin de {} à {}.'.format(start, k ))

    return s_connu


#IMPLEMENTATION DATABASE LINEAIRE
def recherche(l,id):
    for s in l:
        if(s[0]==id):
            return s
    print('ID not in the list')

def recherche_dicho(l, id):
    a = 0
    b = len(l)-1
    m = (a+b)//2
    while a < b :
        if l[m][0]== id :
            return l[m]
        elif l[m][0] > id:
            b = m-1
        else :
            a = m+1
        m = (a+b)//2
    return l[a]

def recherche_dichotomique_recursive(id, liste_triee, a = 0, b = -1):
    if a == b :
        return a
    if b == -1 :
        b = len(liste_triee)-1
    m = (a+b)//2
    if liste_triee[m][0]== id:
        return liste_triee[m]
    elif liste_triee[m][0] > id :
        return recherche_dichotomique_recursive(id, liste_triee, a, m-1)
    else :
        return recherche_dichotomique_recursive(id, liste_triee, m+1, b)

def tri_insertion(l):
    L = list(l)
    n = len(L)
    for k in range(1,n):
        cle = L[k]
        j = k-1
        while j>=0 and L[j] > cle:
            L[j+1] = L[j]
            j = j-1
        L[j+1] = cle
    return L


if __name__=='__main__':
    print('--------------------PROJET ADSA: LE JOKER--------------------\n')
    print('PART 1 : CONNECTING THE PEOPLE')
    print('---------------------------------')
    print('1)To display the Gotham City’s railways.')
    print('2)To show a connected graph while minimizing the total amount of distance.')
    print('---------------------------------')
    print('Part 2: SPREAD THE REVOLUTION')
    print('---------------------------------')
    print('3)To show the shortest path from to Gotham City (first line/column) to the others.')
    print('---------------------------------')
    print('Part 3:ORGANIZE THE JOKERS')
    print('---------------------------------')
    print('4)To find a member of Joker team in database with his ID.(linear algorithm)')
    print('5)To find a member of Joker team in database with his ID.(Divide&Conquer algorithm)')
    print('6)To sort database and find a member of Joker team with his ID.(Divide&Conquer algorithm)')
    print('---------------------------------')
    print('Part 4:THE JOKERFATHER')
    print('---------------------------------')
    print('7)To find a member of Joker team in database using BINARY TREE.')
    print('8)To find a member of Joker team in database using AVL TREE.')
    print('---------------------------------')


    choix = int(input("Please choose an option between 1 and 8: "))
    while choix not in (1,2,3,4,5,6,7,8):
        print('Error, this option is nor available.')
        choix = int(input("Please choose an option between 1 and 3: "))
    if choix==1:
        print('GOTHAM CITY RAIL !')
        graph = Graphe()
        with open("GothamCityRail.txt") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data = line.split()
                if len(data) == 3:
                    graph.ajouteSommet(data[0])
                    graph.ajouteSommet(data[1])
                    graph.ajouteArrete(data[0], data[1], float(data[2]))
                line = fp.readline()
                cnt += 1
        print(graph)
        graph.__plotnetwork__()

    if choix==2:
        print('à faire')

    if choix==3:
        graphematrice = [[0, 8.1, 9.2, 7.7, 9.3, 2.3, 5.1, 10.2, 6.1, 7.0],
                         [8.1, 0, 12, 0.9, 12, 9.5, 10.1, 12.8, 2.0, 1.0],
                         [9.2, 12, 0, 11.2, 0.7, 11.1, 8.1, 1.1, 10.5, 11.5],
                         [7.7, 0.9, 11.2, 0, 11.2, 9.2, 9.5, 12, 1.6, 1.1],
                         [9.3, 12, 0.7, 11.2, 0, 11.2, 8.5, 1.0, 10.6, 11.6],
                         [2.3, 9.5, 11.1, 9.2, 11.2, 0, 5.6, 12.1, 7.7, 8.5],
                         [5.1, 10.1, 8.1, 9.5, 8.5, 5.6, 0, 9.1, 8.3, 9.3],
                         [10.2, 12.8, 1.1, 12.0, 1.0, 12.1, 9.1, 0, 11.4, 12.4],
                         [6.1, 2.0, 10.5, 1.6, 10.6, 7.7, 8.3, 11.4, 0, 1.1],
                         [7.0, 1.0, 11.5, 1.1, 11.6, 8.5, 9.3, 12.4, 1.1, 0.0]]

        dijkstra(graphematrice, 0)

        print ("\n We can conclude that it will be better to send only 7 peoples!\n")

    if choix == 4:
        equipejoker = []
        with open("acteur.txt") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data = line.split()
                membre = [int(data[0]), data[1]]
                equipejoker.append(membre)
                line = fp.readline()
                cnt += 1
        print(equipejoker)
        idmember=int(input("Please choose an ID between 1 and 129 of the joker team:(Linear search) "))
        print(recherche(equipejoker, idmember))

    if choix == 5:
        equipejoker = []
        with open("acteur.txt") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data = line.split()
                membre = [int(data[0]), data[1]]
                equipejoker.append(membre)
                line = fp.readline()
                cnt += 1
        print(equipejoker)
        idmember = int(input("Please choose an ID between 1 and 129 of the joker team:(Divide&Conquer search dicho) "))
        print(recherche_dicho(equipejoker,idmember))
    if choix == 6:
        equipejoker = []
        with open("acteur.txt") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data = line.split()
                membre = [int(data[0]), data[1]]
                equipejoker.append(membre)
                line = fp.readline()
                cnt += 1
        print(equipejoker)
        random.shuffle(equipejoker)
        print(equipejoker)
        print("TRI INSERTION:")
        print(tri_insertion(equipejoker))
        idmember = int(input("Please choose an ID between 1 and 129 of the joker team:(sort and Divide&Conquer algorithm) "))
        print(recherche_dicho(tri_insertion(equipejoker), idmember))
    if choix == 7:
        arbre = Node(0, 'Depart')
        equipejoker = []
        with open("acteur.txt") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data = line.split()
                membre = [int(data[0]), data[1]]
                equipejoker.append(membre)
                line = fp.readline()
                cnt += 1
        for personne in equipejoker:
            insert(arbre, Node(personne[0], personne[1]))
        print("Inorder traversal of the constructed AVL tree is\n")
        inorder(arbre)
        print("\n")
        idmember = int(input("Please choose an ID between 1 and 129 of the joker team: (Binary Search Tree)"))
        print(search(arbre, idmember))
    if choix == 8:
        myTree = AVL_Tree()
        AVL = None
        equipejoker = []
        with open("acteur.txt") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                data = line.split()
                membre = [int(data[0]), data[1]]
                equipejoker.append(membre)
                line = fp.readline()
                cnt += 1
        for personne in equipejoker:
            AVL = myTree.insert(AVL, personne[0], personne[1])

        print("Preorder traversal of the constructed AVL tree is\n")
        myTree.preOrder(AVL)
        print("\n")
        print("Inorder traversal of the constructed AVL tree is\n")
        myTree.inorderAVL(AVL)
        idmember = int(input("Please choose an ID between 1 and 129 of the joker team:(AVL Search Tree) "))
        print(search(AVL, idmember))
        print()




