import os
from _ast import If
import constants as cs
####################################################################
############ Service du module liste des projets ###################
####################################################################


###  lire la liste du projet a partir du fichier 

def getAllProject():
    
    if not os.path.exists(cs.PROJECT_FILE_PATH):
        f = open(cs.PROJECT_FILE_PATH, "w")
        f.close()
        
    list_projets=[]
    f = open(cs.PROJECT_FILE_PATH, "r")
    Lines = f.readlines()
    count = 0
    for line in Lines:
        count += 1
        list_projets.append(line.split(";"))
    return list_projets