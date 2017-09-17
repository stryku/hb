#!/bin/bash

rm -r $1/build
mkdir -p $1/build
cd $1/build

python $1/trainer.py
