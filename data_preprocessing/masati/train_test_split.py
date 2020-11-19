import os
import numpy as np
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split

def float_fraction(arg):
    """ Float bounded between 0.0 and 1.0 """
    try:
        f = float(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Fraction must be a float")
    if f < 0.0 or f > 1.0:
        raise argparse.ArgumentTypeError("Argument is a fraction! Must be <= 1.0 and >= 0.0")
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
    testsize = 1.-trainpct
    train, test = train_test_split(full_dataset, test_size = testsize, shuffle=True, random_state=42) # set the random seed so we get reproducible results!
    return train, test
    

def output_files(train, test):
    train_out_name = os.path.join(os.getcwd(), "xml_annotations_train.txt")
    test_out_name = os.path.join(os.getcwd(), "xml_annotations_test.txt")
    train.to_csv(train_out_name, header=None, index=False)
    print("Written train annotation set to: {}".format(train_out_name))
    test.to_csv(test_out_name, header=None, index=False)
    print("Written test annotation set to: {}".format(test_out_name))
    return

def main(args):

    if len(args.annotation_paths_file) < 1:
        print("Generating list of xml annotation files from current directory")
        file_list=[]
        for xml_file in os.listdir(os.path.join(os.getcwd(),"xml_annotations")):
            file_list.append(os.path.join(os.getcwd(),"xml_annotations",xml_file))
        train_set, test_set = split_dataset(file_list, args.trainpct)                   
    else:
        print("Running split dataset for paths in file {}".format(args.annotation_paths_file))
        train_set, test_set = split_dataset(args.annotation_paths_file, args.trainpct)

    output_files(train_set, test_set)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Provide a dataset to split into test and eval')
    parser.add_argument('-a',
                        '--annotation_paths_file',
                        type = str,
                        default = '',
                        help='Provide a file of annotation file paths to split into test and eval sets')
    parser.add_argument('--trainpct',
                        type = float_fraction,
                        default = '0.75', # default 75% train, 25% eval
                        help="Define the fraction of data to be used for training")
    args = parser.parse_args()
    main(args)
