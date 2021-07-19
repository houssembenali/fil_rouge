import csv
import constants as cs
import git
import shutil
import stat
import os

def addProject(resultat):
    nom = resultat['name']
    link = resultat['link']
    error = ""
    if not isNameExist(nom):
        if not isUrlExist(link):
            if isUrlExistInNet(link):
                id = getNewId()
                with open(cs.PROJECT_FILE_PATH, mode='a',newline='') as projects_file:
                    projects_writer = csv.writer(projects_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    projects_writer.writerow([id,nom,link])
            else:
                error = "L'URL Git du projet "+ nom + " n'est pas accecible. Projet non ajouter, merci de verifier votre lien SVP"
        else:
            error = "L'URL Git du projet "+ nom + " existe deja. Projet non ajouter"
    else:
        error = 'Le nom '+ nom + ' existe deja. Projet non ajouter'
    return error
    

def isUrlExistInNet(link):
    exist =True
    try:
    #filelist = [ f for f in os.listdir("temp/clone") ]
       for f in os.listdir("temp/clone"):
          shutil.rmtree(os.path.abspath("temp/clone/"+f))
    
    #shutil.rmtree("temp/clone")
       git.Git("temp/clone").clone(link)    
    
    except git.exc.GitError:
        print("ERROR! "+ link +" does not exist")
        exist = False
    return exist
    
    
def isNameExist(name):
    exist = False
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if name == list({row[1]})[0]:
               exist=True
    return exist

def isUrlExist(name):
    exist = False
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if name == list({row[2]})[0]:
               exist=True
    return exist

def getNewId():
    max = 1
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if max < int(list({row[0]})[0]):
               max=int(list({row[0]})[0])
    max=max+1
    return max