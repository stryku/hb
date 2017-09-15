#!/bin/bash

DEPLOY_DIR=$1
SCRIPTS_DIR=$DEPLOY_DIR/scripts

mkdir $SCRIPTS_DIR
cp ../image_processing/preprocess/run_cleaner.sh $SCRIPTS_DIR/run_cleaner.sh
cp ../image_processing/preprocess/textcleaner $SCRIPTS_DIR/textcleaner
cp ../image_processing/tesseract/run_tesseract.sh $SCRIPTS_DIR/run_tesseract.sh
cp -r ../image_processing/tesseract/tessdata $DEPLOY_DIR/tessdata

cp ../client_server/*.py $DEPLOY_DIR/


