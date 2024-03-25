# import subprocess

# def launch_app(path_of_app):
#     try:
#         subprocess.call([path_of_app])
#         return True
#     except Exception as e:
#         print(e)
#         return False

import os
import subprocess

def launch_app(path_of_app):
    try:
        # Check if the file exists
        if os.path.exists(path_of_app):
            subprocess.run([path_of_app], check=True)
            return True
        else:
            print(f"Error: File not found at path {path_of_app}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
