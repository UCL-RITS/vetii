import os
import shutil
from tqdm import tqdm as progress_bar
from pathlib import Path

"""
Sorts yolo image and label directories into the file structure YOLOv5 expects
"""


def create_yolo_dirs(
    train_label_dir, val_label_dir, train_img_dir, val_img_dir, target_directory
):

    output_images_dir = os.path.join(target_directory, "images")
    output_labels_dir = output_images_dir.replace("images", "labels")

    # Make these directories if they don't exist
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    if not os.path.exists(output_labels_dir):
        os.mkdir(output_labels_dir)

    if not os.path.exists(output_images_dir):
        os.mkdir(output_images_dir)

    output_train_label_dir = os.path.join(output_labels_dir, "train")
    output_validation_label_dir = os.path.join(output_labels_dir, "val")
    output_train_img_dir = os.path.join(output_images_dir, "train")
    output_validation_image_dir = os.path.join(output_images_dir, "val")
    os.rename(train_label_dir, output_train_label_dir)
    os.rename(val_label_dir, output_validation_label_dir)
    os.rename(train_img_dir, output_train_img_dir)
    os.rename(val_img_dir, output_validation_image_dir)

    return [
        output_train_label_dir,
        output_validation_label_dir,
        output_train_img_dir,
        output_validation_image_dir,
    ]


def main():
    from read_params import read_parameter_file

    params = read_parameter_file("params.yaml")
    workdir = os.getcwd()
    train_label_dir = os.path.join(
        workdir, params["create_yolov5_filestructure"]["train_labels"]
    )
    val_label_dir = os.path.join(
        workdir, params["create_yolov5_filestructure"]["val_labels"]
    )
    train_img_dir = os.path.join(
        workdir, params["create_yolov5_filestructure"]["train_imgs"]
    )
    val_img_dir = os.path.join(
        workdir, params["create_yolov5_filestructure"]["val_imgs"]
    )
    dataset = params["create_yolov5_filestructure"]["dataset"]

    # Check that directories exist before we move anything...
    try:
        assert os.path.isdir(train_label_dir)
        assert os.path.isdir(val_label_dir)
        assert os.path.isdir(train_img_dir)
        assert os.path.isdir(val_img_dir)
    except AssertionError:
        "Check that the yolo train/val label and image directories exist in this directory!"

    assert os.path.isdir(
        "../../data_preprocessing"
    ), "Run this script from a subdirectory of data_preprocessing"

    vetii_directory = str(Path(workdir).parent.parent)
    data_directory = os.path.join(vetii_directory, "data")

    assert os.path.isdir(
        data_directory
    ), "data/ directory does not exist at the top level of this project. Create this directory before running!"

    target_directory = os.path.join(data_directory, dataset)
    print(target_directory)
    output_dirs = create_yolo_dirs(
        train_label_dir, val_label_dir, train_img_dir, val_img_dir, target_directory
    )

    for outdir in output_dirs:
        assert os.path.isdir(outdir), "{} was not found".format(outdir)


if __name__ == "__main__":
    main()
