import os
import pytest
from pathlib import Path
from .fixtures.setup_convert_xml_yolo import create_temp_file_io
from ..scripts import convert_xml_to_yolotxt as funcs


def test_yolo_conversion():
    """
    Tests yolo_conversion
    Uses 0910.xml from masati data prep
    """

    boundaries = (469, 472, 28, 37)


    width = 512.0
    height = 512.0
    bounding_box = funcs.yolo_conversion((width, height), boundaries)
    expected_bounding_box = [0.9189453125, 0.0634765625, 0.005859375, 0.017578125]
    assert list(bounding_box) == expected_bounding_box

@pytest.mark.usefixtures("create_temp_file_io")
def test_convert_xml_annotation_to_yolo(create_temp_file_io):
    test_xml, test_outdir = create_temp_file_io
    print(test_xml, test_outdir)
    funcs.convert_xml_annotation_to_yolo(test_xml, test_outdir, True, ['boat'])
    assert len(os.listdir(test_outdir)) == 1
    assert os.listdir(test_outdir)[0] == "test.txt"
    output_file = os.path.join(test_outdir,"test.txt")
    output_text = Path(output_file).read_text().replace("\n", "")
    assert output_text == "0 0.9189453125 0.0634765625 0.005859375 0.017578125"