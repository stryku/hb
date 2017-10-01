#!/bin/bash
#Credits: http://broexperts.com/how-to-backup-files-and-directories-in-linux-using-tar-cron-jobs/
#Purpose = Backup of Important Data
#Created on 17-1-2012
#Author = Hafiz Haider
#Version 1.0
#START
TIME=`date +%b-%d-%y`            # This Command will add date in Backup File Name.
FILENAME=backup-$TIME.tar.gz    # Here i define Backup file name format.
SRCDIR=$1                    # Location of Important Data Directory (Source of backup).
DESDIR=$2            # Destination of backup file.
tar -cpzf $DESDIR/$FILENAME $SRCDIR
#END