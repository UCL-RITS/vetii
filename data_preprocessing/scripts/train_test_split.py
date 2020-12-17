import os
import pandas as pd
from sklearn.model_selection import train_test_split

import shutil


def float_fraction(trainpct):
    """ Float bounded between 0.0 and 1.0 """
    try:
        f = float(trainpct)
    except ValueError:
        raise Exception("Fraction must be a float")
    if f < 0.0 or f > 1.0:
        raise Exception("Argument should be a fraction! Must be <= 1.0 and >= 0.0")
    return f


def split_dataset(dataset_file, trainpct):
    """
    Split a file containing the full path to individual annotation files into
    train and test datasets, with a split defined by trainpct.


    Inputs:
    - dataset_file - a .txt or .csv file containing file paths pointing to annotation files.
      (Expects that these have no header)
    - trainpct = 0.8 produces an 80:20 train:test split
    """
    if type(dataset_file) is list:
        full_dataset = pd.DataFrame(dataset_file, columns=["Filename"])
    else:
        full_dataset = pd.read_csv(dataset_file, names=["Filename"])
    print(
        "You've chosen a training percentage of: {} (this variable has type: {})".format(
            trainpct, type(trainpct)
        )
    )
    testsize = 1.0 - trainpct
    train, test = train_test_split(
        full_dataset, test_size=testsize, shuffle=True, random_state=42
    )  # set the random seed so we get reproducible results!
    return train, test


def output_files(outdir, train, test):
    train_out_name = os.path.join(outdir, "xml_annotations_train.txt")
    test_out_name = os.path.join(outdir, "xml_annotations_test.txt")
    train.to_csv(train_out_name, header=None, index=False)
    print("Written train annotation set to: {}".format(train_out_name))
    test.to_csv(test_out_name, header=None, index=False)
    print("Written test annotation set to: {}".format(test_out_name))
    return


def move_image_files(workdir, train, test, annotations_dir_name, params):
    train_dir_name = params["split_dataset"]["train_dir"]
    test_dir_name = params["split_dataset"]["valid_dir"]
    img_dir_name = params["split_dataset"]["img_dir"]
    file_type = params["split_dataset"]["file_type"]

    train_img_dir = os.path.join(workdir, train_dir_name)
    test_img_dir = os.path.join(workdir, test_dir_name)
    if not os.path.exists(train_img_dir):
        os.mkdir(train_img_dir)
    if not os.path.exists(test_img_dir):
        os.mkdir(test_img_dir)

    train_img_paths = train["Filename"].tolist()
    test_img_paths = test["Filename"].tolist()

    for img_file in train_img_paths:
        print(img_file)
        old_img_file_path = img_file.replace(annotations_dir_name, img_dir_name)
        old_img_file_path = old_img_file_path.replace("xml", file_type)
        new_img_file_path = old_img_file_path.replace(img_dir_name, train_dir_name)
        shutil.copyfile(old_img_file_path, new_img_file_path)

    for img_file in test_img_paths:
        old_img_file_path = img_file.replace(annotations_dir_name, img_dir_name)
        old_img_file_path = old_img_file_path.replace("xml", file_type)
        new_img_file_path = old_img_file_path.replace(img_dir_name, test_dir_name)
        shutil.copyfile(old_img_file_path, new_img_file_path)
    return


def main():
    from read_params import read_parameter_file

    params = read_parameter_file("params.yaml")
    float_fraction(params["split_dataset"]["trainpct"])
    xml_annotations_dir = params["split_dataset"]["annotations_dir"]
    print("Generating list of xml annotation files from {}".format(xml_annotations_dir))

    file_list = []
    for xml_file in os.listdir(os.path.join(os.getcwd(), xml_annotations_dir)):
        file_list.append(os.path.join(os.getcwd(), xml_annotations_dir, xml_file))
    train_set, test_set = split_dataset(file_list, params["split_dataset"]["trainpct"])

    output_files(os.getcwd(), train_set, test_set)
    workdir = os.getcwd()
    move_image_files(workdir, train_set, test_set, xml_annotations_dir, params)
    return


if __name__ == "__main__":
    main()
