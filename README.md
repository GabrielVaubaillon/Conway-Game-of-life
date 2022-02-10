# Conway-Game-of-life

## Divers
- programme écrit en python en utilisant la bibliotheque [Pygame](https://www.pygame.org).
- développé sur Manjaro-KDE, par un étudiant pour le loisir. Aucune garantie de fonctionnement correct sur votre machine.
- README rédigé en avance sur la prochaine mise à jour. Le fichier *config.py* n'existe pas encore. Dans le reste de ce fichier lisez *config.py* comme "au début du programme".

## Utilisation  

### Liste touches
*(réglable dans config.py)*

**P** : Pause/reprendre/commencer  
**Left clic** : change l'état de la cellule cliquée   
**Escape** : quit  
**V** : grille vierge  

**L** : Afficher le quadrillage  

**F** : Diminue le temps entre les générations  
**D** : Augmente le temps entre les générations  
**C** : Remet le temps entre les générations à la valeur par défaut  

**R** : Génère un état aléatoire  
**G** : symétrie par rapport à un axe vertical  
**H** : symétrie par rapport à un axe horizontal  

**M** : Entrer en mode mémoire *(voir partie détaillée)*  
**Arrows** : Se déplacer dans la mémoire  
**W en mode mémoire** : rétablir la position


**S** : Sauvegarde de l'état actuel dans un fichier  
**W** : Charge le fichier dans le coin haut gauche  
**X** : Charge le fichier au centre  

### Détails d'utilisation
  Ce programme est un réalisation en Python du jeu de la vie de Conway.
  - Vous pouvez gérer la **taille** du jeu dans le fichier *config.py*
    - Toutes les cellules hors de l'espace de jeu sont considérées comme mortes
  - Vous pouvez changer les **couleurs** dans le fichier *config.py*
  - Vous pouvez **cliquer** sur l'espace du jeu pour changer l'état des cellules.  
  - Par défaut le jeu commence en pause.  
  - Vous controlez la **pause** avec la touche P.  
  - Vous pouvez controler le **temps entre les générations** en utilisants les touches F,D et C.   
    - Le temps de calcul de l'ordinateur est soustrait à la valeur. Si le temps de calcul est inférieur à la valeur, celle ci est exacte, sinon elle est remplacée par le temps de calcul
  - Vous pouvez générer un espace de jeu **aléatoire** avec la touche R. Lors de cette action le programme va parcourir l'ensemble de l'espace et attribuer avec une certaine repartition les états morts ou vivant. *(réglable dans config.py)*  
  - Vous pouvez réaliser des **symétries** sur l'espace de jeu avec les touches G et H.  
  - Le **quadrillage** est caché par défaut *(réglable dans config.py)*, pour l'afficher ou le cacher une fois le jeu lancé, appuyez sur L.
  - Vous pouvez **sauvegarder** l'état actuel du jeu en appuyant sur la touche S. Le nom du fichier sera composé de la date, de l'année aux secondes. *(work in progress : réaliser des noms plus "user friendly")*
  - Vous pouvez **charger le fichier** spécifié dans *config.py* en appuyant soit sur W (pour le charger dans le coin supérieur gauche) soit sur X (pour le charger au centre).
  - Les états successifs sont conservés en mémoire. Vous pouvez naviguer parmis eux en passant en **mode mémoire** avec la touche M.  
    - Vous entrez automatiquement en mode pause
    - Vous ne pouvez pas intéragir avec les états
    - Vous pouvez naviguer parmi les états en utilisant les fleches gauche et droite
    - Seulement un certain nombre d'état peuvent être stockés *(réglable dans config.py)*
    - Vous pouvez quitter le mode mémoire en appuyant sur P. Vous serez cependant toujours en pause.
    - Vous pouvez rétablir une position de la mémoire en appuyant sur W. Vous sortez alors du mode mémoire.



## Work in Progress  
- Accélération des traitemenents
- Mise en place d'un fichier séparé pour la configuration du programme
- Choix multiple pour charger les fichiers
- Meilleurs noms pour les fichiers


