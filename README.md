# VETII Boat Detection
## Detecting fishing boats in Sassoon Docks

This repository contains code to pre-process datasets containing labelled satellite images of boats for use with a YOLOv5 model.

## Contributors :hammer_and_wrench:

A list of key developers on the project.

| Name               | GitHub ID                                            | Email                       | 
| ------------------ | -----------------------------------------------------| --------------------------- | 
| Harry Moss    | [@harryjmoss](https://github.com/harryjmoss) | <h.moss@ucl.ac.uk>   |
| Sanaz Jabbari | [@sanazjb](https://github.com/sanazjb) |  |  

## Contents :book:
* [Setup](##setup-:construction_worker::wrench:)
* [VETII weight generation](##training-a-yolov5-model-for-VETII-:weight_lifting:)
    * [Data preprocessing](###data-preprocessing)
    * [Model training](###model-training)
* [Inference](##inference)
* [Contributing](##contributing-:pencil:)
* [Style guide](##style-guide-:art:)
* [Contact](#contact)

## Setup :construction_worker::wrench:

Get your own copy up and running by on Linux/macOS by following these simple steps:

1. Clone the repository
```bash
git clone https://github.com/UCL-RITS/vetii
```
2. Install dependencies (preferably within a virtual environment)
```bash
cd vetii/
python -m venv your_virtual_environment_name_here
source your_virtual_environment_name_here/bin/activate
pip install --upgrade pip
pip install -r requirements/base.txt
```
3. Clone the YOLOv5 model repository (with VETII settings and modifications) **within** the VETII repository
```bash
git clone https://github.com/harryjmoss/yolov5.git
```
4. Install model dependencies
```bash
cd yolov5
pip install -r requirements.txt
```

## Training a YOLOv5 model for VETII :weight_lifting:

The approach taken in the VETII project was as follows:

 **Data preprocessing**:  

0. Pre-process all data, generate labels in the correct format, split datasets into train/validation sets and place into a suitable file structure.  

**Training**:
1. Use [transfer learning](https://en.wikipedia.org/wiki/Transfer_learning) to train an existing pre-trained model on a large dataset of aerial images of boats. A subset of the [MASATI-v2 dataset](https://www.iuii.ua.es/datasets/masati/) was chosen for training. After an initial literature search and comparison of three models, YOLOv5x was chosen as the candidate model.
2. Using the output weights from step 1, further train the model using a curated dataset with satellite images of Sassoon Dock, Mumbai. Images were generated using Google Earth Pro and annotated with [labelImg](https://github.com/tzutalin/labelImg)  



Each step is described in detail below. 

### Data preprocessing

The data provided within this project, and available externally, requires some preprocessing before it can be used to **train** YOLOv5 models. The steps described in this section are **not** necessary if you're using the model to detect boats within images!

In the following, `$VETII` refers to the directory containing **this** README.  

**For MASATI**  

`cd` into the MASATI-v2 data preprocessing directory
```bash
cd $VETII/data_preprocessing/masati/
```
Request the dataset from the researchers [here](https://goo.gl/forms/xrBmFfbSuwpyb3wS2) (google form to request the dataset from the researchers) - you will receive a link to a google drive file with a url like 
```
https://drive.google.com/file/d/<GOOGLE-DRIVE-ID>/view
```
Extract `<GOOGLE-DRIVE-ID>` from the link above. Download and extract the dataset with
```bash
gdown https://drive.google.com/uc?id=<GOOGLE-DRIVE-ID>
unzip MASATI-v2.zip
rm MASATI-v2.zip
```
the dataset will be extracted to `$VETII/data_preprocessing/masati/MASATI-v2`

All stages of data preprocessing can then be run with
```bash
dvc repro
```
By default, this uses a 75:25 train:validation dataset split. To change this, or any other parameter in the data preprocessing, see `params.yaml`.

After data preprocessing, the current directory will look like

```bash
$VETII/data_preprocessing/masati/
├── MASATI-v2/ # original extracted folder
├── MASATI-v2.zip
├── PNGImages/ # all masati images
├── __init__.py
├── coco_json_annotations/ # masati labels in a json format
├── convert_masatixml_to_json_labels.py
├── convert_xml_to_yolotxt.py
├── dvc.lock
├── dvc.yaml
├── filename_mapping.csv
├── masati_instructions.md
├── modified_xml_annotations/ # corrected masati xml labels
├── params.yaml
├── refine_masati.py
├── remove_extra_classes.py
├── sort_yolo_images.py
├── train/ # training image set
├── train_test_split.py
├── validation/ # validation image set
├── xml_annotations/ # uncorrected masati xml labels
├── xml_annotations_test.txt
├── xml_annotations_train.txt
├── yolo_annotations/ # annotations in YOLO .txt format
├── yolo_images_train/ # renamed training set images for YOLOv5 compatibility
├── yolo_images_validation/ # renamed validation set images for YOLOv5 compatibility
├── yolo_labels_train/  # training set labels
└── yolo_labels_validation/ # validation set labels
```
and the `$VETII/data/masati` directory will contain files in the necessary structure for use with YOLOv5:
```bash
$VETII/data/masati
├── images
│   ├── train
│   └── val
└── labels
    ├── train
    └── val
```


**For Sassoon Dock dataset**  

`cd` into the Sassoon Dock data preprocessing directory
```bash
cd $VETII/data_preprocessing/sassoon/
```

Download the dataset tarball - currently available through the VETII sharepoint site, but liable to move to UCL RDS in the near future - and place it in the data preprocessing directory.

Extract the dataset with
```bash
tar -xzvf sassoon_dock-v2.tar.gz
```

Run the data preprocessing with
```bash
dvc repro
```

Files will be placed within `$VETII/data/sassoon`, which should look like
```bash
$VETII/data/sassoon
├── images
│   ├── train
│   └── val
└── labels
    ├── train
    └── val
```

### Model training

After cloning the [VETII YOLOv5 fork](https://github.com/harryjmoss/yolov5) inside the `$VETII` directory and installing the required dependencies, model training is performed using the following commands

Note: the `runs/train/expN` directory will change as a function of `N` training runs
1. Training the model with the MASATI-v2 dataset 

Use the following commands to recreate the training used during the VETII project (two training runs with 50 epochs each), or use a single command training on 100 epochs. Results should be similar.

```bash
cd $VETII/yolov5

python train.py --img 512 --batch 8 --epochs 50 --data masati.yaml --weights yolov5x.pt --workers 0

cp runs/train/exp/weights/best.pt weights/masati_yolov5x_50epoch_training.pt

python train.py --img 512 --batch 16 --epochs 50 --data masati.yaml --weights weights/masati_yolov5x_50epoch_training.pt --workers 0

cp runs/train/exp2/weights/best.pt weights/masati_yolov5x_100epoch_best.pt
```
Results finished in <8 hours using a V100 GPU. 

2. Training the model with the Sassoon Dock dataset

Recover the model weights used for inference in the VETII project with the following commands:

```bash
cd $VETII/yolov5

python train.py --img 1175 --rect --batch 2 --epochs 100 --data sassoon.yaml --weights weights/masati_yolov5x_100epoch_best.pt --workers 0

cp runs/train/exp3/weights/best.pt weights/sassoon100epoch_best_trained_on_masati_yolov5x_100epoch.pt

python train.py --img 1175 --rect --batch 8 --epochs 50 --hyp data/hyp.sassoon.yaml --data sassoon.yaml --weights weights/sassoon100epoch_best_trained_on_masati_yolov5x_100epoch.pt --workers 0

cp runs/train/exp4/weights/best.pt weights/sassoon_dock_final_weights.pt
```

You should then have an equivalent set of weights to the ones found on the VETII sharepoint [here](https://liveuclac.sharepoint.com/sites/RADDISH/Shared%20Documents/VETII/Model_weights/sassoon_wandb_best_150epoch_trained_on_masati100epoch_yolov5x.pt).


## Inference
*... or, detecting boats with the trained model*

This step requires the use of either the model weights provided the VETII sharepoint or produce your own by following the steps in [the training section](###model-training). These weights should be placed in the `$VETII/yolov5/weights` directory.

To detect boats within images (of `jpg` or `png` format), place them within the `$VETII/yolov5/data/images` directory. For example, to detect boats in images of the Sassoon Dock, use the following command for images in the `$VETTI/yolov5/data/images/sassoon/` directory 
```bash
$ python detect.py --weights weights/sassoon_wandb_best_150epoch_trained_on_masati100epoch_yolov5x.pt --img 1175 --conf 0.25 --source data/images/sassoon --iou-thres 0.5 --save-txt --save-conf
```
Arguments used:
* `img`: the image width in pixels
* `conf`: confidence threshold (~prediction probability threshold)
* `source`: location of an image file or image directory
* `iou-thres`: [Intersection over union (IoU)](https://en.wikipedia.org/wiki/Jaccard_index) (or Jaccard index) threshold applied during detection - this is the minimum IoU score
* `save-txt`: If present, saves the coordinates of the centre coordinate, width and height of the bounding boxes around detected boats. **For VETII this should always be included!**
* `save-conf`: Saves confidence scores in the final column of the text output **Include this for VETII!**

Outputs can be found in the `runs/detect` directory. An example output directory for a single image detection should look something like
```bash
├── 00001.jpg
├── centre_dot_00001.jpg
└── labels
    └── 00001.txt
```

The output text file format for a single input image will look like

```bash
Object_ID   Class   x   y   width   height  confidence   

```

For the pre-trained MASATI+Sassoon model, `Class` will always equal zero as the model was trained on a single class of object, `boat`. The `Object_ID` is unique to each detected object in the image, and is also written onto the corresponding output `centre_dot_` image.

## Contributing :pencil:
A great place to get started is to first take a look at any [open issues](https://github.com/UCL-RITS/vetii/issues). 

If you spot something else and would like to work on it, please feel free to create an issue.

Once you've found something to work on, the suggested workflow is:

1. Fork this repository
2. Create your new feature in a branch (`git checkout -b feature/MyNewGreatFeature`)
3. Commit your changes with a descriptive and helpful commit message (`git commit -m 'Adding MyNewGreatFeature'`)
4. Push your changes to your forked remote (`git push my_vetii_fork feature/AmazingFeature`)
5. Open a pull request to merge your changes into the `main` branch.

## Style guide :art:
### Code :computer:
Python code should be PEP8 compliant where possible, using [black](https://black.readthedocs.io/en/stable/) to make life easier.

### Documentation :closed_book:
Before being merged into `main`, all code should have well writen documentation, including the use of docstrings. Adding and updating existing documentation is highly encouraged.

### Gitmoji :smiley:
Optional, but recommended - [gitmoji](https://gitmoji.carloscuesta.me/) for an emoji:commit message dictionary. This also includes an optional [gitmoji-cli](https://github.com/carloscuesta/gitmoji-cli) as a hook so you remember when you write commits!

### Working on an issue :construction_worker:
The branch naming convention is `iss_<issue-number>_<short_decription>`, where `<issue-number>` is the issue number and `<short_description>` is a short description of the issue.

### Running tests :microscope:
Contributing to existing to tests or adding new ones will always be well received! Please include tests in any contributed code before requesting to merge, if appropriate.

## Contact :envelope:

Harry Moss - [@invariantmoss](https://twitter.com/invariantmoss)