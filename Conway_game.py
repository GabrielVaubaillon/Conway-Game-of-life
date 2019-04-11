###############################################################################
###     Gabriel Vaubaillon
###
###             Conway Game of Life
###

###############################################################################
###     Settings :

#On choisit la taille de la grille de jeu :
cases_large = 125
cases_haut = 90

#La taille en pixel des cases
cases_pixels = 10

#Le nom du fichier chargé lorsque l'on appuiera sur la touche adéquate
fichier_source = 'canon.cgol'

#L'intervalle minimum entre deux générations, en secondes :
default_time_gap = 0.0

#le nombre de grilles maximum retenues en mémoire :
taille_memoire = 1000

#Lorsque l'on génère une grille aléatoire, la proba qu'une cellule soit en vie :
probabilite_alive = 0.25

#Apparence
#La couleur des cellules, vivantes ou mortes :
dead_color = (0,0,0)
living_color = (255,255,255)

###############################################################################
###     imports :

import time
import random

import pygame
from pygame.locals import *

#Controls keys :

pause_key = K_p
save_key = K_s
load_key = K_w
random_key = K_r
erase_key = K_v
restart_key = K_z
fast_key = K_f
slow_key = K_d
symmetry_horizontal_key = K_h
symmetry_vertical_key = K_g




###############################################################################
###     Functions :


def positif(n):
    if n < 0:
        #On retourne un nombre du même type que celui passé en entrée
        if type(n) == int :
            return 0
        else:
            return 0.00
    return n


def case(pos):
    """renvoie l'état de la case, si elle existe"""
    #On teste si la cellule demandée existe :
    if pos[0] < 0 or pos[0] >= cases_haut or pos[1] < 0 or pos[1] >= cases_large:
        return False
    #On retourne la valeur de la cellule
    return grid[ pos[0] ][ pos[1] ]


def voisins_alive(pos):
    """"retourne le nombre de voisins en vie"""
    nb_voisins_alive = 0
    l = pos[0]
    c = pos[1]
    #On regarde le carré des cellules autours de la position donnée
    for i in range(l - 1, l + 2):
        for j in range(c - 1, c + 2):
            position = (i,j)
            if case(position) and position != pos :
                nb_voisins_alive += 1
    return nb_voisins_alive


def next_step(pos):
    """détermine l'état d'une cellule pour la prochaine génération"""
    #Il s'agit ici des regles de base du jeu de la vie
    alive = case(pos)
    #La cellule vie ou meurt en fonction de son nombre de voisins vivants
    if (not alive) and voisins_alive(pos) == 3:
        next = True
    elif alive and voisins_alive(pos) in [2,3]:
        next = True
    else:
        next = False
    return next


def refresh():
    """crée la grille de la génération suivante"""
    #On calcule la nouvelle grille à partir du nombre de voisins des cellules
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append( next_step((i,j)) )
        new_grid.append(ligne)
    return new_grid[:]


def init_grid():
    """initialise une grille de la bonne taille"""
    #La grille initialisée est vide
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append(False)
        new_grid.append(ligne)
    return new_grid


def affiche():
    """affiche correctement l'état actuel de la grille
    dans la fenetre, avec les bonnes couleurs"""
    #On passe dans chaque ligne et chaque colonne de la grille, on affiche
    #la bonne couleur à la position correspondante
    for i in range(cases_haut):
        for j in range(cases_large):
            pos = (i,j)
            if case(pos):
                image = living_cell
            else:
                image = dead_cell
            pixel_position = (j* cases_pixels, i*cases_pixels)
            fenetre.blit(image, pixel_position)
    #On actualise la fenetre
    pygame.display.flip()


