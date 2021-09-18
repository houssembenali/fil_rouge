from modules.parametrage import bdd_file


def create_bucket_name(paramBucket):
    """
    Méthode qui va permettre de créer un nouveau bucket.
    :return:
    """
    return bdd_file.write_bd(paramBucket)


def get_bucket_name():
    """
        Méthode qui va permettre de récupérer un bucket.
    :return:
    """
    for bucket in bdd_file.read_bd():
        if bucket is not None:
            return bucket
    return ""