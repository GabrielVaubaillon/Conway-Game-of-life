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
intervalle_gen = 0.0

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


###############################################################################
###     Functions :


def positif(n):
    if n < 0:
        return 0
    return n


def case(pos):
    """renvoie l'état de la case, si elle existe"""
    #On teste si la cellule demandée existe :
    if pos[0] < 0 or pos[0] >= cases_haut or pos[1] < 0 or pos[1] >= cases_large:
        return False
    return grid[ pos[0] ][ pos[1] ]

def voisins_alive(pos):
    """"retourne le nombre de voisins en vie"""
    nb_voisins_alive = 0
    l = pos[0]
    c = pos[1]
    for i in range(l - 1, l + 2):
        for j in range(c - 1, c + 2):
            position = (i,j)
            if case(position) and position != pos:
                nb_voisins_alive += 1
    return nb_voisins_alive

def next_step(pos):
    """détermine l'état d'une cellule pour la prochaine génération"""
    #Il s'agit ici des regles de base du jeu de la vie
    alive = case(pos)
    if (not alive) and voisins_alive(pos) == 3:
        next = True
    elif alive and voisins_alive(pos) in [2,3]:
        next = True
    else:
        next = False
    return next

def refresh():
    """crée la grille de la génération suivante"""
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append( next_step((i,j)) )
        new_grid.append(ligne)
    return new_grid[:]

def init_grid():
    """initialise une grille de la bonne taille"""
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append(False)
        new_grid.append(ligne)
    return new_grid

def affiche_str():
    """affiche la grille sous forme de cractere, dans la console"""
    for i in range(cases_haut):
        for j in range(cases_large):
            pos = (i,j)
            if case(pos):
                print("O", end=' ')
            else:
                print("-", end=' ')
        print()
    print()

def affiche():
    """affiche correctement l'état actuel de la grille
    dans la fenetre, avec les bonnes couleurs"""
    #affiche_str()
    for i in range(cases_haut):
        for j in range(cases_large):
            pos = (i,j)
            if case(pos):
                image = living_cell
            else:
                image = dead_cell
            pixel_position = (j* cases_pixels, i*cases_pixels)
            fenetre.blit(image, pixel_position)
    pygame.display.flip()

