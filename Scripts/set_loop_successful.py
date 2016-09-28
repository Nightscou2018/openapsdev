#!/usr/bin/python3
# After every successful loop run, touch a file to update the date

import subprocess

def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

def touch_file():
    try:
        output = bash_command('rm loop_successful')      
        output = bash_command('touch -a loop_successful')
        print('removed and replaced loop_successful file')
    except:
        output = bash_command('touch -a loop_successful')
        print('created loop_successful file')

touch_file()

