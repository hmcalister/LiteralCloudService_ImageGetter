import wget
from PIL import Image
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def download(url):
    if os.path.exists("cloud.png"):
        os.remove("cloud.png")
    download = wget.download(url, "cloud.png")
    return download

def get(url):
    im = Image.open(download(url))
    print(im.size)
    im.show()
    return im

def crop(im, coords):
    im=im.crop(coords)
    im.show()