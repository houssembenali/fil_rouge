import os
from _ast import If
import constants as cs

import git
import markdown
from pathlib import Path
from modules.parametrage import crud
from modules.addproject.addprojet import checkTempDir
from utils import viderdossier

###################################################################################
############ Service du module liste et publication des projets ###################
###################################################################################


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


'''
    A partir d'une adresse de dossier, récupérer la liste de tous les fichiers markdown
'''
def getListOfFiles(dirName):
    # creation de list de fichiers et sous-dossier a partir de dossier parent stocker dans la variable "dirName"
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # parcourir la liste (composer de fichiers et sous-dossier)
    for entry in listOfFile:
        # composition de l'adresse complette 
        fullPath = os.path.join(dirName, entry)
        # si l'élément est un dossier ALORS récupérer la liste des fichier et sous-dossier du contenu 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            # récupérer uniquement les fichiers markdown
            pathTab = fullPath.split(".")
            if pathTab[len(pathTab)-1].upper() == "MD":
                allFiles.append(fullPath)
                
    return allFiles



'''
    Cloner le projet dans le dossier de clonnage situé dans le dossier temporaire
'''    
def cloneProject(link):
    checkTempDir(cs.TMP_CLONE_PATH)

    # vider le dossier temporaire du clonage
    viderdossier(cs.TMP_CLONE_PATH)

    print("cloning ...")
    try:
        git.Git(cs.TMP_CLONE_PATH).clone(link.strip())
    except:
        return False
    print("cloning ok")

    return True
'''
    Méthode principal de la conversion et l'upload du projet
'''  
def publishFromFileById(id, name,link):
	projectName =os.path.splitext(os.path.basename(link))[0]
	mainPath = cs.TMP_CLONE_PATH

	isCloned = cloneProject(link)
	if not isCloned:
		return "le projet '" + projectName +"' non publié. Problème lors du clonage du répository GIT"
    #variables
	
    #Parcourir les fichiers MarkDown
	lst = getListOfFiles(mainPath+ '/' +projectName)
	for e in lst:
		with open(e) as f:
			try:
    				mdContent = f.read()
			except:
				print("Erreur de lécture du fichier : "+e)
            #Conversion du contenu MD vers contenu HTML 
			htmlContent = markdown.markdown(mdContent)
			
            # Préparation des variable util pour réspécter l'arborescence des dossiers et sous-dossier pour les fichiers HTML 
			tabPath = e.split("/")
            # extraction nom du fichier
			fileName = tabPath[len(tabPath)-1]
			fileName = os.path.splitext(fileName)[0]
            # extraction des sous-dossiers
			subFolder = e.replace(mainPath,"").replace(fileName+".md","")
            # Vérifier et créer l'arborescence des sous-dossiers
			Path(mainPath+"/html/"+subFolder).mkdir(parents=True, exist_ok=True)
            # Génération du fichier HTML
			with open (mainPath+"/html/"+subFolder+fileName+".html", "w") as fHtml:
				fHtml.write(htmlContent)
    #Partie upload
	bucketName = crud.get_bucket_name()
	if bucketName == "":
		return "Le nom du Bucket n'est pas configurer, merci de le configurer"

	print('Upload du projet '+projectName)
	os.system('aws s3 sync '+mainPath+'/html/'+projectName+ " s3://"+bucketName + " --acl bucket-owner-full-control --acl public-read")
	viderdossier(cs.TMP_CLONE_PATH)
	return ""