import csv
import os
import shutil
import wordings

def is_index_valid(index):
    return index > 0

# Supprime un projet du fichier de listing à l'aide de son id. Retourne un message 
# d'erreur si le projet n'est pas trouvé.
def delete_from_file_by_id(id,path):
    messageretour = ""
    projects_file = open(path, "r")
    lines = projects_file.readlines()
    projects_file.close()
    # supprimer la ligne.
    index = __find_from_file_by_id(id,path)
    if not is_index_valid(index):
        messageretour = wordings.PROJET_NON_SUPPRIME_ID_INTROUVABLE
    else:
        del lines[index]
        # Réecrire le fichier après suppression de la ligne.
        new_file = open(path, "w+")
        for line in lines:
            new_file.write(line)
        new_file.close()
    return messageretour

# Cherche dans le fichier de listing des projets les informations d'un projet à l'aide de son id. 
# Renvoie l'id si trouvé.        
def __find_from_file_by_id(id, path):
    with open(path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        line_count = -1
        for row in reader:
                line_count +=1
                if id == row[0]: # if the username shall be on column 3 (-> index 2)
                    print ('existe dans la colon N '+str(line_count))
                    return line_count
    print ('projet non trouvée ID= '+str(id))
    return -1

# Vide le dossier données.
def vider_dossier(chemin):
    for f in os.listdir(chemin):
        if os.path.isdir(chemin+"/"+f):
            shutil.rmtree(os.path.abspath(chemin+"/"+f))

# Création du répertoire s'il n'existe pas.
def check_temp_dir(dirName):
    try:
        os.makedirs(dirName)    
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")