from libtiff import TIFF
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from os import listdir, getenv
from os.path import isfile, join,abspath
from typing import List

load_dotenv()


IMAGES_PATH = getenv('IMAGES_PATH')

def read_images_dir(path: str):
  files: List[str] = []
  for item in listdir(path):
    full_path = join(path, item)
    if isfile(full_path):
      files.append(full_path)
    else:
      for _item in read_images_dir(full_path):
        files.append(_item)
  return files

def create_tiff_from_images(src_path: str, dest_path: str):
  read_images_dir(src_path)

create_tiff_from_images(src_path=IMAGES_PATH, dest_path=abspath('./tmp/result.tif'))

data = np.random.randint(0, 255, (10,10)).astype(np.uint8)
im = Image.fromarray(data)
im.save('test.tif')

tif = TIFF.open('test.tif', mode='r')
