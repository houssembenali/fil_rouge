#!/usr/bin/env bash

STACK_NAME="groupe4-stack"
INSTANCE_TYPE="t2.micro"
#DIR="/home/ec2-user/fil-rouge-cloud-formation"
AWS_REGION="eu-west-3"
KEY_NAME="groupe4-key-pair"
TYPE_CLOUD_FORMATION=""

# Création de l'instance EC2
if aws ec2 wait key-pair-exists --key-names $KEY_NAME
    then
    echo 'La clé existe déjà, on la supprime'
    aws ec2 delete-key-pair --key-name $KEY_NAME
fi

if [ $KEY_NAME.pem ]
    then
    echo 'La clé existe déjà en local, on la supprime'
    #rm $KEY_NAME.pem
fi

# Création d'une paire clé SSH
echo "Création d'une paire clé SSH..."
aws ec2 create-key-pair \
    --key-name $KEY_NAME \
    --query 'KeyMaterial' \
    --output text > $KEY_NAME.pem #> ~/.ssh/$KEY_NAME.pem

#echo "Describe key pairs ..."
#aws ec2 describe-key-pairs 
#    --key-name $KEY_NAME

# Définition des bons droits sur la clé SSH
echo " La clé $KEY_NAME.pem à été Créée!"
chmod 400 $KEY_NAME.pem
#chmod 400 ~/.ssh/$KEY_NAME.pem

# echo "Checking if stack exists ..."
# if ! aws cloudformation describe-stacks --region $AWS_REGION --stack-name $STACK_NAME ; then
#     echo -e "Stack $STACK_NAME does not exist...Creating"
#     TYPE_CLOUD_FORMATION='create-stack'
# else
#     echo -e "Stack $STACK_NAME exist, update $STACK_NAME"
#     TYPE_CLOUD_FORMATION='update-stack'
# fi

 --key-name $KEY_NAME \

echo "Creating and actualization stack..."
STACK_ID=$(aws cloudformation  create-stack  \
        --region $AWS_REGION  \
        --stack-name $STACK_NAME  \
        --parameters ParameterKey=KeyName,ParameterValue=$KEY_NAME \
        --template-body file://create-update-stack.yml \
)

echo "Waiting on ${STACK_NAME} create completion..."
aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}

echo "Describe stacks ..."
aws --region $api_region cloudformation describe-stacks --stack-name $STACK_NAME

#aws cloudformation create-stack --stack-name myteststack --template-body file://sampletemplate.json 
#--parameters ParameterKey=KeyPairName,ParameterValue=TestKey ParameterKey=SubnetIDs,ParameterValue=SubnetID1




# aws cloudformation create-stack --region eu-west-3 --stack-name filrougestackgroupe4 --template-url https://groupe-4-fil-rouge.s3.eu-west-3.amazonaws.com/create-update-stack.yml

# aws cloudformation create-stack --region eu-west-3 --stack-name groupe4-test-1 --template-url https://groupe-4-fil-rouge.s3.eu-west-3.amazonaws.com/create-bucket.yml

# aws cloudformation create-stack --region eu-west-3 --stack-name groupe4-test-2 --template-url https://groupe-4-fil-rouge.s3.eu-west-3.amazonaws.com/create-vpc.yml

# aws cloudformation create-stack --region eu-west-3 --stack-name groupe4ec2 --template-url https://groupe-4-fil-rouge.s3.eu-west-3.amazonaws.com/create-ec2.yml

# aws cloudformation create-stack --stack-name G4-web-server --template-url https://groupe-4-fil-rouge.s3.eu-west-3.amazonaws.com/G4-ec2.yml --parameters ParameterKey=InstanceType,ParameterValue=t2.micro ParameterKey=KeyName,ParameterValue=subnet-019844b586b3a73ed ParameterKey=VpcId,ParameterValue=vpc-0abd3e892b3173fef --tags Key=Name,Value="G4WebServer"


#aws cloudformation wait stack-exists \
#    --stack-name $STACK_NAME

# Création de l'instance EC2
# if aws ec2 wait key-pair-exists --key-names $KEY_NAME
#     then
#     echo 'La clé existe déjà, on la supprime'
#     aws ec2 delete-key-pair --key-name $KEY_NAME
# fi

# if [ -f ~/.ssh/$KEY_NAME.pem ]
#     then
#     echo 'La clé existe déjà en local, on la supprime'
#     sudo rm -f ~/.ssh/$KEY_NAME.pem
# fi