def whereiam(pixel_position):
    """retourne la position dans la grille en fonction de la position en pixel"""
    return (pixel_position[1] // cases_pixels, pixel_position[0] // cases_pixels)

def flipItPlease(pos):
    """change l'état d'une cellule"""
    if case(pos):
        grid[ pos[0] ][ pos[1] ] = False
    else:
        grid[ pos[0] ][ pos[1] ] = True

def randomized():
    """"génère une grille aléatoire"""
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
    new_grid1 = []
    new_grid2 = []
    for i in range(cases_haut // 2):
        ligne = []
        for j in range(cases_large):
            ligne.append(case((i,j)))
        new_grid1.append(ligne[:])
        new_grid2 = [ligne[:]] + new_grid2[:]

    if cases_haut % 2 != 0:
        i = cases_haut // 2
        ligne = []
        for j in range(cases_large):
            ligne.append(case((i,j)))
        new_grid1.append(ligne[:])

    new_grid = new_grid1[:] + new_grid2[:]
    return new_grid


def symetric_vertical():
    """réalise une symétrie de la partie haute de la grille"""
    new_grid = []
    for i in range(cases_haut):
        ligne1 = []
        ligne2 = []
        for j in range(cases_large //2):
            ligne1.append(case((i,j)))
            ligne2 = [case((i,j))] + ligne2
        if cases_large % 2 != 0:
            j = cases_large // 2
            ligne1.append(case((i,j)))
        ligne = ligne1[:] + ligne2[:]
        new_grid.append(ligne)
    return new_grid

def init_memoire():
    """crée la liste pour stocker les grilles succésives, la mémoire"""
    memory = []
    for i in range(taille_memoire):
        memory.append(grid[:])
    return memory

def memory():
    """ajoute la grille actuelle dans la mémoire """
    global past
    past = past[1:]
    past.append(grid[:])

def save_grid(grid):
    """permet de sauvegarder une grille dans un fichier"""
    L = time.localtime()
    name = str(L[1]) + "_" + str(L[2]) + "_" + str(L[3]) + "_" + str(L[4]) + "_" + str(L[5]) + ".cgol"
    f = open(name, "w")
    ch = ''
    for i in range(cases_haut):
        for j in range(cases_large):
            pos = (i,j)
            if case(pos):
                ch += 'O'
            else:
                ch += '-'
        ch += '\n'
    f.write(ch)
    f.close()
    print("Position sauvegardée")

def grid_from_file(fichier):
    """lit un fichier et crée la grille de jeu associée"""
    f = open(fichier, 'r')
    lignes = f.readlines()
    f.close()
    new_grid = []
    for ligne in lignes:
        new_ligne = []
        for carac in ligne:
            if carac in 'O0':
                new_ligne.append(True)
            else:
                new_ligne.append(False)

        if len(new_ligne) > cases_large:
            new_ligne = new_ligne[:cases_large]

        elif len(new_ligne) < cases_large:
            for i in range(cases_large - len(ligne)):
                # TODO: il ne faut pas supprimer le reste de la grille :(
                new_ligne.append(False)

        new_grid.append(new_ligne[:])

    if len(new_grid) > cases_haut:
        new_grid = new_grid[:cases_haut]
    elif len(new_grid) < cases_haut:
        for i in range(cases_haut-len(new_grid)):
            new_ligne = []
            for j in range(cases_large):
                # TODO: il ne faut pas supprimer le reste de la grille :(
                new_ligne.append(False)
            new_grid.append(new_ligne)

    return new_grid


###############################################################################
###     Code executé :


#Initialisation de la fenetre :
largeur_pixel = cases_large * cases_pixels
hauteur_pixel = cases_haut * cases_pixels

pygame.init()
fenetre = pygame.display.set_mode((largeur_pixel, hauteur_pixel))


#On initialise les images pour les cellules :
living_cell = pygame.Surface((cases_pixels,cases_pixels))
living_cell.fill(living_color)

dead_cell = pygame.Surface((cases_pixels, cases_pixels))
dead_cell.fill(dead_color)

#permet de rester appuyé sur une touche
pygame.key.set_repeat(1000,100)

#Pour changer la vitesse sans perdre la valeur par défaut :
changed_intervalle_gen = intervalle_gen

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
        time_to_wait = positif(changed_intervalle_gen - (time.time() - start_time))
        time.sleep(time_to_wait)

        #On affiche la grille :
        affiche()

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
                continuer = False

            if event.key == K_p:
                """permet de mettre ou d'enlever la pause"""
                pause = not pause
                #lorsque l'on redémarre on se se remet à la bonne position
                #de l'historique
                if not pause:
                    pos_temporelle = 0

            if event.key == K_r:
                """génere une grille aléatoire"""
                grid = randomized()
                memory()
                affiche()

            if event.key == K_h:
                """réalise une symétrie horizontale de la grille"""
                grid = symetric_horizontal()
                memory()
                affiche()

            if event.key == K_g:
                """réalise une symétrie verticale de la grille"""
                grid = symetric_vertical()
                memory()
                affiche()

            if event.key == K_v:
                """réinitialise la grille"""
                grid = init_grid()
                memory()
                affiche()

            if event.key == K_f:
                """diminue le temps intergénération minimum"""
                changed_intervalle_gen = round(changed_intervalle_gen - 0.02, 2)
                if changed_intervalle_gen < 0:
                    changed_intervalle_gen = 0.00
                print(changed_intervalle_gen," secondes entre générétions")

            if event.key == K_d:
                """augmente le temps intergénération minimum"""
                changed_intervalle_gen = round(changed_intervalle_gen + 0.02, 2)
                if changed_intervalle_gen < 0:
                    changed_intervalle_gen = 0.00
                print(changed_intervalle_gen," secondes entre générétions")

            if event.key == K_LEFT:
                """historique"""
                #On vérifie que l'on n'est pas au bout de l'historique
                if pos_temporelle > -taille_memoire + 1:
                    pause = True
                    pos_temporelle -= 1

                    #On change la grille, parceque l'on peut repartir de
                    #n'importe quelle position de l'historique :
                    grid = past[pos_temporelle -1]
                    affiche()

            if event.key == K_RIGHT:
                """historique"""
                if pos_temporelle < 0:
                    pause = True
                    pos_temporelle += 1
                    grid = past[pos_temporelle -1]
                    affiche()

            if event.key == K_z:
                """Réinitialisation de la grille et de la vitesse"""
                grid = init_grid()
                changed_intervalle_gen = intervalle_gen
                pause = True
                affiche()

            if event.key == K_s:
                """sauvegarde de la grille dans un fichier"""
                save_grid(grid)

            if event.key == K_w:
                """création de la grille à partir d'un fichier"""
                grid = grid_from_file(fichier_source)
                affiche()


###     Fin du fichier
################################################################################