def whereiam(pixel_position):
    """retourne la position dans la grille à partir de la position en pixel"""
    return (pixel_position[1] //cases_pixels, pixel_position[0] //cases_pixels)


def flipItPlease(pos):
    """change l'état d'une cellule"""
    #La cellule passée en parametre changera d'état
    grid[ pos[0] ][ pos[1] ] = not case(pos)


def randomized():
    """"génère une grille aléatoire"""
    #On génere une nouvelle grille en mettant aléatoirement des cellules
    #vivantes ou mortes. La probabilité pour chaque cellule d'être vivante est
    #définie au début du programme
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            if random.random() < probabilite_alive:
                value = True
            else:
                value = False
            ligne.append(value)
        new_grid.append(ligne)
    return new_grid


def symetric_horizontal():
    """réalise une symétrie de la partie gauche de la grille"""
    #Pour réaliser la symétrie on remplie deux grilles, une dans le bon
    #sens et l'autre dans le sens inverse, puis on les concatene
    new_grid1 = []
    new_grid2 = []
    for i in range(cases_haut // 2):
        #on ne parcour que la moitié haute de la grille
        ligne = []
        for j in range(cases_large):
            ligne.append(case((i,j)))
        new_grid1.append(ligne[:])
        new_grid2 = [ligne[:]] + new_grid2[:]

    #Si la grille n'a pas une hauteur paire, il faut rajouter la ligne du milieu
    #qui ne change pas par rapport à la grille initiale
    if cases_haut % 2 != 0:
        i = cases_haut // 2
        ligne = []
        for j in range(cases_large):
            ligne.append(case((i,j)))
        new_grid1.append(ligne[:])

    #On concatene les deux grilles pour obtenir la nouvelle grille
    new_grid = new_grid1[:] + new_grid2[:]
    return new_grid


def symetric_vertical():
    """réalise une symétrie de la partie haute de la grille"""
    new_grid = []
    for i in range(cases_haut):
        #Pour réaliser la symétrie on remplie deux listes, une dans le bon
        #sens et l'autre dans le sens inverse, puis on les concatene
        ligne1 = []
        ligne2 = []
        for j in range(cases_large //2):
            ligne1.append(case((i,j)))
            ligne2 = [case((i,j))] + ligne2

        #si la grille a une largeur impaire, il faut rajouter la derniere
        #cellule, qui conserve son état :
        if cases_large % 2 != 0:
            j = cases_large // 2
            ligne1.append(case((i,j)))

        #On concatene les deux listes symétriques pour former la nouvelle ligne
        ligne = ligne1[:] + ligne2[:]
        #on ajoute la nouvelle ligne à la nouvelle grille
        new_grid.append(ligne)
    return new_grid


def init_memoire():
    """crée la liste pour stocker les grilles succésives, la mémoire"""
    #on initialise la mémoire de la bonne taille :
    memory = []
    for i in range(taille_memoire):
        memory.append(grid[:])
    return memory


def memory():
    """ajoute la grille actuelle dans la mémoire """
    global past
    #On enlève la derniere position de la mémire
    past = past[1:]
    #On ajoute la nouvelle position :
    past.append(grid[:])


def save_grid(grid):
    """permet de sauvegarder une grille dans un fichier"""
    #on sauvegarde la position dans un fichier, dont le nom est la date
    #actuelle (année mois jour heure seconde)
    #On récupère la date :
    D = time.localtime()
    name = str(D[1]) + str(D[2]) + str(D[3]) + str(D[4])+ str(D[5]) + ".cgol"
    f = open(name, "w")
    #On enregistre la grille dans une chaîne de caractere, '-' pour les cellules
    #mortes, O pour les vivantes
    ch = ''
    for i in range(cases_haut):
        for j in range(cases_large):
            pos = (i,j)
            if case(pos):
                ch += 'O'
            else:
                ch += '-'
        ch += '\n'
    #On enregistre le fichier, puis on quitte
    f.write(ch)
    f.close()
    print("Position sauvegardée")


def grid_from_file(fichier):
    """lit un fichier et crée la grille de jeu associée"""
    #On ouvre le fichier et on lit les lignes
    f= open(fichier, 'r')
    lignes = f.readlines()
    f.close()
    #Si la hauteur du fichier est trop grande pour la grille actuelle on ne peut
    #pas tout copier. Si la grille est plus grande que le fichier, on n'écrase
    #que les cellules dans la zone du fichier
    hauteur = min(len(lignes), cases_haut)
    for i in range(hauteur):
        #Comme au-dessus, mais pour la largeur
        largeur = min(len(lignes[i]), cases_large)
        for j in range(largeur):
            #On regarde si le fichier code une cellule vivant ou morte puis puis
            #on modifie directement la valeur dans la grille
            if lignes[i][j] in 'O0':
                grid[i][j] = True
            else:
                grid[i][j] = False



###############################################################################
###     Code executé :


#Initialisation de la fenetre :
largeur_pixel = cases_large * cases_pixels
hauteur_pixel = cases_haut * cases_pixels

#On initialise la fenetre d'interaction :
pygame.init()
fenetre = pygame.display.set_mode((largeur_pixel, hauteur_pixel))


#On initialise les images pour les cellules :
living_cell = pygame.Surface((cases_pixels,cases_pixels))
dead_cell = pygame.Surface((cases_pixels, cases_pixels))
#On leur donne la bonne couleur :
living_cell.fill(living_color)
dead_cell.fill(dead_color)

#permet de rester appuyé sur une touche
pygame.key.set_repeat(1000,100)

#Pour changer la vitesse sans perdre la valeur par défaut :
time_gap = default_time_gap

#On initialise une grille vide
grid = init_grid()

#Le jeu ne se lance pas tout de suite
pause = True
pos_temporelle = 0 #Notre position dans l'historique
past = init_memoire() #On initialise la mémoire

#La condition de boucle :
continuer = True
while continuer:

    if not pause:
        #On regarde le temps avant le calcul, pour attendre le bon temps après
        start_time = time.time()

        #On génere la nouvelle grille :
        grid = refresh()

        #On stocke la nouvelle grille dans la mémoire :
        memory()

        #On attend le temps qu'il faut avant la prochaine génération
        #en prenant en compte le temps de calcul
        time_to_wait = positif(time_gap - (time.time() - start_time))
        time.sleep(time_to_wait)

        #On affiche la grille :
        affiche()

    elif pos_temporelle == 0:
        #On ralentit la boucle quand on est en pause et que l'on ne navigue pas
        #dans l'historique, pour laisser l'ordinateur respirer
        time.sleep(0.5)

    #On interagit avec l'utilisateur :
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                """si l'utilisateur appuie sur une cellule elle change d'état"""
                #On récupère la position de la cellule que l'on veut changer
                position = whereiam(event.pos)
                #On change l'état de la cellule :
                flipItPlease(position)
                affiche()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                #On peut quitter le programme en appuyant sur échap
                continuer = False

            if event.key == pause_key:
                """permet de mettre ou d'enlever la pause"""
                pause = not pause
                #lorsque l'on redémarre on se se remet à la bonne position
                #de l'historique
                if not pause:
                    pos_temporelle = 0

            if event.key == random_key:
                """génere une grille aléatoire"""
                grid = randomized()#On génere la grille
                memory()#On ajoute la grille à la mémoire
                affiche()#On affiche la grille

            if event.key == symmetry_horizontal_key:
                """réalise une symétrie horizontale de la grille"""
                grid = symetric_horizontal()#On génere la grille
                memory()#On ajoute la grille à la mémoire
                affiche()#On affiche la grille

            if event.key == symmetry_vertical_key:
                """réalise une symétrie verticale de la grille"""
                grid = symetric_vertical()#On génere la grille
                memory()#On ajoute la grille à la mémoire
                affiche()#On affiche la grille

            if event.key == erase_key:
                """réinitialise la grille"""
                grid = init_grid()#On vide la grille
                memory()#On ajoute la grille à la mémoire
                affiche()#On affiche la grille

            if event.key == fast_key:
                """diminue le temps intergénération minimum"""
                #On arrondi pour éviter des flottants à rallonge
                #Et on ne prend pas de nombres négatifs
                time_gap = positif(round(time_gap - 0.02, 2))
                #Petit message pour afficher la vitesse :
                print(time_gap," secondes entre générétions")

            if event.key == slow_key:
                """augmente le temps intergénération minimum"""
                time_gap = positif(round(time_gap + 0.02, 2))
                #Petit message pour afficher la vitesse :
                print(time_gap," secondes entre générétions")

            if event.key == K_LEFT:
                """historique"""
                #On vérifie que l'on n'est pas au bout de l'historique
                if pos_temporelle > -taille_memoire + 1:
                    #On met pause lorsque l'on se déplace dans l'historique
                    pause = True
                    #stocke notre position actuelle dans la mémoire
                    pos_temporelle -= 1

                    #On change la grille, parceque l'on peut repartir de
                    #n'importe quelle position de l'historique :
                    grid = past[pos_temporelle -1]
                    affiche()

            if event.key == K_RIGHT:
                """historique"""
                #On vérifie que l'on n'essaie pas d'aller dans le futur
                #En effet, ces positions ne sont pas stockées
                if pos_temporelle < 0:
                    #on met pause lorsque l'on est dans l'historique
                    pause = True
                    #stocke notre position actuelle dans la mémoire
                    pos_temporelle += 1
                    grid = past[pos_temporelle -1]
                    affiche()

            if event.key == restart_key:
                """Réinitialisation de la grille et de la vitesse"""
                grid = init_grid() #On réinitialise la grille
                time_gap = default_time_gap #On réinitialise la vitesse
                pause = True #On met pause
                affiche() #On affiche le nouveau jeu :)
                memory()#Nota bene : On ne réinitialise pas la mémoire

            if event.key == save_key:
                """sauvegarde de la grille dans un fichier"""
                save_grid(grid)

            if event.key == load_key:
                """création de la grille à partir d'un fichier"""
                #La procédure modifie directement la grille
                grid_from_file(fichier_source)
                affiche()


###     Fin du fichier
################################################################################
