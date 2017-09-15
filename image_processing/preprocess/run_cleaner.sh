#!/bin/bash


if hash textcleaner 2>/dev/null; then
        textcleaner -g -e stretch -f 25 -o 20 -t 30 -s 1 -T $1 $2
else
    echo "textcleaner not found. Download and instal it from here: http://www.fmwconcepts.com/imagemagick/textcleaner/index.php"
fi

