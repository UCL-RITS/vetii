import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def setup_target_dir(tmpdir_factory):
    test_target_dir = tmpdir_factory.mktemp("data_testset")

    train_label_dir = tmpdir_factory.mktemp("train_labels")
    val_label_dir = tmpdir_factory.mktemp("val_labels")
    train_img_dir = tmpdir_factory.mktemp("train_imgs")
    val_img_dir = tmpdir_factory.mktemp("val_labels")

    setup_dict = {
        "train_label_dir": str(train_label_dir),
        "val_label_dir": str(val_label_dir),
        "train_img_dir": str(train_img_dir),
        "val_img_dir": str(val_img_dir),
        "target_dir": str(test_target_dir)
    }
    return setup_dict