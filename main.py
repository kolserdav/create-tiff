from PIL import Image
from dotenv import load_dotenv
from os import listdir, getenv
from os.path import isfile, join, abspath
from typing import List

load_dotenv()

# Constants
SHIFT_STEP = 10
RESULT_FILE_NAME='result.tif'
ERROR = '[ERROR]'
INFO = '[INFO]'
WARN = '[WARN]'

## Dependends of .gitignore
RESULT_PATH = join(abspath('./tmp'), RESULT_FILE_NAME)
EXCLUDE_FILES = ['.gitkeep', RESULT_FILE_NAME]

# Env variables
EXCLUDE_NAMES = (getenv('EXCLUDE_NAMES') or '').split(',')
IMAGES_PATH = getenv('IMAGES_PATH')
EXCLUDE_FILES= EXCLUDE_FILES + EXCLUDE_NAMES
WIDTH = int(getenv('WIDTH')) or 1920
HEIGHT = int(getenv('HEIGHT')) or 1080

def read_images_dir(path: str):
  files: List[str] = []
  dir = []
  try:
   dir = listdir(path)
  except:
    print('[ERROR]', 'Failed to read images dir, check env variable IMAGES_PATH:' + IMAGES_PATH)
  for item in dir:
    full_path = join(path, item)
    if item in EXCLUDE_FILES:
      if item in EXCLUDE_NAMES:
        print(WARN, 'Excluded item:', full_path)
      continue
    if isfile(full_path):
      files.append(full_path)
    else:
      # Recursive
      for _item in read_images_dir(full_path):
        files.append(_item)
  print(INFO, 'Read directory:', path)
  return files

def get_max_sizes(length: int, shift: int):
  s_all = WIDTH * HEIGHT
  s_one = s_all / length
  width = int(s_one ** (0.5)) - shift
  height = width
  row_count = int(WIDTH / width)
  col_count = int(HEIGHT / height)
  if (row_count * col_count < length):
    # Recursive
    return get_max_sizes(length, shift + SHIFT_STEP)
  shift_x = int((WIDTH - width * row_count) / row_count)
  shift_y = int((HEIGHT - height * col_count) / col_count)
  res = (width, height, row_count, shift_x, shift_y)
  print(INFO, 'Items sizes (width, height, row_count, shift_x, shift_y):', res)
  return res


def create_tiff_from_images(src_path: str, dest_path: str):
  src_images = read_images_dir(src_path)
  (width, height, row_count, shift_x, shift_y) = get_max_sizes(len(src_images), 0)
  result = Image.new(size=(WIDTH, HEIGHT), mode='RGB')

  col = 0
  row = 1
  x = int(shift_x / 2)
  y = int(shift_y / 2)
  for item in src_images:
    if col < row_count:
      x = col * (width + shift_x) or int(shift_x / 2)
      col += 1
    else:
      x = int(shift_x / 2)
      col = 1

      y = row * (height + shift_y)
      row += 1
    
    img = Image.open(item)
    img = img.resize(size=(width, height))
    result.paste(img, (x,  y ))
  
  result.save(dest_path, format='TIFF')
  print(INFO, 'Result saved:', dest_path)

create_tiff_from_images(src_path=IMAGES_PATH, dest_path=RESULT_PATH)



