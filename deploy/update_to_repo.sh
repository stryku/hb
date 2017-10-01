#!/bin/bash

REPO_URL='https://github.com/stryku/hb'
DEPLOY_DIR=`pwd`
BACKUP_DIR=$DEPLOY_DIR/..

echo '[UPDATE TO REPO START]'

echo '[BACKUP]'
./backup.sh $DEPLOY_DIR $BACKUP_DIR

echo '[CLONE REPO]'
REPO_DIR=$(mktemp -d)
cd $REPO_DIR
git clone $REPO_URL

echo '[DEPLOY]'
$REPO_DIR/hb/deploy/deploy.sh $DEPLOY_DIR

echo '[RM REPO DIRECTORY]'
rm -rf $REPO_DIR

echo '[UPDATE TO REPO END]'
