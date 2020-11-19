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
You may notice that the annotations are provided in XML format, which may be incompatible with some neural network architectures described in this repository. It should also be noted
that the XML labels contain several classes (ship, multi_224, multi, ok) which will affect transformations to other label formats. Additionally, the width and height in the `size` element may show `224` pixels when
all provided images are 512 x 512 pixel. This has been observed to affect the YOLO-style label format on conversion, so should either be changed pre-conversion or taken into consideration when converting between label formats.








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