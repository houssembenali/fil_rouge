#!/bin/sh
# Définition des variables :
AWS_REGION=$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]')
VPC_NAME="VPC_EQUIPE_4"
VPC_CIDR="10.0.0.0/16"
SUBNET_PUBLIC_CIDR="10.0.1.0/24"
SUBNET_PUBLIC_AZ=$AWS_REGION"a"
SUBNET_PUBLIC_NAME="10.0.1.0 - "$AWS_REGION"a"
SUBNET_PRIVATE_CIDR="10.0.2.0/24"
SUBNET_PRIVATE_AZ=$AWS_REGION"b"
SUBNET_PRIVATE_NAME="10.0.2.0 - "$AWS_REGION"b"
CHECK_FREQUENCY=5
KEY_NAME="key_Equipe_1"
IMAGE_ID="ami-0f7cd40eac2214b37"
ENV_JENK="jenkins"
ENV_DEV="dev"
ENV_PROD="prod"
ENV_TEST="test"
ENV_NEXUS="nexus"
 
#Function Create Key SSH with exist check
aws_ssh_key_gen(){
	KEY=$1
	if aws ec2 wait key-pair-exists --key-names $KEY
		then
		echo "La clé $KEY existe déjà, on la supprime!"
		aws ec2 delete-key-pair --key-name $KEY
	fi
	 
	if test -f "./keys/$KEY.pem"
		then
		sudo rm -f ./keys/$KEY.pem
	fi
	 
	aws ec2 create-key-pair \
		--key-name $KEY \
		--query 'KeyMaterial' \
		--output text > $KEY.pem
	 
	echo " $KEY.pem Créée!"
	chmod 400 $KEY.pem

}
aws_ec2_status(){
	id=$1
	val=$(aws ec2 describe-instance-status --instance-id $id --output text --query 'InstanceStatuses[0].InstanceState.{Name:Name}')
	echo $val
}
aws_set_tcp(){
	GROUP=$1
	PORT=$2
	aws ec2 authorize-security-group-ingress \
		--group-id $GROUP \
		--protocol tcp \
		--port $PORT \
		--cidr 0.0.0.0/0
}

aws_create_EC2(){
	NAME=$KEY_NAME"_"$1
	if [ "$#" -eq 2 ]
	then
		File=$2
		ID=$(aws ec2 run-instances \
			--image-id $IMAGE_ID \
			--count 1 \
			--instance-type t2.medium \
			--key-name $NAME \
			--security-group-ids $GROUP_ID \
			--subnet-id $SUBNET_PUBLIC_ID \
			--user-data file://$File | sudo jq '.Instances[0].InstanceId' | sed -e 's/^"//' -e 's/"$//' )

	else
		ID=$(aws ec2 run-instances \
			--image-id $IMAGE_ID \
			--count 1 \
			--instance-type t2.medium \
			--key-name $NAME \
			--security-group-ids $GROUP_ID \
			--subnet-id $SUBNET_PUBLIC_ID | sudo jq '.Instances[0].InstanceId' | sed -e 's/^"//' -e 's/"$//' )
	fi
	aws ec2 create-tags --resources $ID --tags Key=Name,Value="GRP1_EC2_$1"
  echo $ID
}
# Creation VPC
echo "Creation VPC"
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block $VPC_CIDR \
  --query 'Vpc.{VpcId:VpcId}' \
  --output text )
echo "  VPC ID '$VPC_ID' CREATED in '$AWS_REGION' region."

# Creation d'un Nom de VPC
aws ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=$VPC_NAME

# Creation sous-réseau Public 
echo "Creation sous-réseau Public "
SUBNET_PUBLIC_ID=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block $SUBNET_PUBLIC_CIDR \
  --availability-zone $SUBNET_PUBLIC_AZ \
  --query 'Subnet.{SubnetId:SubnetId}' \
  --output text )
echo "  Subnet ID '$SUBNET_PUBLIC_ID' CREATED in '$SUBNET_PUBLIC_AZ'" \
  "Availability Zone."
 
aws ec2 create-tags --resources $SUBNET_PUBLIC_ID --tags Key=Name,Value="GRP1_Pub_SubNet"

# Create Private Subnet
echo "Creating Private Subnet..."
SUBNET_PRIVATE_ID=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block $SUBNET_PRIVATE_CIDR \
  --availability-zone $SUBNET_PRIVATE_AZ \
  --query 'Subnet.{SubnetId:SubnetId}' \
  --output text )
echo "  Subnet ID '$SUBNET_PRIVATE_ID' CREATED in '$SUBNET_PRIVATE_AZ'" \
  "Availability Zone."
  
aws ec2 create-tags --resources $SUBNET_PRIVATE_ID --tags Key=Name,Value="GRP1_Priv_SubNet"
 
# Create Internet gateway
echo "Creating Internet Gateway..."
IGW_ID=$(aws ec2 create-internet-gateway \
  --query 'InternetGateway.{InternetGatewayId:InternetGatewayId}' \
  --output text )
