import cv2
import os
from typing import List

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

FPS_COUNT = 8
save_dir = "images/videos"

cloud_source_names = [
    "Hobart-Australia",
    "Bauang-Philippines",
    "Stavrakia-Crete",
    "Kalahari-Namibia",
    "AliceSprings-Australia",
    "NynganNW-Australia",
    "Geraldton-Australia",
    "Alexandra-NZ",
    "Guadalajara-Mexico",
    "RevolutionMonument-Mexico",
    "Frankfurt-Germany",
    "ChimneySouthTaranaki-NZ",
    "TuahuTaranaki-NZ",
    "MidhirstTaranaki-NZ"
]

image_root_dirs = ["images/images_archive/2022-02-27", "images/images_archive/2022-02-28"]



for cloud_source_name in cloud_source_names:
    video_name = f'{cloud_source_name}.mp4'
    video_path = os.path.join(save_dir, video_name)

    image_paths = []
    print(f"Generating {cloud_source_name}")
    for image_root_dir in image_root_dirs:
        print(f"Checking root dir {image_root_dir}")
        image_paths.extend(process_directory(image_root_dir, cloud_source_name))
    if len(image_paths)==0:
        print("No images found!")
        print("-"*80)
        continue
    image_paths.sort()
    frame = cv2.imread(image_paths[0])
    height, width, layers = frame.shape

    print(f"Creating video {video_name}...")
    try:
        video = cv2.VideoWriter(video_path, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=FPS_COUNT, frameSize=(width,height))

        for image in image_paths:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()
    except Exception as e:
        print(f"ERROR: {type(e)}, {e}")