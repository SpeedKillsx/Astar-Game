"""
    TP2 RP (Qst 1 ,2 et 3 en utilisant pygame)
    - LABCHRI Amayas
    - KOULAL Yidhir Aghiles
"""
import time
from tkinter import *
from tkinter import messagebox
import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size
import pygame
from pygame.locals import *
import numpy as np
from collections import deque
from time import sleep
pygame.init()
#c = True
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300
# Matrice du taquin
matrice = np.array([
     [1,2,3],
     [8,0,4],
     [7,6,5]
    ])
mat = np.array([
     [2,8,3],
     [1,6,4],
     [7,0,5],
    ])
tab=[
     [0,1,2],
     [3,5,6],
     [7,8,9]
     ]
# Listes des deplacement possible pour chaque case de la matrice
dep00=[(0,1),(1,0)]
dep01=[(0,0),(0,2),(1,1)]
dep02=[(0,1),(1,2)]
dep10=[(0,0),(1,1),(2,0)]
dep11=[(1,0),(0,1),(1,2),(2,1)]
dep12=[(1,1),(0,2),(2,2)]
dep20=[(1,0),(2,1)]
dep21=[(2,0),(1,1),(2,2)]
dep22=[(2,1),(1,2)]
#Remplissage du tableau qui contiendra les listes de deplacement possible 
tab[0][0] = dep00
tab[0][1] = dep01
tab[0][2] = dep02
tab[1][0] = dep10
tab[1][1] = dep11
tab[1][2] = dep12
tab[2][0] = dep20
tab[2][1] = dep21
tab[2][2] = dep22

# la fonction pour le jeu
def main():
    # on declare deux variables globales pour facilites les modifications
    global SCREEN, CLOCK
    pygame.init() #on initilise une fenetre pygame
    pygame.display.list_modes() 
    

    SCREEN = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)#le background en blanc
    #drawGrid()# fonction pour dessiner la grille a partir de la matrice
    #Nombre(matrice)# fonction qui ecrit les chiffres dans la matrice
    # tant que le jeu est actif
    drawGrid()
    
    c = True
    while c:
        
        
        pygame.display.update()# mettre a jour le jeu 
        c = a_star(mat,0,False)
        
        pygame.display.update()# on effectue les modifications
        
    

#fonction qui dessine la grille
def drawGrid():
    blockSize = 100 #distance entre chaque case de la grille
    
    for x in range(0, WINDOW_WIDTH, blockSize):
        
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)# creer un rectangle
            pygame.draw.rect(SCREEN, BLACK, rect, 1)#dessiner un rectangle dans la matrice (grille)

# fonction qui remplit la grille avec des nombres
def Nombre(matrice):
    #sleep(2)
    
    i = 0
    j = 0
    # font est arial avec une taille de 30
    font = pygame.font.SysFont("arial", 30)
    for x in range(0, WINDOW_HEIGHT, 100):
        for y in range(0, WINDOW_WIDTH, 100):
           
               
               #si la valeur de la case est differente de 0 on ne dessine rien dans la case
               if matrice[j,i]!=0:
                   text = font.render(str(matrice[j,i]), False, BLACK)# le text est la valeur de la matrice
                   SCREEN.blit(text,(x+ 50, y+50))#on met le text dans la position (x+50, y+50)
                   
               
               j=j+1   
        i=i+1 
        j=0# des avoir fini une ligne de la matrice on remet l indice des colonnes a 0

# fonction qui retourne la postion (x,y) du vide dans la matrice
def rechercher_vide(matrice_img):
  librei=0
  librej=0
  for i in range(3):
    for j in range(3):
      if(matrice_img[i][j]==0):
        librei=i
        librej=j
        break
    
  return(librei,librej)
#Foction pour trouver la position (x,y) du chiffre dans la matrice
def rechercher_chiffre(chiffre,matrice_img):
  for i in range(3):
    for j in range(3):
      if(matrice_img[i][j]==chiffre):
        posi=i
        posj=j
        break
    
  return(posi,posj)
# retourner le nombre dans la matrice selon sa position (x,y)
def retournerNobre(chi, chj):
    return matrice[chi, chj]
#fonction qui va verifier si le deplacement est possible
def jouer(chiffre,matrice_img,tab):
    #on cherche la position du vide
    librei,librej=rechercher_vide(matrice_img)
    #la position du chiffre a permuter avec le vide
    poschi,poschj=rechercher_chiffre(chiffre,matrice_img)  
    q = deque(tab[librei][librej])#file pour les deplacements possible de la case vide
    
    possible=False#un booleen pour sortir de la boucle
    while(possible==False):
        while len(tab[librei][librej]) !=0:
            try:
                posi,posj=q.popleft()
                if(posi == poschi and posj == poschj):#si la position du chiffre a permuter est dans les deplacements possible de la case vide
                    print("se deplace vers ",poschi, poschj)
                    matrice_img[poschi][poschj]=0
                    matrice_img[librei][librej]=chiffre
                    possible=True
                    #q.clear()
                    return poschi,poschj 
            except IndexError:
                break
    if(possible==False):
        print("deplacement impossible")
    return None, None
  
