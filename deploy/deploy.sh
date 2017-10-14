#!/bin/bash

DEPLOY_DIR=$1
CLIENT_SERVER_DIR=$2
SCRIPTS_DIR=$DEPLOY_DIR/scripts
DB_DIR=$DEPLOY_DIR/db
SAVED_IMAGES_DIR=$DEPLOY_DIR/data/received_images

echo '[CURRENT DIR]'
echo "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo '[ARGUMENTS]'
echo $@
echo

mkdir $SCRIPTS_DIR
mkdir $DB_DIR
mkdir -p $SAVED_IMAGES_DIR

yes | cp -rfi ../image_processing/preprocess/run_cleaner.sh $SCRIPTS_DIR/run_cleaner.sh > /dev/null
yes | cp -rfi ../image_processing/tesseract/run_tesseract.sh $SCRIPTS_DIR/run_tesseract.sh > /dev/null
yes | cp -rfi ../image_processing/tesseract/tessdata $DEPLOY_DIR/tessdata > /dev/null
yes | cp -rfi update_to_repo.sh $DEPLOY_DIR > /dev/null
yes | cp -rfi backup.sh $DEPLOY_DIR > /dev/null


if [$CLIENT_SERVER_DIR == '']
then
    echo '[CLIENT_SERVER_DIR empty, assigning ../client_server]'
    $CLIENT_SERVER_DIR='../client_server/'
fi


RSYNC_FROM=$CLIENT_SERVER_DIR
RSYNC_TO=$DEPLOY_DIR

echo
echo
echo '[rsync]'
PWD=`pwd`
echo `realpath $RSYNC_FROM`
echo `realpath $RSYNC_TO`
echo

rsync -avm --include='*.py' -f 'hide,! */' $RSYNC_FROM $RSYNC_TO


