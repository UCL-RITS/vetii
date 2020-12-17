import os
import pytest
import pandas as pd
from pathlib import Path
from .fixtures.setup_train_test_split import setup_file_list, setup_move_img_files, setup_out_dir
from ..scripts import train_test_split as funcs


def test_float_fraction():

    with pytest.raises(Exception) as string_exception:
        funcs.float_fraction("string")
    assert string_exception.value.args[0] == "Fraction must be a float"

    with pytest.raises(Exception) as below_zero_exception:
        funcs.float_fraction(-0.5)
    assert below_zero_exception.value.args[0] == "Argument should be a fraction! Must be <= 1.0 and >= 0.0"

    with pytest.raises(Exception) as above_one_exception:
        funcs.float_fraction(1.5)
    assert above_one_exception.value.args[0] == "Argument should be a fraction! Must be <= 1.0 and >= 0.0"


    assert funcs.float_fraction(0.75) <= 1.0
    assert funcs.float_fraction(0.75) >= 0.0

@pytest.mark.usefixtures("setup_file_list")
def test_split_dataset(setup_file_list):
    test_file_list = setup_file_list
    train_set, test_set = funcs.split_dataset(test_file_list, 0.75)
    assert len(train_set) == 3
    assert len(test_set) == 1

@pytest.mark.usefixtures("setup_out_dir")
def test_output_files(setup_out_dir):
    outdir = setup_out_dir
    train_list = pd.DataFrame()
    test_list = pd.DataFrame()
    funcs.output_files(outdir, train_list, test_list)
    assert len(os.listdir(outdir)) == 2
    assert 'xml_annotations_train.txt' in os.listdir(outdir)
    assert 'xml_annotations_test.txt' in os.listdir(outdir)

@pytest.mark.usefixtures("setup_move_img_files")
def test_move_image_files(setup_move_img_files):
    test_variables = setup_move_img_files
    workdir = str(Path(test_variables["params"]["split_dataset"]["train_dir"]).parent)
    funcs.move_image_files(
        workdir,
        test_variables["train"],
        test_variables["test"],
        test_variables["labels"],
        test_variables["params"]
    )
