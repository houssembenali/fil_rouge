import os
import constants as cs

import git
import markdown
import md_toc
from pathlib import Path
from modules.parametrage import crud
import utils
import wordings

EN_TETE_SOMMAIRE = "# SOMMAIRE \n"

###################################################################################
############ Service du module liste et publication des projets ###################
###################################################################################


###  lire la liste du projet a partir du fichier 

def get_all_projects():
    
    if not os.path.exists(cs.PROJECT_FILE_PATH):
        f = open(cs.PROJECT_FILE_PATH, "w")
        f.close()
        
    list_projets=[]
    f = open(cs.PROJECT_FILE_PATH, "r")
    lines = f.readlines()
    for line in lines:
        list_projets.append(line.split(";"))
    return list_projets


'''
    A partir d'une adresse de dossier, récupérer la liste de tous les fichiers markdown
'''
def __get_list_of_files(dirname):
    # création de la liste de fichiers et sous-dossiers à partir de dossier parent stocker dans la variable "dirName"
    listofcontentindir = os.listdir(dirname)
    allfilesindir = list()
    # parcourir la liste (composée de fichiers et sous-dossiers)
    for entry in listofcontentindir:
        # composition de l'adresse complette 
        entryfullpath = os.path.join(dirname, entry)
        # si l'élément est un dossier ALORS récupérer la liste des fichier et sous-dossier du contenu 
        if os.path.isdir(entryfullpath):
            allfilesindir = allfilesindir + __get_list_of_files(entryfullpath)
        else:
            # récupérer uniquement les fichiers markdown
            pathTab = entryfullpath.split(".")
            if pathTab[len(pathTab)-1].upper() == "MD":
                allfilesindir.append(entryfullpath)
                
    return allfilesindir



'''
    Cloner le projet dans le dossier de clonnage situé dans le dossier temporaire
'''    
def __clone_project(link):
    utils.check_temp_dir(cs.TMP_CLONE_PATH)

    # vider le dossier temporaire du clonage
    utils.vider_dossier(cs.TMP_CLONE_PATH)

    print("cloning ...")
    try:
        git.Git(cs.TMP_CLONE_PATH).clone(link.strip())
    except git.exc.CommandError:
        return False
    print("cloning ok")

    return True
'''
    Méthode principal de la conversion et l'upload du projet
'''  
def publish_from_file_by_id(link,issummary):
	
	bucketname = crud.get_bucket_name()
	if bucketname == "":
		return wordings.NOM_BUCKET_NON_CONFIGURE
	
	projectname = os.path.splitext(os.path.basename(link))[0]
	mainpath = cs.TMP_CLONE_PATH

	iscloned = __clone_project(link)
	if not iscloned:
		return wordings.PROJET_NON_PUBLIE_ERREUR_CLONAGE.format(name=projectname)
	
    #Parcourir les fichiers MarkDown
	listfilemd = __get_list_of_files(mainpath + '/' + projectname)
	for mdfile in listfilemd:
		with open(mdfile) as f:
			try:
    				mdcontent = f.read()
			except Exception:
				print("Erreur de lecture du fichier : " + mdfile)
            #Ajout Sommaire
			if issummary:
				mdcontent=EN_TETE_SOMMAIRE + md_toc.build_toc(mdfile) + mdcontent
			#Conversion du contenu MD vers contenu HTML 
			htmlcontent = markdown.markdown(mdcontent)
            # Préparation des variable util pour réspécter l'arborescence des dossiers et sous-dossier pour les fichiers HTML 
			tabpath = mdfile.split("/")
            # extraction nom du fichier
			filename = tabpath[len(tabpath)-1]
			filename = os.path.splitext(filename)[0]
            # extraction des sous-dossiers
			subfolder = mdfile.replace(mainpath,"").replace(filename+".md","")
            # Vérifier et créer l'arborescence des sous-dossiers
			Path(mainpath+"/html/"+subfolder).mkdir(parents=True, exist_ok=True)
            # Génération du fichier HTML
			with open (mainpath+"/html/"+subfolder+filename+".html", "w") as fHtml:
				fHtml.write(htmlcontent)
    #Partie upload

	print('Upload du projet '+projectname)
	os.system('aws s3 sync '+mainpath+'/html/'+projectname+ " s3://"+bucketname + " --acl public-read")
	utils.vider_dossier(cs.TMP_CLONE_PATH)
	return ""