echo "  Internet Gateway ID '$IGW_ID' CREATED."
 
# Attach Internet gateway to your VPC
aws ec2 attach-internet-gateway \
  --vpc-id $VPC_ID \
  --internet-gateway-id $IGW_ID 
echo "  Internet Gateway ID '$IGW_ID' ATTACHED to VPC ID '$VPC_ID'."
 
# Create Route Table
echo "Creating Route Table..."
ROUTE_TABLE_ID=$(aws ec2 create-route-table \
  --vpc-id $VPC_ID \
  --query 'RouteTable.{RouteTableId:RouteTableId}' \
  --output text )
echo "  Route Table ID '$ROUTE_TABLE_ID' CREATED."
 
# Create route to Internet Gateway
RESULT=$(aws ec2 create-route \
  --route-table-id $ROUTE_TABLE_ID \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id $IGW_ID )
echo "  Route to '0.0.0.0/0' via Internet Gateway ID '$IGW_ID' ADDED to" \
  "Route Table ID '$ROUTE_TABLE_ID'."
 
# Associate Public Subnet with Route Table
RESULT=$(aws ec2 associate-route-table  \
  --subnet-id $SUBNET_PUBLIC_ID \
  --route-table-id $ROUTE_TABLE_ID )
echo "  Public Subnet ID '$SUBNET_PUBLIC_ID' ASSOCIATED with Route Table ID" \
  "'$ROUTE_TABLE_ID'."
 
# Enable Auto-assign Public IP on Public Subnet
aws ec2 modify-subnet-attribute \
  --subnet-id $SUBNET_PUBLIC_ID \
  --map-public-ip-on-launch 
 
echo " 'Auto-assign Public IP' ENABLED on Public Subnet ID" $SUBNET_PUBLIC_ID
 
# Creation clé SSH
aws_ssh_key_gen $KEY_NAME"_"$ENV_JENK
aws_ssh_key_gen $KEY_NAME"_"$ENV_DEV
aws_ssh_key_gen $KEY_NAME"_"$ENV_TEST
aws_ssh_key_gen $KEY_NAME"_"$ENV_PROD
aws_ssh_key_gen $KEY_NAME"_"$ENV_NEXUS
 
 
echo "Clés SSH crées et prêtes a être utilisées"
 
# Création du groupe de sécurité
GROUP_ID=$(aws ec2 create-security-group \
    --group-name SSHAccess \
    --query 'GroupId' \
    --description "Security group for SSH access" \
    --vpc-id $VPC_ID\
    --output text )
echo "Le groupe de sécurité a bien été créé avec l'id "$GROUP_ID
 
# Ajout des règles pour la connexion SSH
 
aws_set_tcp $GROUP_ID 22
aws_set_tcp $GROUP_ID 80
aws_set_tcp $GROUP_ID 8080
aws_set_tcp $GROUP_ID 8081
aws_set_tcp $GROUP_ID 5000
echo 'Les règles de sécurité ont été ajoutées'
 
# Lancer l'instance EC2

echo "Creation des Instances"
INSTANCE_ID_JENKINS=$(aws_create_EC2 $ENV_JENK install-jenkins-ansible.sh)
echo "L'instance $ENV_JENK est créée avec l'ID $INSTANCE_ID_JENKINS"
INSTANCE_ID_DEV=$(aws_create_EC2 "$ENV_DEV")
echo "L'instance $ENV_DEV est créée avec l'ID $INSTANCE_ID_DEV"
INSTANCE_ID_PROD=$(aws_create_EC2 $ENV_PROD)
echo "L'instance $ENV_PROD est créée avec l'ID $INSTANCE_ID_PROD"
INSTANCE_ID_TEST=$(aws_create_EC2 $ENV_TEST)
echo "L'instance $ENV_TEST est créée avec l'ID $INSTANCE_ID_TEST"
INSTANCE_ID_NEXUS=$(aws_create_EC2 $ENV_NEXUS install-nexus.sh)
echo "L'instance $ENV_NEXUS est créée avec l'ID $INSTANCE_ID_NEXUS"
 
#Allocation des IP Elastic
ELASTIC_IP_JENKINS=$(aws ec2 allocate-address | sudo jq '.PublicIp' | sed -e 's/^"//' -e 's/"$//')
ELASTIC_IP_PROD=$(aws ec2 allocate-address | sudo jq '.PublicIp' | sed -e 's/^"//' -e 's/"$//')
ELASTIC_IP_TEST=$(aws ec2 allocate-address | sudo jq '.PublicIp' | sed -e 's/^"//' -e 's/"$//')
ELASTIC_IP_DEV=$(aws ec2 allocate-address | sudo jq '.PublicIp' | sed -e 's/^"//' -e 's/"$//')
ELASTIC_IP_NEXUS=$(aws ec2 allocate-address | sudo jq '.PublicIp' | sed -e 's/^"//' -e 's/"$//')
