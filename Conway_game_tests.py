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

def init_grid():
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append(False)
        new_grid.append(ligne)
    return new_grid

def affiche():
    fenetre.blit(fond, (0,0))
    for cell in alive:
        pixel_pos = (cell[1] * cases_pixels , cell[0] * cases_pixels)
        fenetre.blit(living_cell, pixel_pos)
    pygame.display.flip()

def valide(cell):
    return not (cell[0] < 0 or cell[0] >= cases_haut or cell[1] < 0 or cell[1] >= cases_large)

def voisins(cell):
    voisins = []
    l = cell[0]
    c = cell[1]
    for i in range(l - 1, l + 2):
        for j in range(c - 1, c + 2):
            voisin = (i,j)
            if valide(cell) and voisin != cell:
                voisins.append(voisin)
    return voisins

def interesting():
    interessant = []
    for cell in alive:
        if not cell in interessant :
            interessant.append(cell)
        for i in voisins(cell):
            if not i in interessant:
                interessant.append(i)
    return interessant

def etat(cell):
    if not valide(cell):
        return False
    return grid[ cell[0] ][ cell[1] ]

def voisins_alive(cell):
    nb = 0
    for v in voisins(cell):
        if etat(v):
            nb += 1
    return nb

def next_etat(cell):
    alive = etat(cell)
    nb_voisins = voisins_alive(cell)
    if alive and nb_voisins in [2,3]:
        next = True
    elif (not alive) and nb_voisins == 3:
        next = True
    else:
        next = False
    return next

def flip(cell):
    if etat(cell):
        del alive[ alive.index(cell) ]
    else:
        alive.append(cell)
    grid [cell[0]][cell[1]] = not etat(cell)

def refresh():
    need_to_change = []
    for cell in interesting():
        if  etat(cell) != next_etat(cell):
            need_to_change.append(cell)

    for cell in need_to_change:
        flip(cell)

def button_clik(pixel_pos):
    cell = (pixel_pos[1] //cases_pixels, pixel_pos[0] //cases_pixels)
    flip(cell)

def randomized():
    global grid
    global alive
    grid = []
    alive = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            if random.random() < probabilite_alive:
                value = True
                alive.append((i,j))
            else:
                value = False
            ligne.append(value)
        grid.append(ligne)

###############################################################################
###     Code executé :


pygame.init()

largeur_pixel = cases_large * cases_pixels
hauteur_pixel = cases_haut * cases_pixels

fenetre = pygame.display.set_mode((largeur_pixel, hauteur_pixel))

fond = pygame.Surface((largeur_pixel, hauteur_pixel))
fond.fill(dead_color)

living_cell = pygame.Surface((cases_pixels,cases_pixels))
living_cell.fill(living_color)

time_gap = default_time_gap

grid = init_grid()
alive = []

alive.append((10,10))
grid[10][10] = True
alive.append((10,11))
grid[10][11] = True
alive.append((10,9))
grid[10][9] = True

print(voisins_alive((10,12)))
print(next_etat((10,12)))


affiche()

pause = True
continuer = True
while continuer:
    if not pause:
        start_time = time.time()

        refresh()

        time_to_wait = positif(time_gap - (time.time() - start_time))
        time.sleep(time_to_wait)

        affiche()

    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                button_clik(event.pos)
                affiche()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
            if event.key == pause_key:
                pause = not pause
            if event.key == random_key:
                randomized()
                affiche()















###     Fin du fichier
################################################################################
