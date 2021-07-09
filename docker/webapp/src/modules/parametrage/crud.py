from modules.parametrage import bdd_file
from modeles import ParamBucket

def create_bucket_name(param):
    """
    Methode qui va permettre de créer un nouveau bucket
    :return:
    """
    #param: ParamBucket param.nom_bucket
    return bdd_file.write_bd(param)


def update_bucket_by_name(update_bucket):
    pass
    
