import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Move Html files to and from a django project. '
                                             'HTML directory names need to match the name that the django project '
                                             'directories. If no argument is passed to -local , '
                                             f'the program will assume that the html directories are in '
                                             f'{os.getcwd()}/html.')
parser.add_argument('--project_path', type=str, help='The path to the Django project. REQUIRED')
parser.add_argument('--project_name', type=str,
                    help='The name of the django project. REQUIRED')
parser.add_argument('--operation', type=str, help='The operation to do. Supported: move_to, move_from. REQUIRED')
parser.add_argument('--local', type=str, help='Name of the local directory containing html files. OPTIONAL')


args = parser.parse_args()

# Django path setup
project_name = args.project_name
path_of_django_project = args.project_path
full_path = f"{path_of_django_project}/{project_name}"

if not os.path.exists(full_path):
    print("Path to django project does not exist!")
    exit(1)

tmpl = "templates"

# Local path setup
base_local_dir_name = "html"
if args.local is not None:
    base_local_dir_name = args.local
local_path = f"{os.getcwd()}/{base_local_dir_name}"

if not os.path.exists(local_path):
    create_path = input("Path to local html files does not exist! Do you want to create it? (y/n) ")

    if create_path[0].lower() == "y":
        os.makedirs(local_path)
    else:
        print("Aborting")
        exit(1)

# Operations, finally!
choice = input("No path errors could be found. The next steps will overwrite all files in the destination "
               "directories. Double-check your operation before continuing. Do you want to continue? (y/n) ")

if choice[0].lower() == "y":
    operation = args.operation
    if operation == "move_to":
        print("Moving files to django project...")
        for directory in os.listdir("html/"):
            dstpath = f"{full_path}/{directory}/{tmpl}"
            if os.path.exists(dstpath):
                shutil.copytree(f"{local_path}/{directory}", dstpath, dirs_exist_ok=True)
        print("Finished moving files to project, quitting.")
    elif operation == "move_from":
        print("Moving files from django project...")
        for directory in os.listdir(full_path):
            srcpath = f"{full_path}/{directory}/{tmpl}/"
            if os.path.exists(srcpath):
                new_dir = f"{local_path}/{directory}"
                os.makedirs(new_dir)
                shutil.copytree(srcpath, new_dir, dirs_exist_ok=True)
        print("Finished moving files from project, quitting.")
    else:
        print("Operation not understood. Quitting...")
else:
    print("Operation aborted.")