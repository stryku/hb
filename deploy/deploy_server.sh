#!/bin/bash

DEPLOY_DIR=$1
SCRIPTS_DIR=$DEPLOY_DIR/scripts
DB_DIR=$DEPLOY_DIR/db
SAVED_IMAGES_DIR=$DEPLOY_DIR/data/received_images

mkdir $SCRIPTS_DIR
mkdir $DB_DIR
mkdir -p $SAVED_IMAGES_DIR

cp ../image_processing/preprocess/run_cleaner.sh $SCRIPTS_DIR/run_cleaner.sh
cp ../image_processing/tesseract/run_tesseract.sh $SCRIPTS_DIR/run_tesseract.sh
cp -r ../image_processing/tesseract/tessdata $DEPLOY_DIR/tessdata

rsync -avm --include='*.py' -f 'hide,! */' ../client_server/ $DEPLOY_DIR


