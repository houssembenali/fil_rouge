#!/usr/bin/env bash

# Constants listing packages and modules to have installed at the end of the environment set up.
PACKAGES_LIST="python3 python3-dev python3-pip git"
PYTHON_MODULES_LIST="flask markdown pylint GitPython"

# Check if a package is already installed on the machine, if not then install it.
ip_check_install_package() {
    PACKAGE_NAME="$1"
	apt update
    if ! dpkg -l |grep --quiet "^ii.*$PACKAGE_NAME " ; then
        apt install -y "$PACKAGE_NAME"
		echo "$PACKAGE_NAME has been installed"
    else
        echo ""
        echo "$PACKAGE_NAME was already installed."
    fi
}


# Allows to pass a list of packages as parameter. Then summon the ps_check_install_package method on each element of the list.
ip_install_packages() {
	for i in $( seq 1 1 $# ); do 
		PACKAGE=${!i}
		echo "$PACKAGE will be installed"
    # Instalation du package
		ip_check_install_package "$PACKAGE"
	done
}


# Allows to pass a list of python modules as parameter. Then install them with pip3.
ip_install_python_modules() {
    for i in $( seq 1 1 $# ); do 
		MODULE=${!i}
		echo "$MODULE will be installed"
    # Installation du module
		pip install "$MODULE"
	done
}


# Checks if python can be found in /usr/bin/. If yes remove python. Anyway, link python3 command to python command in /usr/bin/.
ip_link_python_to_python3() {
    if [ -f "/usr/bin/python" ] ; then
        echo "python1 is installed. Remove it and create link to call python3 with python command."
        apt remove -y python
        ln -s /usr/bin/python3 /usr/bin/python
    else
        echo "Create link to call python3 with python command."
        ln -s /usr/bin/python3 /usr/bin/python
    fi
}


# Create a pip alias for pip3.
ip_link_pip_to_pip3() {
    if [ -f "/usr/bin/pip" ] ; then
        echo "pip is installed. Remove it and create link to call pip3 with pip command."
        apt remove -y python-pip
        ln -s /usr/bin/pip3 /usr/bin/pip
    else
        echo "Create link to call python3 with python command."
        ln -s /usr/bin/pip3 /usr/bin/pip
    fi
}
apt-get update
# Install all needed packages, for python and git.
ip_install_packages $PACKAGES_LIST
# Remove python if installed to keep only python3, and create link to be able to call python3 with python alias.
ip_link_python_to_python3
# Create pip alias for pip3.
ip_link_pip_to_pip3
# Install python modules for development.
ip_install_python_modules $PYTHON_MODULES_LIST