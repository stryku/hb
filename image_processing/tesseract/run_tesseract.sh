#!/bin/bash

(export TESSDATA_PREFIX=..; tesseract -l hb $1 stdout)

