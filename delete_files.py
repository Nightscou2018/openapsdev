#!/usr/bin/python3

import os

def delete_files_from_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception:
            print (Exception)
            
delete_files_from_folder('enact/')
delete_files_from_folder('suggest/')
