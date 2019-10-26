import time
import random

import pygame
from pygame.locals import *

largeur = 125
hauteur = 90
tailleCase = 10 #Largeur d'une case en pixel

fichierSource = 'canon.cgol'
#Le nom du fichier que l'on charge lorsque l'on appuie qur la touche adequate

#Temps minimal entre les générations :
timeGapDefaut = 0.0 #float en secondes
#Il s'agit d'un temps minimal, parceque si l'ordinateur met trop de temps à
#calculer, on ne pourra pas aller plus vite que lui

pasChangementtimeGap= 0.02 #en secondes
#Le pas de changement lorque l'on accelere ou ralenti le programme


#La couleur des cellules, vivantes ou mortes :
couleurMort = (0,0,0)
couleurVie = (255,255,255)

#La couleur du quadrillage :
couleurQuadrillage = (50,50,50)
#Faut il afficher le quadrillage :
afficheQuadrillage = False #Possibilité de changer pendant l'execution du programme

tailleMemoire = 1000
#Nombre maximal de positions à conserver

#Controls keys :

pauseKey = K_p
saveKey = K_s
loadKey = K_w
centerLoadKey = K_x
randomKey = K_r
eraseKey = K_v
timeGapDefautKey = K_c
fasterKey = K_f
slowerKey = K_d
miroirHorizontalKey = K_h
miroirVerticalKey = K_g
afficheQuadrillageKey = K_l
enterMemoryMode = K_m
backInPastKey = K_LEFT
backInFutureKey = K_RIGHT
loadMemoryPositionKey = K_w

# TODO: Essayer d'accélerer le calcul de la position suivante : pour le moment
#on calcule l'etat suivant pour chaque case, mais les seules cases à changer
#sont celles autours de cases vivantes ou les cases vivantes. Il faut cependant
#eviter de calculer deux fois la meme case et éviter d'utiliser la fonction in
#qui semble ralentir considérablement les calculs (ou alors je l'utilisait
#vraiment mal)

#TODO : ajouter un fichier de configuration pour les constantes et les touches

#---------------------------------------
#   Objets :
#---------------------------------------
class Case:
    def __init__(self,position):
        self.ligne = position[0] #int
        #Position de la case en hauteur
        self.colonne = position[1] #int
        #Position de la case en largeur
        self.vivant = False #Boolean
        #Etat actuel de la case
        self.suivant = False #Boolean
        #Etat suivant de la case
        self.voisins = [] #List of Case
        #Contient toutes les cases voisines
        #voisins prend sa bonne valeur plus tard, quand toutes les autres cases
        #sont crées

    def initVoisins(self,cases):
        #But de la procédure : récupérer les cases voisines dans l'attribut voisins
        #In : cases, list of Case, la liste des cases
        l = self.ligne
        c = self.colonne
        positionVoisines =  [(l-1 , c-1),
            (l   , c-1),
            (l+1 , c-1),
            (l-1 , c),
            (l+1 , c),
            (l-1 , c+1),
            (l   , c+1),
            (l+1 , c+1)]

        for pos in positionVoisines:
            l = pos[0]
            c = pos[1]
            if l >= 0 and l < hauteur and c >= 0 and c < largeur:
                self.voisins.append( cases[ l ][ c ] )

    def nextState(self):
        #But de la procédure : regarder l'etat suivant de la case selon les voisins

        nbVoisinsVivant = self.voisinsVivants()

        if self.vivant and (nbVoisinsVivant == 2 or nbVoisinsVivant == 3):
            self.suivant = True
        elif (not self.vivant) and nbVoisinsVivant == 3:
            self.suivant = True
        else:
            self.suivant = False

    def voisinsVivants(self):
        #But de la fonction : retourner le nombre de voisins vivants
        nbVoisinsVivant = 0
        for case in self.voisins:
            if case.vivant :
                nbVoisinsVivant += 1
        return nbVoisinsVivant

    def changeState(self):
        #But de la procédure : changer la valeur de self.vivant
        self.vivant = not self.vivant


    def newState(self):
        #But de la procédure : passer à l'etat suivant
        self.vivant = self.suivant


    def affiche(self):
        #But de la procédure : affiche la case au bon endroit
        if self.vivant:
            skin = skinAlive
        else:
            skin = skinDead
        positionPixel = posCoordToPixel(self.getPosition())
        fenetre.blit(skin , positionPixel)

    def getPosition(self):
        #But de la procédure : retourner un tupple contenant la position de la case
        return (self.ligne , self.colonne)

    def setState(self,vivant):
        #But de la procedure : forcer l'etat de la case à la valeur choisie
        #IN : vivant , boolean, l'etat que l'on impose à la case
        self.vivant = vivant

    def getState(self):
        #But de la fonction : retourner la valeur de self.vivant
        #RETURN : boolean, la valeur de self.vivant
        return self.vivant

