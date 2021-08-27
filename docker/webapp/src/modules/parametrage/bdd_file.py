import os
import constants as cs

def read_bd():
    """
        Methode permettant d'aller lire les données qui se trouve dans notre fichier
    :return:
    """
    if os.path.isfile(cs.FILE_PATH) and os.access(cs.FILE_PATH, os.R_OK):
        with open(cs.FILE_PATH, "r") as read_file:
            return read_file.readlines()
    else:
        print("Either the file is missing or not readable")
    return ""

        
def write_bd(data):
    """
        Methode permettant de mettre à jour
    :param data: list data qu'on va mettre dans notre fichier
    :return:
    """
    with open(cs.FILE_PATH, "w", encoding="utf-8") as read_file:
        read_file.write(str(data))
