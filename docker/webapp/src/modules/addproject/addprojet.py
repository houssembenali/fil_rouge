import csv
import constants as cs
import git
import shutil
import stat
import os

# Méthode principal de vérification et insértion de projet
def addProject(resultat):
    checkTempDir(cs.TMP_CLONE_PATH)
    nom = resultat['name']
    link = resultat['link']
    error = ""
    if not isNameExist(nom):
        if not isUrlExist(link):
            if isUrlExistInNet(link):
                id = getNewId()
                insertProject(id,nom,link)
            else:
                error = "L'URL Git du projet "+ nom + " n'est pas accecible. Projet non ajouter, merci de verifier votre lien SVP"
        else:
            error = "L'URL Git du projet "+ nom + " existe deja. Projet non ajouter"
    else:
        error = 'Le nom '+ nom + ' existe deja. Projet non ajouter'
    return error



def insertProject(id,nom,link):
    with open(cs.PROJECT_FILE_PATH, mode='a',newline='') as projects_file:
        projects_writer = csv.writer(projects_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        projects_writer.writerow([id,nom,link])
    
# Verification de l'existance de l'URL dans internet (github, gitlab, ...)
def isUrlExistInNet(link):
    exist =True
    try:
       for f in os.listdir(cs.TMP_CLONE_PATH):
        if os.path.isdir(cs.TMP_CLONE_PATH+f):   
           shutil.rmtree(os.path.abspath(cs.TMP_CLONE_PATH+f))
       git.Git(cs.TMP_CLONE_PATH).clone(link)    
    except git.exc.GitError:
        print("ERROR! "+ link +" does not exist")
        exist = False
    return exist
    

# Verifier si le nom existe deja dans notre base de donnee
def isNameExist(name):
    exist = False
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if name == list({row[1]})[0]:
               exist=True
    return exist

# Verifier si l'URL existe deja dans notre base de donnee
def isUrlExist(name):
    exist = False
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if name == list({row[2]})[0]:
               exist=True
    return exist

# Recuperer le dernier ID utiliser dans la liste des projet
def getNewId():
    max = 1
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if max < int(list({row[0]})[0]):
               max=int(list({row[0]})[0])
    max=max+1
    return max

# Creation du repertoir s'il n'existe pas
def checkTempDir(dirName):
    try:
        os.makedirs(dirName)    
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")