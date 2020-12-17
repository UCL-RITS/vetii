import pytest
import os
from pathlib import Path
from ..scripts import prepare_yolov5 as funcs
from .fixtures.setup_prepare_yolov5 import setup_target_dir


@pytest.mark.usefixtures("setup_target_dir")
def test_create_yolo_dirs(setup_target_dir):
    setup_dict = setup_target_dir
    output_dirs = funcs.create_yolo_dirs(
        setup_dict["train_label_dir"],
        setup_dict["val_label_dir"],
        setup_dict["train_img_dir"],
        setup_dict["val_img_dir"],
        setup_dict["target_dir"],
    )
    assert len(output_dirs) == 4


# @pytest.mark.usefixtures("setup_yolo_rename_dirs")
