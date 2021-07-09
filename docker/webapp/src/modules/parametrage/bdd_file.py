import os 
import json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
file_param = os.path.join(THIS_FOLDER, 'param-file.txt')


def read_bd():
    """
        Methode permettant d'aller lire les données qui se trouve dans notre fichier
    :return:
    """
    with open(file_param, "r") as read_file:
        return read_file.readlines()


def write_bd(data):
    """
        Methode permettant de mettre à jour
    :param data: list data qu'on va mettre dans notre fichier
    :return:
    """
    with open(file_param, "w", encoding="utf-8") as read_file:
        read_file.write(str(data))

