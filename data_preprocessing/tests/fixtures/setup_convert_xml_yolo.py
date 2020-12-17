import pytest


@pytest.fixture(scope="session")
def create_temp_file_io(tmpdir_factory):
    """
    Set up files for convert_xml_annotation_to_yolo
    Uses 0910.xml from masati data prep
    """
    test_xml = tmpdir_factory.mktemp("test_conversion").join("test.xml")
    test_outdir = tmpdir_factory.mktemp("test_output")
    test_xml_string = (
        r"<annotation>"
        r"<folder>coast_ship</folder>"
        r" <filename>x0971.png</filename>"
        r" <path>C:\Users\Tofahito\Documents\PHD\NUEVAS_IMAGES_A_ETIQUETAR\coast_ship\x0971.png</path>"
        r" <source>"
        r" <database>Unknown</database>"
        r" </source>"
        r" <size>"
        r" <width>512</width>"
        r" <height>512</height>"
        r" <depth>3</depth>"
        r" </size>"
        r" <segmented>0</segmented>"
        r" <object>"
        r" <name>ship</name>"
        r" <pose>Unspecified</pose>"
        r" <truncated>0</truncated>"
        r" <difficult>0</difficult>"
        r" <bndbox>"
        r" <xmin>469</xmin>"
        r" <ymin>28</ymin>"
        r" <xmax>472</xmax>"
        r" <ymax>37</ymax>"
        r" </bndbox>"
        r" </object>"
        r" </annotation>"
    )
    test_xml.write(test_xml_string)
    return test_xml, test_outdir
