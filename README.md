# Conway-Game-of-life
Personal project in python, feel free to use the code

## To use the program :
### Basics :

**P** : pause/resume  
**Left clic** : change the state of the clicked cell  
**Escape** : quit  
**V** : recreate a new grid  
**Z** : re-start everything  

**Left_arrow** : navigate in the past grid  
**Right_arrow** : navigate in the past grid  

**F** : decrease the time between generations  
**D** : increase the time between generations  

**R** : generate a random grid  
**G** : vertical symmetry  
**H** : horizontal symmetry  

**S** : save the grid in a file  
**W** : recreate a grid from the file (see "Files" in detailed section)  

### Detailed :
**Size of the grid** :
To change the size of the grid you need to change the "cases_haut" (height),"cases_large" (width) and "cases_pixels" (size of a cell in pixel) at the beginning of the program

**Files** :
Positions are saved in text files. To choose the file you want to charge you need to change the "fichier_source" at the beginning of the program

**Time between generations** :
The time between generation is the minimum time. Because if the computer take 1 seconde to generate the next step, you cant be faster than it. If the maths take too long, the next step will start immediatly.  
The defaut value is at the beggining of the program : "default_time_gap"
