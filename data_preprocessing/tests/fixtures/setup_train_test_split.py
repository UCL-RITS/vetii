import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture(scope="session")
def setup_file_list(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("test_split")
    test_xml_one = temp_dir.join("test_1.xml")
    test_xml_two = temp_dir.join("test_2.xml")
    test_xml_three = temp_dir.join("test_3.xml")
    test_xml_four = temp_dir.join("test_4.xml")

    test_file_list = [
        str(test_xml_one),
        str(test_xml_two),
        str(test_xml_three),
        str(test_xml_four),
        ]
    return test_file_list

@pytest.fixture(scope="session")
def setup_out_dir(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("test_outdir")
    return temp_dir

@pytest.fixture(scope="session")
def setup_move_img_files(tmpdir_factory):

    test_labels_dir = tmpdir_factory.mktemp("label")
    test_labels_dir.join("test_1.xml")
    test_labels_dir.join("test_2.xml")
    
    test_train_dir = tmpdir_factory.mktemp("train")
    test_valid_dir = tmpdir_factory.mktemp("valid")

    test_img_dir = tmpdir_factory.mktemp("img")
    test_img_one = test_img_dir.join("test_1.png")
    test_img_one.write("test1")
    test_img_two = test_img_dir.join("test_2.png")
    test_img_two.write("test2")
    assert test_img_one.read() == "test1"
    assert test_img_two.read() == "test2"

    test_val_dict = {
            "Filename": [str(test_img_dir)+"/test_1.png"]
        }
    
    test_train_dict = {
            "Filename": [str(test_img_dir)+"/test_2.png"]
        }
    test_train_set = pd.DataFrame.from_dict(test_train_dict)
    test_val_set = pd.DataFrame.from_dict(test_val_dict)


    params = {
        "split_dataset": {
            "train_dir": str(test_train_dir),
            "valid_dir": str(test_valid_dir),
            "img_dir": str(test_img_dir),
            "file_type": "png"
        }
    }
    setup_dict = {
        "train": test_train_set,
        "test": test_val_set,
        "labels": str(test_labels_dir),
        "params": params
    }
    return setup_dict

