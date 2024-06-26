# Importing Image class from PIL module
import os
from pathlib import Path
import fire
from PIL import Image


def remove_padidng(path, dir):
    path = Path(path)
    dir = Path(dir)
    if path.is_dir():
        for p in path.glob("*"):
            remove_padidng(p, dir)
    elif path.is_file() and path.suffix in [".png", ".jpg"]:
        # Opens a image in RGB mode
        im = Image.open(path)
        width, height = im.size
        # Setting the points for cropped image
        left = 100
        top = 100
        right = width - 100
        bottom = height - 100
        # Cropped image of above dimension
        im1 = im.crop((left, top, right, bottom))
        if not dir.exists():
            dir.mkdir(parents=True)
        im1.save(os.path.join(dir,path.name))

if __name__=="__main__":
    fire.Fire(remove_padidng)