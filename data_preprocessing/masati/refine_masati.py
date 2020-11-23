import os
import pandas as pd
from tqdm import tqdm


def create_directory_structure(masati_directories, debug=False):
    for new_dir in masati_directories:
        if not os.path.exists(os.path.join(os.getcwd(), new_dir)):
            os.mkdir(os.path.join(os.getcwd(), new_dir))

    print("Finding MASATI image directories...")
    directories = []
    for fpath in os.listdir(os.path.join(os.getcwd(), "MASATI-v2")):
        if os.path.isdir(os.path.join(os.getcwd(), "MASATI-v2", fpath)):
            directories.append(os.path.join(os.getcwd(), "MASATI-v2", fpath))

    print("Getting XML files...")
    label_paths = []
    for test_dir in directories:
        label_paths += [
            os.path.join(test_dir, test_file)
            for test_file in os.listdir(test_dir)
            if "xml" in test_file
        ]

    print("Moving XML files...")
    img_paths = []
    new_xml_paths = []
    for xml_file in tqdm(label_paths):
        img_paths.append(xml_file.replace("_labels", "").replace("xml", "png"))
        filename = xml_file.rsplit("/", 1)[-1]
        new_xml_path = os.path.join(os.getcwd(), masati_directories[0], filename)
        if debug:
            print(f"os.rename({xml_file}, {new_xml_path})")
        new_xml_paths.append(new_xml_path)
        os.rename(xml_file, new_xml_path)

    print("Moving image files...")
    new_img_paths = []
    for img_file in tqdm(img_paths):
        filename = img_file.rsplit("/", 1)[-1]
        new_img_path = os.path.join(os.getcwd(), masati_directories[-1], filename)
        if debug:
            print(f"os.rename({img_file}, {new_img_path})")
        new_img_paths.append(new_img_path)
        os.rename(img_file, new_img_path)

    new_paths = list(zip(new_img_paths, new_xml_paths))
    # Renaming all our files to integers
    filecounter = 1
    label_map = []
    for imgpath, labelpath in new_paths:
        img_base_name = imgpath.split(".")[0].rsplit("/", 1)[-1]
        label_base_name = labelpath.split(".")[0].rsplit("/", 1)[-1]

        # Check that each image file and label file have the same base name (without extension)
        assert img_base_name == label_base_name
        # Masati has 2368 files of interest, so only pad string with zeros until it's 4 digits long
        new_base_name = str(filecounter).zfill(4)
        new_img_path = os.path.join(imgpath.rsplit("/", 1)[0], new_base_name + ".png")
        new_label_path = os.path.join(
            labelpath.rsplit("/", 1)[0], new_base_name + ".xml"
        )

        label_map.append(
            {
                "original_img_name": imgpath.rsplit("/", 1)[-1],
                "original_label_name": labelpath.rsplit("/", 1)[-1],
                "new_img_name": new_base_name + ".png",
                "new_label_name": new_base_name + ".xml",
            }
        )
        # file moving...
        os.rename(imgpath, new_img_path)
        os.rename(labelpath, new_label_path)
        filecounter += 1

    filename_map = pd.DataFrame(label_map)
    filename_map.to_csv("filename_mapping.csv", index=False, sep="\t")

    return


def main():
    masati_directories = ["xml_annotations", "PNGImages"]
    create_directory_structure(masati_directories)


if __name__ == "__main__":
    main()
