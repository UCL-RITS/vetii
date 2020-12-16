import os
import xml.etree.ElementTree as ET
from tqdm import tqdm as progress_bar


def set_single_class(label_path, output_path, is_masati, classes):
    basename = os.path.basename(label_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(label_path)
    out_file = os.path.join(output_path, basename_no_ext + ".xml")
    tree = ET.parse(in_file)
    root = tree.getroot()

    size = root.find("size")
    width = "512"
    height = "512"
    root.find("size/width").text = width
    root.find("size/height").text = height

    for obj in root.iter("object"):
        obj.find("name").text = "boat"

    tree.write(out_file)


def main():

    labels_dir = os.path.join(os.getcwd(), "xml_annotations")
    classes = ["boat"]

    output_path = os.path.join(os.getcwd(), "modified_xml_annotations")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for label in progress_bar(os.listdir(labels_dir)):
        set_single_class(os.path.join(labels_dir, label), output_path, True, classes)


if __name__ == "__main__":
    main()
