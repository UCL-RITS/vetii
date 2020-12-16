import os
import shutil
from tqdm import tqdm as progress_bar

"""Rough script for sorting yolo annotations and images files 
for use with YOLOv3/v5
"""


def create_yolo_dirs(imgdir, labeldir):

    output_labels_dir = os.path.join(os.getcwd(), "yolo_labels_" + imgdir)
    output_images_dir = output_labels_dir.replace("labels", "images")

    if os.path.exists(output_images_dir) and os.path.exists(output_labels_dir):
        return output_images_dir, output_labels_dir

    if not os.path.exists(output_labels_dir):
        os.mkdir(output_labels_dir)

    if not os.path.exists(output_images_dir):
        os.mkdir(output_images_dir)

    label_list = os.listdir(labeldir)
    for imgfile in progress_bar(os.listdir(imgdir)):
        basefile = imgfile.split(".", 1)[0]
        if basefile + ".txt" in label_list:
            shutil.copyfile(
                os.path.join(os.getcwd(), imgdir, imgfile),
                os.path.join(output_images_dir, imgfile),
            )
            shutil.copyfile(
                os.path.join(os.getcwd(), labeldir, basefile + ".txt"),
                os.path.join(output_labels_dir, basefile + ".txt"),
            )
    return output_images_dir, output_labels_dir


def rename_yolo_files(label_dir):
    labels_path = os.path.join(os.getcwd(), label_dir)
    counter = 1
    for thisfile in progress_bar(os.listdir(labels_path)):

        old_label_path = os.path.join(labels_path, thisfile)
        old_image_path = old_label_path.replace("labels", "images").replace(
            ".txt", ".png"
        )
        new_label_name = str(counter).zfill(5)
        new_label_path = os.path.join(labels_path, new_label_name + ".txt")
        images_dir = old_image_path.rsplit("/", 1)[0]
        new_image_name = os.path.join(images_dir, new_label_name + ".png")
        counter += 1
        os.replace(old_label_path, new_label_path)
        os.replace(old_image_path, new_image_name)


def main():
    yolo_annotations_dir = "yolo_annotations"
    for imgdir in ["train", "validation"]:
        _, new_label_dir = create_yolo_dirs(imgdir, yolo_annotations_dir)
        rename_yolo_files(new_label_dir)


if __name__ == "__main__":
    main()
