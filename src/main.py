import os
import shutil

def clean_dir(dir):
    path = f"{os.getcwd()}/"+ dir
    print(f"Clearing: {path}...")
    shutil.rmtree(path, True)
    os.mkdir(path)

def copy_files(src, dest):
    items = os.listdir(src)
    
    for item in items:
        src_path = f"{src}/{item}"
        dest_path = f"{dest}/{item}"
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"{src_path}...")
        else:
            os.mkdir(dest_path)
            copy_files(src_path, dest_path)


def copy_content(src, dest):
    src_path = f"{os.getcwd()}/"+ src
    dest_path = f"{os.getcwd()}/"+ dest
    print(f"Copying content: {src_path} to {dest_path}...")
    copy_files(src_path, dest_path)


def main():
    clean_dir("public")
    copy_content("static", "public")

main()
