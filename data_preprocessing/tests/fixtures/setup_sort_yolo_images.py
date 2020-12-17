import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def setup_yolo_dirs(tmpdir_factory):

    test_label_dir = tmpdir_factory.mktemp("label_sortyolo")
    test_label_one = test_label_dir.join("test_1.txt")
    test_label_one.write("test_label_1")
    test_label_two = test_label_dir.join("test_2.txt")
    test_label_two.write("test_label_2")

    test_img_dir = tmpdir_factory.mktemp("train")
    test_img_one = test_img_dir.join("test_1.png")
    test_img_one.write("test_img_1")
    test_img_two = test_img_dir.join("test_2.png")
    test_img_two.write("test_img_2")

    assert test_label_one.read() == "test_label_1"
    assert test_label_two.read() == "test_label_2"
    assert test_img_one.read() == "test_img_1"
    assert test_img_two.read() == "test_img_2"

    return test_label_dir, test_img_dir


@pytest.fixture(scope="session")
def setup_yolo_rename_dirs(tmpdir_factory):

    test_old_label_dir = tmpdir_factory.mktemp("test_labels")
    test_label_one = test_old_label_dir.join("test_1.txt")
    test_label_one.write("test_label_1")

    test_old_img_dir = tmpdir_factory.mktemp("test_images")
    test_img_one = test_old_img_dir.join("test_1.jpg")
    test_img_one.write("test_img_1")

    assert test_label_one.read() == "test_label_1"
    assert test_img_one.read() == "test_img_1"

    return test_old_label_dir, test_old_img_dir
