#!/usr/bin/env bash


## CONSTANTS

# Constants listing packages and modules to have installed at the end of the environment set up.
PACKAGES_LIST="python3 python3-dev python3-pip git default-jdk apt-transport-https ca-certificates curl software-properties-common unzip"


## METHODS

# Check if a package is already installed on the machine, if not then install it.
ij_check_install_package() {
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
ij_install_packages() {
	for i in $( seq 1 1 $# ); do 
		PACKAGE=${!i}
		echo "$PACKAGE will be installed"
    # Instalation du package
		ij_check_install_package "$PACKAGE"
	done
}


# Checks if python can be found in /usr/bin/. If yes remove python. Anyway, link python3 command to python command in /usr/bin/.
ij_link_python_to_python3() {
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
ij_link_pip_to_pip3() {
    if [ -f "/usr/bin/pip" ] ; then
        echo "pip is installed. Remove it and create link to call pip3 with pip command."
        apt remove -y python-pip
        ln -s /usr/bin/pip3 /usr/bin/pip
    else
        echo "Create link to call python3 with python command."
        ln -s /usr/bin/pip3 /usr/bin/pip
    fi
}

# Get Jenkins package, then install it.
ij_install_jenkins() {
    # Download Jenkins package. 
    # You can go to https://pkg.jenkins.io/debian/ to see the available commands
    # First, add a key to your system
    wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | apt-key add -

    # Add the following entry in your /etc/apt/sources.list:
    echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list

    ij_check_install_package 'jenkins'
}

# Manage to start JEnkins service and to make sure it will be relaunched every time at boot.
ij_launch_jenkins() {
    # Start the Jenkins server
    systemctl start jenkins
    # Enable the Jenkins service to load during the boot
    systemctl enable jenkins
}

# Get Docker and install it. Docker will be used for creating and publishing the image to DockerHub, and to run it for testing purposes.
ij_install_docker() {
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    apt-key fingerprint 0EBFCD88
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

    ij_check_install_package 'docker_ce'
}

# Allow docker to be used by the user without using "sudo".
ij_enable_docker_for_jenkins_user() {
    groupaad docker 
    usermod -aG docker $USER
    systemctl enable docker
}

# Get and install Gradle manually. Gradle is used in the build process, called by the Jenkinsfile.
ij_install_gradle() {
    wget https://services.gradle.org/distributions/gradle-7.0-bin.zip -P /tmp
    unzip -d /opt/gradle /tmp/gradle-*.zip

    echo 'export GRADLE_HOME=/opt/gradle/gradle-7.0 \
    export PATH=${GRADLE_HOME}/bin:${PATH}' >> /etc/profile.d/gradle.sh


    chmod +x /etc/profile.d/gradle.sh
    source /etc/profile.d/gradle.sh
    ln -s /opt/gradle/gradle-7.0/bin/gradle /usr/bin/gradle

    rm -f /tmp/gradle-*.zip
}

# PRint the initial admn password in the logs of the vagrant up command. When retrieved can be used with ease by the admin to perform first configuration of the server.
ij_get_jenkins_admin_password() {
    cat /var/lib/jenkins/secrets/initialAdminPassword
}


## MAIN PROCESS

apt-get update
# Install all needed packages, for python and git.
ij_install_packages $PACKAGES_LIST
# Remove python if installed to keep only python3, and create link to be able to call python3 with python alias.
ij_link_python_to_python3
# Create pip alias for pip3.
ij_link_pip_to_pip3
# Install Jenkins
ij_install_jenkins
# Start Jenkins server enable it to be launched again on boot.
ij_launch_jenkins
# Install Docker.
ij_install_docker
# Make Docker use from Jenkins.
ij_enable_docker_for_jenkins_user
# Install gradle with a recent version.
ij_install_gradle
# Display the initial admin password in the logs of the vagrant up to allow the admin to configure it.
ij_get_jenkins_admin_password