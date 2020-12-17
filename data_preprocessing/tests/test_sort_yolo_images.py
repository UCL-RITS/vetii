import pytest
import os
from pathlib import Path
from ..scripts import sort_yolo_images as funcs
from .fixtures.setup_sort_yolo_images import setup_yolo_dirs, setup_yolo_rename_dirs


@pytest.mark.usefixtures("setup_yolo_dirs")
def test_create_yolo_dirs(setup_yolo_dirs):
    test_label_dir, _ = setup_yolo_dirs
    workdir = str(Path(test_label_dir).parent)
    assert str(test_label_dir) == os.path.join(workdir, test_label_dir)
    assert len(os.listdir(os.path.join(workdir, "label_sortyolo0"))) == 2
    assert len(os.listdir(os.path.join(workdir, "train0"))) == 2

    out_img_dir, out_label_dir = funcs.create_yolo_dirs(
        workdir,
        "train0",
        "label_sortyolo0",
    )
    print(out_img_dir, out_label_dir)
    assert str(out_img_dir) == os.path.join(workdir, "yolo_images_train0")
    assert str(out_label_dir) == os.path.join(workdir, "yolo_labels_train0")
    assert len(os.listdir(out_img_dir)) == 2
    assert len(os.listdir(out_label_dir)) == 2


@pytest.mark.usefixtures("setup_yolo_rename_dirs")
def test_rename_yolo_files(setup_yolo_rename_dirs):
    test_label_dir, test_img_dir = setup_yolo_rename_dirs
    workdir = Path(str(test_label_dir)).parent

    assert os.listdir(test_label_dir)[0] == "test_1.txt"
    assert os.listdir(test_img_dir)[0] == "test_1.jpg"
    funcs.rename_yolo_files(str(workdir), test_label_dir, "jpg")

    assert os.listdir(test_label_dir)[0] == "00001.txt"
    assert os.listdir(test_img_dir)[0] == "00001.jpg"
