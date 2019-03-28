###############################################################################
###     Gabriel Vaubaillon
###
###             Conway Game of Life
###

###############################################################################
###     Settings :

cases_large = 125
cases_haut = 90
cases_pixels = 10

fichier_source = '3_28_11_12_23.cgol'

intervalle_evo = 0.0 #en secondes

probabilite_alive = 0.25

taille_memoire = 1000

dead_color = (0,0,0)
living_color = (255,255,255)



###############################################################################
###     Imports des bibliotheques :

import time
import random

import pygame
from pygame.locals import *


###############################################################################
###     Fonctions :


def positif(n):
    if n < 0:
        return 0
    return n


def case(pos):
    if pos[0] < 0 or pos[0] >= cases_haut or pos[1] < 0 or pos[1] >= cases_large:
        return 0
    return grid[ pos[0] ][ pos[1] ]

def voisins_alive(pos):
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
    alive = case(pos) == 1
    if (not alive) and voisins_alive(pos) == 3:
        next = True
    elif alive and voisins_alive(pos) in [2,3]:
        next = True
    else:
        next = False
    return next

def refresh():
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append( next_step((i,j)) )
        new_grid.append(ligne)
    return new_grid[:]

def init_grid():
    new_grid = []
    for i in range(cases_haut):
        ligne = []
        for j in range(cases_large):
            ligne.append(False)
        new_grid.append(ligne)
    return new_grid

def affiche_str():
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
    return (pixel_position[1] // cases_pixels, pixel_position[0] // cases_pixels)

def flipItPlease(pos):
    if case(pos):
        grid[ pos[0] ][ pos[1] ] = False
    else:
        grid[ pos[0] ][ pos[1] ] = True

def randomized():
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
    memory = []
    for i in range(taille_memoire):
        memory.append(grid[:])
    return memory

def memory():
    global past
    past = past[1:]
    past.append(grid[:])

def save_grid(grid):
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
        new_grid.append(new_ligne[:])
    return new_grid

largeur_pixel = cases_large * cases_pixels
hauteur_pixel = cases_haut * cases_pixels

pygame.init()
fenetre = pygame.display.set_mode((largeur_pixel,hauteur_pixel))

living_cell = pygame.Surface((cases_pixels,cases_pixels))
living_cell.fill(living_color)

dead_cell = pygame.Surface((cases_pixels, cases_pixels))
dead_cell.fill(dead_color)

pygame.key.set_repeat(1000,100)

grid = init_grid()

pause = True
changed_intervalle_evo = intervalle_evo
n = 0
pos_temporelle = 0
past = init_memoire()

continuer = True
end_gen = time.time()
while continuer:

    if not pause:
        #test = time.time()
        grid = refresh()
        #print(time.time() - test)

        memory()

        time_to_wait = positif(changed_intervalle_evo - (time.time() - end_gen))
        time.sleep(time_to_wait)

        affiche()


    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                position = whereiam(event.pos)
                flipItPlease(position)
                affiche()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False

            if event.key == K_p:
                pause = not pause
                if not pause:
                    pos_temporelle = 0

            if event.key == K_r:
                grid = randomized()
                memory()
                affiche()

            if event.key == K_h:
                grid = symetric_horizontal()
                memory()
                affiche()

            if event.key == K_g:
                grid = symetric_vertical()
                memory()
                affiche()

            if event.key == K_v:
                grid = init_grid()
                memory()
                affiche()

            if event.key == K_f:
                changed_intervalle_evo = round(changed_intervalle_evo - 0.02, 2)
                if changed_intervalle_evo < 0:
                    changed_intervalle_evo = 0.00
                print(changed_intervalle_evo," secondes entre générétions")

            if event.key == K_d:
                changed_intervalle_evo = round(changed_intervalle_evo + 0.02, 2)
                if changed_intervalle_evo < 0:
                    changed_intervalle_evo = 0.00
                print(changed_intervalle_evo," secondes entre générétions")

            if event.key == K_LEFT:
                if pos_temporelle > -taille_memoire + 1:
                    pause = True
                    pos_temporelle -= 1
                    grid = past[pos_temporelle -1]
                    affiche()

            if event.key == K_RIGHT:
                if pos_temporelle < 0:
                    pause = True
                    pos_temporelle += 1
                    grid = past[pos_temporelle -1]
                    affiche()

            if event.key == K_z:
                grid = init_grid()
                changed_intervalle_evo = intervalle_evo
                pause = True
                n = 0
                affiche()

            if event.key == K_s:
                save_grid(grid)

            if event.key == K_w:
                grid = grid_from_file(fichier_source)
                affiche()


    end_gen = time.time()
    n += 1


###     Fin du fichier
################################################################################
