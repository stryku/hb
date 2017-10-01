#!/bin/bash

REPO_URL='https://github.com/stryku/hb'
DEPLOY_DIR=`pwd`

cd $(mktemp -d)
git clone $REPO_URL
cd hb/deploy
./deploy.sh $DEPLOY_DIR
rm `pwd`