#---------------------------------------
#   Fonctions secondaires :
#---------------------------------------

def supZero(x):
    #But de la fonction : si le nombre est négatif, on renvoie 0.0, sinon on
    #   renvoie le nombre tel quel
    #IN : x , float, le nombre que l'on veut traiter
    #RETURN : res , float, 0 si x est négatif, x sinon
    if x < 0:
        res = 0
    else:
        res = x
    return res


def str_nb(n,taille = 2):
    #But de la fonction : écrit les nombres à la bonne taille,
    #    avec des 0 devant si ils sont trops courts
    #IN : n , float or int, le nombre que l'on veut écrire
    #     taille , int , la taille du nombre écrit (2 par défaut)
    ch = str(n)
    while len(ch) < taille:
        ch = '0' + ch
    return ch


def posPixelToCoord(positionPixel):
    #But de la fonction : retourner la position de la case correspondant à la
    #   position en pixel donné
    #IN : position_pixel, tupple, la position en pixel
    #RETURN : position, tupple, la position de la case touchée
    return (positionPixel[1] //tailleCase, positionPixel[0] //tailleCase)


def posCoordToPixel(position):
    #But de la fonction : retourner la position du pixel haut-gauche
    #   correspondant à la position de la case touchée
    #IN : position, tupple, la position de la case touchée
    #RETURN : position_pixel, tupple, la position en pixel
    return (position[1]* tailleCase, position[0]*tailleCase)

def gridFromFile(name,grille):
    #But de la procédure : construire une grille en rapport avec le fichier
    #IN : name, string, le nom du fichier
    #OUT : grille, list of boolean, la grille correspondante
    f = open(name, 'r')
    lignes = f.readlines()
    f.close()
    #On enleve le retour à la ligne :
    lignes = [x[:-1] for x in lignes]
    for i in range(len(lignes)):
        newLigne = []
        for j in range(len(lignes[i])):
            if lignes[i][j] == '0' or lignes[i][j] == 'O':
                newLigne.append(True)
            else:
                newLigne.append(False)
        grille.append(newLigne[:])

def toBoolean(cases):
    #But de la fonction : renvoyer une liste de booleens correspondant à l'etat
    #   cases
    #IN : cases, List of Case , la liste de toutes les cases
    #Return : Une grille de l'état en utilisant des booleens
    grille = []
    for ligne in cases:
        line = []
        for case in ligne:
            line.append(case.getState())
        grille.append(line[:])
    return grille

def afficheEtatBool(etat , afficheGrille):
    #But de la procedure : afficher un état à partir d'une grille de booleens
    #IN : memoire
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if etat[ligne][colonne]:
                skin = skinAlive
            else:
                skin = skinDead
            positionPixel = posCoordToPixel( (ligne,colonne) )
            fenetre.blit(skin , positionPixel)
    if afficheGrille:
        afficherQuadrillage()
    pygame.display.flip()

def setGridOn(cases, grille):
    #But de la procedure : Mettre cases à jours à partir de la grille de booleen
    #   donnée
    #IN : grille
    #IN-OUT : cases
    for i in range(hauteur):
        for j in range(largeur):
            cases[i][j].setState(grille[i][j])

#Fonctions Principales :

def affiche(cases,afficheGrille):
    #But de la procedure : afficher l'etat actuel du jeu
    #IN : cases , list of Case, la liste contenant toutes les cases du jeu
    for ligne in cases:
        for case in ligne:
            case.affiche()
    if afficheGrille:
        afficherQuadrillage()
    pygame.display.flip()

def afficherQuadrillage():
    #But de la procédure : afficher une grille sur le plateau de jeu
    for i in range(largeur):
        fenetre.blit(ligneVerticale, (i * tailleCase,0))

    for i in range(hauteur):
        fenetre.blit(ligneHorizontale, (0,i * tailleCase))


def initCases(cases):
    #But de la procédure : initialiser toutes les cases en fonction de la taille
    #   voulue. On les stocke dans la liste de Case cases
    #IN : None (largeur et hauteur sont des constantes)
    #OUT : cases
    for h in range(hauteur):
        ligne = []
        for l in range(largeur):
            case = Case( (h,l) )
            ligne.append(case)
        cases.append(ligne[:])
    i = 0
    for ligne in cases:
        for case in ligne:
            case.initVoisins(cases)
            i += 1

def etatSuivant(cases):
    #But de la procedure : modifier chaque case du plateau
    #IN : cases , list of Case, contenant les cases du plateau

    #Calcul de l'etat suivant :
    for ligne in cases:
        for case in ligne:
            case.nextState()

    #Passage à l'état suivant :
    for ligne in cases:
        for case in ligne:
            case.newState()

def changeCase(positionPixel , cases):
    #But de la procédure : changer l'etat de la case sur laquelle on a touché
    #IN : positionPixel , tupple, la position du click de la souris
    pos = posPixelToCoord(positionPixel)

    cases[ pos[0] ][ pos[1] ].changeState()

def randomized(proba,cases):
    #But de la procédure : Choisir aleatoirement l'etat de chaque case de la grille
    #IN : proba, float, proba entre 0 et 1 que la case soit en vie
    #     cases, list of Case, la liste des cases du jeu
    for ligne in cases:
        for case in ligne:
            case.setState(random.random() < proba)

def erase(cases):
    #But de la procédure : mettre toutes les cases mortes
    #IN : cases, list of Case, la liste de toutes les cases
    for ligne in cases:
        for case in ligne:
            case.setState(False)

def chargeFile(name,cases):
    #But de la procédure : changer l'etat des cases en haut a gauche pour coller
    #   au fichier donné
    #IN: name, string, le nom du fichier
    #OUT : cases, list of Case, la liste des cases
    grille = []
    gridFromFile(name,grille)
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if i < hauteur and j < largeur:
                cases[i][j].setState(grille[i][j])

def miroirVertical(cases):
    #But de la procédure : réaaliser une symetrie axiale verticalement
    for i in range(hauteur):
        for j in range(largeur//2):
            cases[i][-(j+1)].setState(cases[i][j].getState())

def miroirHorizontal(cases):
    #But de la procédure : réaaliser une symetrie axiale horizontalement
    for i in range(hauteur//2):
        for j in range(largeur):
            cases[-(i+1)][j].setState(cases[i][j].getState())

def saveState(cases):
    #But procedure : sauvegarder dans un fichier l'etat actuel du jeu
    #IN : cases, list of Case, la liste de toutes les cases

    #on sauvegarde la position dans un fichier, dont le nom est la date
    #actuelle (année mois jour heure seconde)
    #On récupère la date :
    D = time.localtime()

    name = str(D[0]) + str_nb(D[1]) + str_nb(D[2]) + str_nb(D[3])+ str_nb(D[4]) + ".cgol"
    print(name)
    f = open(name, "w")
    #'-' pour les cellules mortes, O pour les vivantes
    for ligne in cases:
        for case in ligne:
            if case.getState():
                f.write("O")
            else:
                f.write("-")
        f.write("\n")
    f.close()
    print("Position sauvegardée")

def chargeFileCenter(name, cases):
    #But de la procédure : changer l'etat des cases au centre pour coller
    #   au fichier donné
    #IN: name, string, le nom du fichier
    #OUT : cases, list of Case, la liste des cases
    grille = []
    gridFromFile(name,grille)
    iStart = ( hauteur - len(grille) ) // 2
    jStart = ( largeur - len(grille[0]) ) // 2

    for i in range(len(grille)):
        l = i + iStart
        for j in range(len(grille[i])):
            c = j + jStart
            if l >= 0 and l < hauteur and c >= 0 and c < largeur:
                cases[l][c].setState(grille[i][j])

def ajoutEtatMemoire(cases,memoire):
    #But de la procédure : enregistrer l'état case dans la mémoire
    #IN : case, list of Case, la liste des cases de l'état actuel
    #IN-OUT : memoire, List of List of boolean
    if len(memoire) >= tailleMemoire:
        del memoire[0]
    memoire.append(toBoolean(cases))

def memoryMode(cases, memoire,afficheGrille):
    #But de la procedure : On rentre en mode memoire, dans ce mode on peut
    #   visionner les états précedents du jeu, puis si on le souhaite recharger
    #   un etat précedent
    #IN : memoire, la liste des états précédents
    #   afficheGrille : Boolean, si il faut afficher la grille ou pas
    #IN-OUT : cases, le nouvel état, si l'on souhaite charger un état précédent
    #   L'état actuel sinon
    #Return : continuer, boolean, si il faut continuer le programme

    continuer = True

    positionMemoire = len(memoire) - 1
    #La position dans memoire où l'on est actuellement
    finBoucle = False
    while not finBoucle:
        for event in pygame.event.get():
            if event.type == QUIT:
                finboucle = True
                continuer = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    finBoucle = True
                    continuer = False
                if event.key == pauseKey:
                    finBoucle = True
                if event.key == afficheQuadrillageKey:
                    afficheGrille = not afficheGrille
                    afficheEtatBool(memoire[ positionMemoire ] ,afficheGrille)
                    #On ne raffraichi l'affichage que quand ça change
                if event.key == backInFutureKey:
                    if positionMemoire < len(memoire) - 1:
                        positionMemoire += 1
                        afficheEtatBool(memoire[ positionMemoire ] ,afficheGrille)
                        #On ne raffraichi l'affichage que quand ça change
                if event.key == backInPastKey:
                    if positionMemoire > 0:
                        positionMemoire -= 1
                        afficheEtatBool(memoire[ positionMemoire ] ,afficheGrille)
                        #On ne raffraichi l'affichage que quand ça change

                if event.key == loadMemoryPositionKey:
                    setGridOn(cases,memoire[positionMemoire])
                    finBoucle = True
    return continuer


def changeSpeed(sens,gap):
    #But de la fonction : augmenter ou diminuer le temps entre deux états
    #IN : sens : "faster" or "slower", sens de variation du temps
    #     gap : float, le temps précedent
    #RETURN : timeGap : le nouveaux temps entre les états
    timeGap = gap
    if sens == 'faster':
        timeGap = supZero(timeGap - pasChangementtimeGap)
    if sens == 'slower':
        timeGap += pasChangementtimeGap

    #Le quatre sert à ne pas trainer des nombres avec 45 chiffres
    #après la virgule, il permet cependant d'avoir une assez bonne
    #précision
    return round( timeGap,4 )



#---------------------------------------
#   Initialisation :
#---------------------------------------
largeurPixel = tailleCase * largeur
hauteurPixel = tailleCase * hauteur

pygame.init()
#permet de laisser une touhe enfoncée
pygame.key.set_repeat(1000,100)

fenetre = pygame.display.set_mode( (largeurPixel, hauteurPixel) )

skinAlive = pygame.Surface((tailleCase,tailleCase))
skinAlive.fill(couleurVie)

skinDead = pygame.Surface((tailleCase,tailleCase))
skinDead.fill(couleurMort)

ligneVerticale = pygame.Surface((1,hauteurPixel))
ligneVerticale.fill(couleurQuadrillage)
ligneHorizontale = pygame.Surface((largeurPixel,1))
ligneHorizontale.fill(couleurQuadrillage)

cases = []
initCases(cases)
memoire = []

timeGap = timeGapDefaut

pause = True
#---------------------------------------
#   Corps du Programme :
#---------------------------------------

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                changeCase(event.pos, cases)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
            if event.key == pauseKey:
                pause = not pause
            if event.key == randomKey:
                randomized(0.25, cases)
            if event.key == eraseKey:
                erase(cases)
            if event.key == loadKey:
                chargeFile(fichierSource, cases)
            if event.key == miroirVerticalKey:
                miroirVertical(cases)
            if event.key == miroirHorizontalKey:
                miroirHorizontal(cases)
            if event.key == saveKey:
                saveState(cases)
            if event.key == fasterKey:
                timeGap = changeSpeed('faster',timeGap)
            if event.key == slowerKey:
                timeGap = changeSpeed('slower',timeGap)
            if event.key == timeGapDefautKey:
                timeGap = timeGapDefaut
            if event.key == afficheQuadrillageKey:
                afficheQuadrillage = not afficheQuadrillage
            if event.key == centerLoadKey:
                chargeFileCenter(fichierSource, cases)
            if event.key == enterMemoryMode:
                pause = True
                continuer = memoryMode(cases,memoire,afficheQuadrillage)

    startTime = time.time()
    if not pause:
        ajoutEtatMemoire(cases,memoire)
        etatSuivant(cases)
    affiche(cases, afficheQuadrillage)
    finalTime = (time.time() - startTime)
    time.sleep(supZero(timeGap - finalTime))