def MoveNumber(nb):
    # on mettra les directions comme qui suit
    """
    * gauche = -1
    * droite = 1
    * haut = 2 
    * bas = -2
    """
    xch, ych = jouer(nb,matrice,tab)
               
    if xch==None and ych==None:
        print("Impossible")
    
    #afficher la grille en noir (cela ne se verra pas) pour la reinitialiser
    SCREEN.fill(pygame.Color("black"))
def comparerMat(mat1,mat2):
  eg=True
  for i in range(mat1.shape[0]):
    for j in range(mat1.shape[1]):
      if(mat1[i][j] != mat2[i][j]):
        eg=False
  return eg      

def h(mat,matrice_img):
  x=0
  for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
      if(mat[i][j] != matrice_img[i][j] and mat[i][j] !=0):
        x=x+1
  return x


    
def a_star(mat,g,term):
  nbrcoups=""
  SCREEN.fill(WHITE)
  drawGrid()
  Nombre(mat)
  pygame.display.update()
  pygame.time.delay(1000)
  if(term == True):
    print("\n\n\nL'algorithme est fini , vous avez gagné dans le jeu de TAQUIN")
    #afficher(mat)
    #plt.show()
    #sleep(2)
    #exit(1)
    #os._exit(1)
    SCREEN.fill(WHITE)
    drawGrid()
    Nombre(mat)
    pygame.display.update()
    nbrcoups = "Vous avez ganger avec un nombre de coups = "+str(g)
    Tk().wm_withdraw() #to hide the main window
    messagebox.showinfo('Felicitation',nbrcoups)
    c= False
    
    return c 
  else:  
    reussir = comparerMat(mat,matrice)
    print("reussir = ",reussir)
    if(reussir == True):
     
      a_star(mat,g,True)
      
      #os._exit(1)
    
    else:

      mat1=np.copy(mat)
      mat2=np.copy(mat)
      mat3=np.copy(mat)
      mat4=np.copy(mat)
      g=g+1
      f1=f2=f3=f4=1000
      print("\n\n \nmatrice initiale\n")
      #afficher(mat)
      #plt.show()
      #sleep(2)
      ilibre,jlibre=rechercher_vide(mat)
      n=mat.shape[0]
      #plt.figure()
      
      if(ilibre != n-1):
        z=mat1[ilibre+1][jlibre]
        mat1[ilibre+1][jlibre]=0
        mat1[ilibre][jlibre]=z
        #afficher(mat1)
        SCREEN.fill(WHITE)
        drawGrid()
        Nombre(mat1)
        pygame.display.update()
        h1=h(mat1,matrice)
        f1=g+h1
        print("h1 = ",h1)
        print("g = ",g)
        print("f1 = ",f1)
        #plt.show()
      
        #sleep(2)
      SCREEN.fill(WHITE)  
      drawGrid()  
      Nombre(mat)
      pygame.display.update()     
      if(jlibre != n-1):
        z=mat1[ilibre][jlibre+1]
        mat2[ilibre][jlibre+1]=0
        mat2[ilibre][jlibre]=z
        print("mat2")
        #afficher(mat2)
        SCREEN.fill(WHITE)
        drawGrid()
        Nombre(mat2)
        pygame.display.update()
        h2=h(mat2,matrice)
        f2=g+h2
        print("h2 = ",h2)
        print("g = ",g)
        print("f2 = ",g+h2)
        #plt.show()
      
        #sleep(2)
      SCREEN.fill(WHITE) 
      drawGrid()  
      Nombre(mat)
      pygame.display.update()
      if(ilibre != 0):
        z=mat1[ilibre-1][jlibre]
        mat3[ilibre-1][jlibre]=0
        mat3[ilibre][jlibre]=z
        print("mat3")
        #afficher(mat3)
        SCREEN.fill(WHITE)
        drawGrid()
        Nombre(mat3)
        pygame.display.update()
        h3=h(mat3,matrice)
        f3=g+h3
        print("h3 = ",h3)
        print("g = ",g)
        print("f3 = ",g+h3)
        #plt.show()
      
        #sleep(2)
      SCREEN.fill(WHITE) 
      drawGrid()  
      Nombre(mat)
      pygame.display.update()
      if(jlibre != 0):
        z=mat1[ilibre][jlibre-1]
        mat4[ilibre][jlibre-1]=0
        mat4[ilibre][jlibre]=z
        print("mat4")
        #afficher(mat4)
        SCREEN.fill(WHITE)
        drawGrid()
        Nombre(mat4)
        pygame.display.update()
        h4=h(mat4,matrice)
        f4=g+h4
        print("h4 = ",h4)
        print("g = ",g)
        print("f4 = ",g+h4)
        #plt.show()
      
        #sleep(2)
#Chercher la composition qui a comme nombres de cases invalides minimal
      SCREEN.fill(WHITE)
      drawGrid()
      Nombre(mat)
      pygame.display.update()
      min=f1
      if(f2<min):
        min=f2
      if(f3<min):
        min=f3
      if(f4<min):
        min=f4
      print("Min des f = ",min)      
      en=False
      if(f1 == min and reussir == False and en == False):
        en = True
        
        a_star(mat1,g,reussir)
      if(f2 == min and reussir == False and en == False):
        en = True
        a_star(mat2,g,reussir)
      if(f3 == min and reussir == False and en == False):
        en = True
        a_star(mat3,g,reussir)
      if(f4 == min and reussir == False and en == False):
        en = True
        a_star(mat4,g,reussir)      

        

main()
