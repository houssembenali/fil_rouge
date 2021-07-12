from modules.parametrage import bdd_file
from modeles import ParamBucket


def create_bucket_name(param: ParamBucket):
    """
    Methode qui va permettre de créer un nouveau bucket
    :return:
    """
    return bdd_file.write_bd(param.nom_bucket)


def update_bucket_by_name(update_bucket):
    pass

def get_bucket_name():
    for bucket in bdd_file.read_bd():
        if bucket is not None:
            return bucket
            print(bucket)  
    return ""