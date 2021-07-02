echo "Start provisioning"

echo "Installing Jenkins from provisioning"
wget -O - https://gist.githubusercontent.com/houssembenali/b72d1403b102566fbfb5d38caf6d9cef/raw/d42b836cafcb8cb1d3d666eb2d9a2fc6a4f6cb23/jenkins-installation.sh | bash

echo "Installing Docker CE from provisioning"
wget -O - https://gist.githubusercontent.com/houssembenali/6eeb306494ca66aa91a941f6a373fcd7/raw/d6af1424d66de03ad06c259cf9ebecbd50e63ad3/docker-installation.sh | bash

sudo usermod -aG docker jenkins

echo "End provisioning"