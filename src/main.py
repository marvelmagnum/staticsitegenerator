import os
import shutil
import blockutils
from htmlnode import HTMLNode

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

def generate_pages(from_path, template_path, dest_path):
    items = os.listdir(from_path)

    for item in items:
        src_path = f"{from_path}/{item}"
        if os.path.isfile(src_path):
            filename_parts = item.split('.')
            name_parts = len(filename_parts)
            if name_parts >= 2:
                if filename_parts[name_parts-1] == "md":
                    filename = '.'.join(filename_parts[:-1])
                    md_path = f"{from_path}/{filename}.md"
                    page_path = f"{dest_path}/{filename}.html"
                    generate_page(md_path, template_path, page_path)
        else:
            target_path = f"{dest_path}/{item}"
            os.mkdir(target_path)
            generate_pages(src_path, template_path, target_path)



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path, "r")
    markdown = md_file.read()
    md_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    html_content = blockutils.markdown_to_html_node(markdown).to_html()
    title = blockutils.extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    page_file = open(dest_path, "w")
    page_file.write(template)
    page_file.close()


def main():
    clean_dir("public")
    copy_content("static", "public")

    md_path = f"{os.getcwd()}/content"
    tem_path = f"{os.getcwd()}/template.html"
    page_path = f"{os.getcwd()}/public"
    generate_pages(md_path, tem_path, page_path)


main()
