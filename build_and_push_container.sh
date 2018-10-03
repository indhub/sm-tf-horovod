#!/usr/bin/env bash
set -e

# Build the Python modules and move them to docker directory
python3 setup.py bdist_wheel
rm -rf docker/dist/
mv dist docker/
cd docker

# Build the Docker container
container_name='sm-tf-horovod'
docker build -t ${container_name} -f Dockerfile.gpu .

# Collect information needed to push the container
region=$(aws configure get region)
region=${region:-us-east-1} #default is not configured

account=$(aws sts get-caller-identity --query Account --output text)
if [ $? -ne 0 ]
then
    exit 255
fi

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${container_name}" > /dev/null 2>&1
if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${container_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
$(aws ecr get-login --region ${region} --no-include-email)

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${container_name}:latest"
docker tag ${container_name} ${fullname}
docker push ${fullname}

