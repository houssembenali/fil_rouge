import os
from _ast import If
####################################################################
############ Service du module liste des projets ###################
####################################################################
PROJECT_FILE_PATH = "DB/projects.txt"


###  lire la liste du projet a partir du fichier 

def getAllProject():
    
    if not os.path.exists(PROJECT_FILE_PATH):
        f = open(PROJECT_FILE_PATH, "w")
        f.close()
        
    list_projets=[]
    f = open(PROJECT_FILE_PATH, "r")
    Lines = f.readlines()
    count = 0
    for line in Lines:
        count += 1
        list_projets.append(line.split(";"))
    return list_projets