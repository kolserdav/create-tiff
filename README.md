# Create TIFF
Create tiff image from a list of images.


## Possibilities
- Flexible size of composite images
- Adjusting the dimensions of the resulting image
- It is possible to exclude subdirectories or files

## Requirements
- Python: ^3.11.8
- Pip: ^24.0

## Installation
1. Install dependencies:
```sh
pip install -r requirements.txt 
```
2. Copy file `.env.example` to `.env`

## Configuration
Edit file `.env`:
```ini
# Source images path
IMAGES_PATH=/abs/path/to/images/dir

# Result image dimensions
WIDTH=1920
HEIGHT=1080

# List of excluded dirs or files
#EXCLUDE_NAMES=1388_12_Наклейки 3-D_3,1388_6_Наклейки 3-D_2
```
## Usage
Run:
```sh
python main.py
```
Show results in `tmp/result.tiff`