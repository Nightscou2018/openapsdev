#!/usr/bin/python3
# check if no loop-successful file exists in this directory or if the time since it was touched is 
# too long.  If either is true, double-check that there is actually an internet connection.
# If so, then zip backup the openaps directory, remove it,  clone git, and set the loop_successful file

import subprocess
import os

# -----------------------------------------------------------------------------
# INPUTS
TIME_THRESHOLD_MINUTES = 20
HOSTNAME = "www.google.com"

#-----------------------------------------------------------------------------

def check_for_time_modified_loop_successful_file(TIME_THRESHOLD_MINUTES):
    try:  # if there is a loop_successful file
        last_touched_in_secs_since_epoch = subprocess.Popen(["stat","-c","%Y","loop_successful"], stdout=subprocess.PIPE).communicate()[0]
        now_in_secs_since_epoch = subprocess.Popen(["date","+%s"], stdout=subprocess.PIPE).communicate()[0]
        elapsed_secs = int(now_in_secs_since_epoch) - int(last_touched_in_secs_since_epoch)
    except:
        elapsed_secs = 9999
    print('elapsed_secs =',elapsed_secs)

    # if so, see how much time has elapsed since last SMS sent
    if elapsed_secs >= (TIME_THRESHOLD_MINUTES*60):
        response = os.system("ping -c 1 " + HOSTNAME)
        if response == 0:
            print('shit is screwed, delete the directory, pull from git and start over')
            backup_existing_directory()
            remove_and_replace_openaps_directory()
            subprocess.Popen('cd /home/pi/Scripts/; ./set_loop_successful.py', stdout=subprocess.PIPE,shell=True).communicate()[0]
        else:
            print('wifi connection must be down, do not reset git')
    else:
        print('loop_successful file says things must be running fine')


def backup_existing_directory():
# subprocess.Popen('cd /home/pi/; cp -r openapsdev/ BACKUP"$(date +"%Y%m%d-%H%M%S")"/', stdout=subprocess.PIPE,shell=True).communicate()[0]
# replaced with tar zip, command from here: http://unix.stackexchange.com/questions/93139/can-i-zip-an-entire-folder-using-gzip 
    subprocess.Popen('cd /home/pi/; tar -zcf BACKUP"$(date +"%Y%m%d-%H%M%S")".tar.gz openapsdev/', stdout=subprocess.PIPE,shell=True).communicate()[0]


def remove_and_replace_openaps_directory():
    subprocess.Popen('cd /home/pi/; rm -rf openapsdev/', stdout=subprocess.PIPE,shell=True).communicate()[0]
    subprocess.Popen('cd /home/pi/; git clone https://github.com/mikestebbins/openapsdev.git;cd /home/pi/openapsdev/; git remote set-url origin https://github.com/mikestebbins/openapsdev.git; git pull', stdout=subprocess.PIPE,shell=True).communicate()[0]


check_for_time_modified_loop_successful_file(TIME_THRESHOLD_MINUTES)
