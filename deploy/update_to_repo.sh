#!/bin/bash

REPO_URL='https://github.com/stryku/hb'
DEPLOY_DIR=`pwd`
BACKUP_DIR=$DEPLOY_DIR/..

BRANCH=$1

echo '[UPDATE TO REPO START]'

echo '[BACKUP]'
./backup.sh $DEPLOY_DIR $BACKUP_DIR

echo '[CLONE REPO]'
REPO_DIR=$(mktemp -d)
cd $REPO_DIR
git clone $REPO_URL

if [ -z ${1+x} ]
then
    echo '[GIT] branch not set. No checkout.'
else
    echo '[GIT] checking out to '$1
    cd hb
    git checkout $1
    cd ..
fi


CLIENT_SERVER_DIR=$REPO_DIR/hb/client_server

echo '[DEPLOY]'
cd $REPO_DIR/hb/deploy/
./deploy.sh $DEPLOY_DIR $CLIENT_SERVER_DIR

echo '[RM REPO DIRECTORY]'
rm -rf $REPO_DIR

echo '[UPDATE TO REPO END]'
