#!/usr/bin/env bash


## CONSTANTS

USER_JENKINS="jenkins"
CLUSTER_NAME="githoster-prod"
NODE_TYPE="t2.micro"
NODES_NUMBER=1
CLUSTER_REGION="eu-west-1"
# Constants listing packages and modules to have installed at the end of the environment set up.
PACKAGES_LIST="git default-jdk apt-transport-https ca-certificates curl software-properties-common unzip docker.io awscli"


## METHODS

# Check if a package is already installed on the machine, if not then install it.
ij_check_install_package() {
    echo "INFO > ij_check_install_package"
    PACKAGE_NAME="$1"
    echo "INFO > ij_check_install_package : install $PACKAGE_NAME"
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
    echo "INFO > ij_install_packages"
	for i in $( seq 1 1 $# ); do 
		PACKAGE=${!i}
		echo "$PACKAGE will be installed"
    # Instalation du package
		ij_check_install_package "$PACKAGE"
	done
}

# Get Jenkins package, then install it.
ij_install_jenkins() {
    echo "INFO > ij_install_jenkins"
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
    echo "INFO > ij_launche_jenkins"
    # Start the Jenkins server
    systemctl start jenkins
    # Enable the Jenkins service to load during the boot
    systemctl enable jenkins
}

# Allow docker to be used by the user without using "sudo".
ij_enable_docker_for_jenkins_user() { 
    echo "INFO > ij_enable_docker_for_jenkins_user"
    usermod -aG docker $USER_JENKINS
    systemctl enable docker
}

# Get and install Gradle manually. Gradle is used in the build process, called by the Jenkinsfile.
ij_install_gradle() {
    echo "INFO > ij_install_gradle"
    wget https://services.gradle.org/distributions/gradle-7.0-bin.zip -P /tmp
    unzip -d /opt/gradle /tmp/gradle-*.zip

    echo 'export GRADLE_HOME=/opt/gradle/gradle-7.0 \
    export PATH=${GRADLE_HOME}/bin:${PATH}' >> /etc/profile.d/gradle.sh


    chmod +x /etc/profile.d/gradle.sh
    source /etc/profile.d/gradle.sh
    ln -s /opt/gradle/gradle-7.0/bin/gradle /usr/bin/gradle

    rm -f /tmp/gradle-*.zip
}

ij_give_rights_user_jenkins(){
    echo "INFO > ij_give_rights_user_jenkins"
    if id "$USER_JENKINS" 2>/dev/null ; then
        echo "INFO > user jenkins exists - upgrading rights"
        # rajout des droits
        sudo cp /etc/sudoers /etc/sudoers.old
        echo "$USER_JENKINS ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
    fi
}

# Print the initial admn password in the logs of the vagrant up command. When retrieved can be used with ease by the admin to perform first configuration of the server.
ij_get_jenkins_admin_password() {
    echo "INFO > ij_get_jenkins_admin_password"
    cat /var/lib/jenkins/secrets/initialAdminPassword
}

ij_configure_aws_cli() {
    echo "INFO > ij_configure_aws_cli"
    aws configure set default.region us-east-1
    aws configure set aws_access_key_id $AWS_ACCESS_KEY
    aws configure set aws_secret_access_key $AWS_SECRET_KEY
}

ij_install_kubectl() {
    echo "INFO > ij_install_kubectl"
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x ./kubectl
    mv ./kubectl /usr/local/bin
}

ij_install_eksctl() {
    echo "INFO > ij_install_eksctl"
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
    chmod +x /tmp/eksctl
    mv /tmp/eksctl /usr/local/bin
}

ij_create_cluster() {
    echo "INFO > ij_create_cluster"
    CLUSTER_NAME="$1"
    eksctl create cluster --name $CLUSTER_NAME --region $CLUSTER_REGION --nodegroup-name worker-nodes --node-type $NODE_TYPE --nodes $NODES_NUMBER
}

## MAIN PROCESS

apt-get update
# Install all needed packages, for aws, docker and git.
ij_install_packages $PACKAGES_LIST
# Install Jenkins
ij_install_jenkins
# Start Jenkins server enable it to be launched again on boot.
ij_launch_jenkins
# Give admin rights to user jenkins
ij_give_rights_user_jenkins
# Make Docker use from Jenkins.
ij_enable_docker_for_jenkins_user
# Install gradle with a recent version.
ij_install_gradle
ij_configure_aws_cli
ij_install_kubectl
ij_install_eksctl
ij_create_cluster $CLUSTER_NAME
# Display the initial admin password in the logs of the vagrant up to allow the admin to configure it.
ij_get_jenkins_admin_password