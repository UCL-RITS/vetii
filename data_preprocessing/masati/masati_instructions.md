# Preprocessing MASATI-v2
These instructions explore the process of obtaining and preprocessing the MASATI-v2 dataset for use with the models described in this repository.
The MASATI dataset is not supplied with this repository - a link to the dataset must be obtained from the [researchers' website](https://www.iuii.ua.es/datasets/masati/)

## Obtaining the MASATI (v2) dataset

The [MASATI dataset](https://www.iuii.ua.es/datasets/masati/) is available on request from researchers at the University of Alicante after filling
in the [following form](https://goo.gl/forms/xrBmFfbSuwpyb3wS2).

Once you have the link, the zip file can be downloaded from google drive using `gdown` and the file ID found in the URL:

```
gdown https://drive.google.com/uc?id=<gdrive-file-id>
```

Uncompress the dataset with
```
unzip MASATI-v2.zip
```
which will extract the dataset into the original folder structure.

## Getting necessary files and annotationss
For the models we will train with MASATI, we don't require negative examples (images containing zero boats),
so these can be removed using `refine_masati.py`
```
python refine_masati.py
```
which creates the `xml_annotations` and `PNGImages` directories in the current directory (which should also contain the MASATI-v2/ directory)

## Exploring the labelling
You may notice that the annotations are provided in XML format, with a single xml annotation file for all annotations of a single image. This format may be/is definitely incompatible with some neural network architectures described in this repository. It should also be noted
that the XML labels contain several classes (ship, multi_224, multi, ok) which will affect transformations to other label formats. Additionally, the width and height in the `size` element may show `224` pixels when
all provided images are 512 x 512 pixel. This has been observed to affect the YOLO-style label format on conversion, so should either be changed pre-conversion or taken into consideration when converting between label formats.

## YOLO labels
YOLO-style `.txt` labels can be created using
```
python convert_xml_to_yolotxt.py
```
which takes an `is_masati` argument that, when `True`, hard codes the width and height to 512 pixels as described above and sets the class of all labels to `boat`.

YOLO-style labels consist of a single `.txt` annotation file for each image, and are of the format:

```
class x y width height
```
where `class` is the zero-indexed class label, `x` and `y` are the coordinates of the centre of a bounding box and the bounding box has a given `width` and `height`.
For example (from the MASATI label `s0276.txt`)

```
0 0.80859375 0.1982421875 0.15625 0.060546875
```

A final thing to note with the YOLO-inspired models (including YOLT and variants) is that they don't split data into a training and evaluation set.


## COCO-style json labels

Models like the pytorch recast of EfficientDet require the labels to be in JSON format with a single annotation file for all annotations. You can (should) still use a
train/test split with these labels, just produce a `.json` for your train set and another for your test/validation set.







If you use the dataset in any work, remember to cite it!

```
@article{Gallego2018,
    author    = {Antonio-Javier Gallego, Antonio Pertusa, and Pablo Gil},
    title     = {Automatic Ship Classification from Optical Aerial Images 
                 with Convolutional Neural Networks},
    journal   = {Remote Sensing},
    volume    = {10},
    number    = {4},
    year      = {2018},
    ISSN      = {2072-4292},
    doi       = {10.3390/rs10040511}
  }
```