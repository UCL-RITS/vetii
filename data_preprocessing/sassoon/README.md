# Sassoon Dock dataset preparation

* This directory should initially contain an `images` directory and an `xml_annotations` directory.
* Image annotations are provided in this repository
* Images are provided in JPG format for now, but may be moved out of this repository in the near future.
* Run the data prep pipeline (requires DVC to be installed) with
```bash
dvc repro
```