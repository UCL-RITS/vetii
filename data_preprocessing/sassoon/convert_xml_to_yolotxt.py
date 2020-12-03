import os
import xml.etree.ElementTree as ET
from tqdm import tqdm as progress_bar


def yolo_conversion(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_xml_annotation_to_yolo(label_path, output_path, is_masati, classes):
    basename = os.path.basename(label_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(label_path)
    out_file = open(os.path.join(output_path, basename_no_ext + ".txt"), "w")
    tree = ET.parse(in_file)
    root = tree.getroot()
    if is_masati:
        size = None
        width = 512.0
        height = 512.0
    else:
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)

    for obj in root.iter("object"):
        difficult = obj.find("difficult").text
        if is_masati:
            class_id = 0
        else:
            cls = obj.find("name").text
            if cls not in classes or int(difficult) == 1:
                continue
            class_id = classes.index(cls)

        xmlbox = obj.find("bndbox")
        boundaries = (
            float(xmlbox.find("xmin").text),
            float(xmlbox.find("xmax").text),
            float(xmlbox.find("ymin").text),
            float(xmlbox.find("ymax").text),
        )
        bounding_box = yolo_conversion((width, height), boundaries)
        out_file.write(
            str(class_id) + " " + " ".join([str(a) for a in bounding_box]) + "\n"
        )


def main():

    labels_dir = os.path.join(os.getcwd(), "xml_annotations")
    classes = ["boat"]

    output_path = os.path.join(os.getcwd(), "yolo_annotations")

    is_masati = False
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for label in progress_bar(os.listdir(labels_dir)):
        convert_xml_annotation_to_yolo(
            os.path.join(labels_dir, label), output_path, is_masati, classes
        )


if __name__ == "__main__":
    main()
