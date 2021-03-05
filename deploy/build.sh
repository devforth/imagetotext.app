#!/bin/bash

branch=$(git branch | grep \* | cut -d ' ' -f2)
branch=`echo $branch | sed 's/feature\///g'`
echo "Building branch $branch"

if [ -z "$VAULT_MASTER_SSH_PRIV_KEY" ]; then
    echo "Running not on Drone (localy)"
else
    mkdir -p ~/.ssh/
    echo "$VAULT_MASTER_SSH_PRIV_KEY" > ~/.ssh/id_rsa
    echo "$VAULT_MASTER_SSH_PUB_KEY" > ~/.ssh/id_rsa.pub
    chmod 600 ~/.ssh/id_rsa
    chmod 644 ~/.ssh/id_rsa.pub
    eval `ssh-agent -s`
    ssh-add ~/.ssh/id_rsa
    echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
fi

    
if [ "$branch" = "master" ]; then
  HOST_DOMAIN=51.158.76.244
  # add more environemnts for branches here, e.g.:
  # elif [ "$branch" = "develop" ]; then
else
  echo "No configuration for branch $branch"
  exit -1
fi

export DOCKER_HOST=ssh://root@$HOST_DOMAIN   

# cleanup cache from previous builds
docker builder prune -a -f
docker container prune -f
docker rmi $(docker images -f "dangling=true" -q) || true

docker-compose -p stack-itt-$branch -f docker-compose.yml up -d --build --remove-orphans 
