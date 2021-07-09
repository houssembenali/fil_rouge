#!/usr/bin/env bash
apt-get update
# install python
apt-get install python3 python3-dev python3-pip -q -y
apt remove -y python

# positionnement de python3 et pip3 dans le profil
ps_verif_dossier_pyhton() {
    
    if [ -f "/usr/bin/python" ] ; then
        echo "file exist"
    else
        sudo ln -s /usr/bin/python3 /usr/bin/python
    fi
}
ps_verif_dossier_pyhton
sudo echo "alias pip=pip3" > ~/.bashrc
