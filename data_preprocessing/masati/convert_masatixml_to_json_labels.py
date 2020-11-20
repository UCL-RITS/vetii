import argparse
import os
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm

def map_class_to_id(classes):
    """
    Get a 1-indexed id for each class given as an argument

    Note that for MASATI, len(classes) == 1 when only considering boats
    Args: 
        classes (list): A list of classes present in the dataset
    Returns:
        dict[str, int]
    """
    class_ids = list(range(1, len(classes)+1))
    return dict(zip(classes, class_ids))

def convert_xml(label_list, class_index, output_json, is_masati, output_dir):
    """
    Function to convert individual xml files to a json format and produce
    a single composite file for use as an input to NN models.

    Produces output json files for the training and test sets.

    Args:
        label_list (tuple[test/train filename, test/train files]): list-of-lists of xml labels, separated by training and test set
        class_index (Dict[str, int]): Dictionary mapping class labels to the class id (an integer)
        output_json (Dict[str, list/str): Output json dictionary with entries either [str, list] or [str, str]
        is_masati (bool): Bool signifying if we're processing the MASATI-v2 dataset
        output_dir (str): Directory where output json files are created
    
    Returns: None
    """
    # Set a 1-indexed id for the label
    label_id = 1
    assert len(label_list) == 2

    # Derive output file name from the input file supplied


    output_json_file = os.path.splitext(label_list[0].split("_",1)[-1])[0]+".json"
    assert os.path.exists(output_dir)
    output_json_path = os.path.join(output_dir, output_json_file)
    
    for label_file in tqdm(label_list[1]):
        label_tree = ET.parse(label_file)
        xml_root = label_tree.getroot()

        xml_file_path = label_file
        xml_file = os.path.basename(xml_file_path)
        # get image name with extension
        img_name = xml_file.replace("xml","png")
        # get image name without extension and remove leading zeros (should be a string of integers...)
        image_id = int(os.path.splitext(img_name)[0].lstrip("0"))
        size = xml_root.find('size')
        # If it's not masati, actually get the width and height of bounding boxes
        if not is_masati:
            width = int(size.findtext('width'))
            height = int(size.findtext('height'))
        # Otherwise, we know all images in masati are 512x512 pixel
        else:
            width = 512
            height = 512
        image_metadata = {
            'file_name': img_name,
            'height': height,
            'width': width,
            'id': image_id
        }
        output_json['images'].append(image_metadata)

        # Find all classes in the xml file and get the bounding boxes
        # Our masati analysis only considers the "boat" class, so override the "multi_224"
        # etc classes with that
        for class_label in xml_root.findall('object'):
            if not is_masati:
                label = class_label.findtext('name')
            # If it *is* masati, everything is a boat!
            else:
                label = "boat"
            assert label in class_index
            class_id = class_index[label] # for boat should be 1 (remember 1-indexing!)
            
            bounding_box = class_label.find('bndbox')
            xmin = int(bounding_box.findtext('xmin')) - 1
            ymin = int(bounding_box.findtext('ymin')) - 1
            xmax = int(bounding_box.findtext('xmax'))
            ymax = int(bounding_box.findtext('ymax'))
            assert xmin < xmax
            assert ymin < ymax
            bounding_box_width = xmax - xmin
            bounding_box_height = ymax - ymin
            json_label = {
                'area': bounding_box_width * bounding_box_height,
                'iscrowd': 0,
                'bbox': [xmin, ymin, bounding_box_width, bounding_box_height],
                'category_id': class_id,
                'ignore': 0,
                'segmentation': [], # Supply empty list, only looking at object detection
                'image_id': image_id,
                'id': label_id,
            }
            output_json['annotations'].append(json_label)
            label_id += 1

    for class_label, class_id in class_index.items():
        categories_metadata = {
            'supercategory': 'none',
            'id': class_id,
            'name': class_label}
        output_json['categories'].append(categories_metadata)
    with open(output_json_path, 'w+') as out_json:
        # Dump json to string and write to file!
        out_json.write(json.dumps(output_json))
    return
def prepare_for_conversion(labels, class_index, is_masati, output_dir):
    """
    Collects arguments and defines the output json structure for 
    use in convert_xml

    Args:
        labels (list[train, test]): list of training and test xml files
        class_index (dict[str,int]): dictionary mapping class labels to an int id
        is_masati (bool): bool denoting whether we're processing masasti
        output_dir (str): directory where output json files will be created

    Returns: NoneType
    """

    output_json= {
        "images": [],
        "type": "instances",
        "annotations": [],
        "categories": []
    }
    for label_type in labels:
        convert_xml(label_type, class_index, output_json, is_masati, output_dir)
    return

def main(args):
    """
    Convert xml-style image labels to coco-style json labels.
    Args:
        args (argparse.Namespace object)
    """
    
    
    xml_annotations_train = args.train_labels
    xml_annotations_test = args.test_labels
    
    is_masati = args.is_masati
    class_index = map_class_to_id(args.classes)

    training_annotations = [line.rstrip() for line in open(xml_annotations_train)]
    test_annotations = [line.rstrip() for line in open(xml_annotations_test)]

    training_set = (xml_annotations_train, training_annotations)
    test_set = (xml_annotations_test, test_annotations)

    output_dir = os.path.join(os.getcwd(), "coco_json_annotations")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    
    labels = [training_set, test_set]
    prepare_for_conversion(
        labels,
        class_index,
        is_masati,
        output_dir,
    )
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_labels', type=str, default=None, required = True,
                        help='annotation labels for training')
    parser.add_argument('--test_labels', type=str, default=None, required = True,
                        help='annotation labels for validation')
    parser.add_argument('--classes', type=list, default=["boat"],
                        help='list of classes in your dataset (only one for our MASATI testing)')
    parser.add_argument('--is_masati', type=bool, default=True,
                        help='Is this MASATI? If it is, we can hard-code a couple of things...')

    args = parser.parse_args()
    main(args)
