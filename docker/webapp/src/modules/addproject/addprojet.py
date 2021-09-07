import csv
import constants as cs
import git
import shutil
import os
import utils

# Ajoute le projet et ses informations au fichier de listing des projets. Si des erreurs sont rencontrées,
#  renvoie une string pour tracer le soucis.
def add_project(resultat):
    utils.check_temp_dir(cs.TMP_CLONE_PATH)
    nom = resultat['name']
    link = resultat['link']
    error = ""
    if not __is_name_exist(nom):
        if not __is_url_exist(link):
            if __is_url_exist_in_net(link):
                id = __get_new_id()
                with open(cs.PROJECT_FILE_PATH, mode='a',newline='') as projects_file:
                    projects_writer = csv.writer(projects_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    projects_writer.writerow([id,nom,link])
            else:
                error = "L'URL Git du projet "+ nom + " n'est pas accessible. Projet non ajouté, merci de vérifier votre lien SVP."
        else:
            error = "L'URL Git du projet "+ nom + " existe deja. Projet non ajouté."
    else:
        error = 'Le nom '+ nom + ' existe deja. Projet non ajouté.'
    return error
    
# Vérification de l'existence de l'URL dans Github ou Gitlab. Si l'url existe, clone le projet.
def __is_url_exist_in_net(link):
    isurlvalid =True
    try:
       for f in os.listdir(cs.TMP_CLONE_PATH):
        if os.path.isdir(cs.TMP_CLONE_PATH+f):   
           shutil.rmtree(os.path.abspath(cs.TMP_CLONE_PATH+f))
       git.Git(cs.TMP_CLONE_PATH).clone(link)    
    except git.exc.GitError:
        print("ERROR! "+ link +" does not exist")
        isurlvalid = False
    return isurlvalid
    

# Vérifie si le nom existe déjà dans notre base de données.
def __is_name_exist(name):
    hasname = False
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if name == list({row[1]})[0]:
               hasname=True
    return hasname

# Vérifie si l'URL existe déjà dans notre base de données.
def __is_url_exist(name):
    hasurl = False
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if name == list({row[2]})[0]:
               hasurl=True
    return hasurl

# Récupérer le dernier ID utilisé dans la liste des projets.
def __get_new_id():
    maxid = 1
    with open(cs.PROJECT_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if maxid < int(list({row[0]})[0]):
               maxid=int(list({row[0]})[0])
    maxid=maxid+1
    return maxid