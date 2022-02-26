from typing import List
from PIL import Image
import datetime
import os

cloud_source_name = "AliceSprings-Australia"
image_root_dir = "images/images_archive"
save_dir = "images/gifs"

image_paths = []

def process_directory(directory:str, target_substring:str, recurse:bool=True) -> List[str]:
    """
    Given a directory, look over each item in that directory and add that item if it contains the target_substring.
    Effectively finds all files thats name contains the target_substring. Note this will only find regular files.
    If recurse is True then this method will be called on any subdirectories found.

    ---
    Params

    directory : str
        The root directory to start searching from.

    target_substring : str
        The substring that must be contained in a files name, not the path to that file

    recurse : boolean, optional, defaults to True
        Boolean to recursively call this method on any subdirectories found

    ---
    Returns : List[str]
        A list of paths to files in the directory tree that contain the target substring in their name. 
        List may be unsorted, as os.listdir may return files in an arbitrary order.
    """

    directory_contents = os.listdir(directory)
    results = []

    for item in directory_contents:
        path = os.path.join(directory, item)
        if os.path.isdir(path) and recurse:
            subdirectory_results = process_directory(path, target_substring)
            results.extend(subdirectory_results)
        if os.path.isfile(path):
            if item.find(target_substring)!=-1:
                results.append(path)

    return results

x=process_directory(image_root_dir, cloud_source_name)
imgs = (Image.open(f) for f in x)
img = next(imgs)
img.save(fp=os.path.join(save_dir, f"{datetime.datetime.utcnow().date()} {cloud_source_name}.gif"),
    format="GIF", append_images=imgs, save_all=True, duration=100, loop=0)