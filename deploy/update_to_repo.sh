#!/bin/bash

REPO_URL='https://github.com/stryku/hb'
DEPLOY_DIR=`pwd`
BACKUP_DIR=$DEPLOY_DIR/..

./backup $DEPLOY_DIR $BACKUP_DIR

cd $(mktemp -d)
git clone $REPO_URL
cd hb/deploy
./deploy.sh $DEPLOY_DIR
rm `pwd`

