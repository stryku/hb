#!/bin/bash

tesseract -l hb --tessdata-dir . $1 stdout
