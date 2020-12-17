import os
import shutil
from tqdm import tqdm as progress_bar


"""Rough script for sorting yolo annotations and images files 
for use with YOLOv3/v5
"""


def create_yolo_dirs(workdir, imgdir, labeldir):

    output_labels_dir = os.path.join(workdir, "yolo_labels_" + imgdir)
    output_images_dir = output_labels_dir.replace("labels", "images")

    if os.path.exists(output_images_dir) and os.path.exists(output_labels_dir):
        return output_images_dir, output_labels_dir

    if not os.path.exists(output_labels_dir):
        os.mkdir(output_labels_dir)

    if not os.path.exists(output_images_dir):
        os.mkdir(output_images_dir)

    label_list = os.listdir(os.path.join(workdir,labeldir))
    for imgfile in progress_bar(os.listdir(os.path.join(workdir, imgdir))):
        basefile = imgfile.split(".", 1)[0]
        if basefile + ".txt" in label_list:
            shutil.copyfile(
                os.path.join(workdir, imgdir, imgfile),
                os.path.join(output_images_dir, imgfile),
            )
            shutil.copyfile(
                os.path.join(workdir, labeldir, basefile + ".txt"),
                os.path.join(output_labels_dir, basefile + ".txt"),
            )
    return output_images_dir, output_labels_dir


def rename_yolo_files(workdir, label_dir, imgformat):
    labels_path = os.path.join(workdir, label_dir)
    counter = 1
    for thisfile in progress_bar(os.listdir(labels_path)):

        old_label_path = os.path.join(labels_path, thisfile)
        old_image_path = old_label_path.replace("labels", "images").replace(
            ".txt", "."+imgformat
        )
        new_label_name = str(counter).zfill(5)
        new_label_path = os.path.join(labels_path, new_label_name + ".txt")
        images_dir = old_image_path.rsplit("/", 1)[0]
        new_image_name = os.path.join(images_dir, new_label_name + ".jpg")
        counter += 1
        os.replace(old_label_path, new_label_path)
        os.replace(old_image_path, new_image_name)


def main():
    from read_params import read_parameter_file
    yolo_annotations_dir = "yolo_annotations"
    workdir = os.getcwd()
    params = read_parameter_file("params.yaml")
    imgformat = params["sort_yolo_images"]["imgformat"]
    for imgdir in ["train", "validation"]:
        _, new_label_dir = create_yolo_dirs(workdir, imgdir, yolo_annotations_dir)
        rename_yolo_files(workdir, new_label_dir, imgformat)


if __name__ == "__main__":
    main()
