import os
from tqdm import tqdm

def create_directory_structure(masati_directories, debug=False):
    for new_dir in masati_directories:
        if not os.path.exists(os.path.join(os.getcwd(),new_dir)):
            os.mkdir(os.path.join(os.getcwd(),new_dir))

    print("Finding MASATI image directories...")
    directories = []
    for fpath in os.listdir(os.path.join(os.getcwd(),"MASATI-v2")):
        if os.path.isdir(os.path.join(os.getcwd(),"MASATI-v2",fpath)):
            directories.append(os.path.join(os.getcwd(),"MASATI-v2",fpath))

    print("Getting XML files...")
    label_paths = []
    for test_dir in directories:
        label_paths+=[os.path.join(test_dir,test_file) for test_file in os.listdir(test_dir) if 'xml' in test_file]

    print("Moving XML files...")
    img_paths = []
    for xml_file in tqdm(label_paths):
        img_paths.append(xml_file.replace("_labels","").replace("xml","png"))
        filename = xml_file.rsplit('/',1)[-1]
        new_xml_path = os.path.join(os.getcwd(), masati_directories[0],filename)
        if debug:
            print(f"os.rename({xml_file}, {new_xml_path})")
        os.rename(xml_file, new_xml_path)
            
    print("Moving image files...")
    for img_file in tqdm(img_paths):
        filename = img_file.rsplit('/',1)[-1]
        new_img_path = os.path.join(os.getcwd(), masati_directories[-1],filename)
        if debug:
            print(f"os.rename({img_file}, {new_img_path})") # make this actually happen when it comes to it...
        os.rename(img_file, new_img_path)
        
    return


def main():
    masati_directories = ["xml_annotations", "PNGImages"]
    create_directory_structure(masati_directories)
        
        
if __name__ == "__main__":
    main()

