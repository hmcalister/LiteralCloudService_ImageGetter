import logging, datetime, time, json
import os, shutil, glob
from PIL import Image
from ast import literal_eval
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from Clouds import CloudSource


logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-cloud-sources.log", 
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

IMAGE_ROOT_DIRECTORY = "images/test_images"

# Map of names to urls to test
CLOUD_SOURCE_URLS = {
    "Kalbarri Australia": "https://mywebcams.com.au/WA/Kalbarri.php",
    "GearldtonNE Australia": "https://view.myairportcams.com/YGEL/showimagecamera1.php",
    "GearldtonSE Australia": "https://view.myairportcams.com/YGEL/showimagecamera4.php",
    "JurienHarbour Australia": "https://mywebcams.com.au/WA/JurienHarbour.php",
    "Lancelin Australia": "https://mywebcams.com.au/WA/Lancelin.php",
    "Swanbourne Australia": "https://mywebcams.com.au/WA/Swanbourne.php",
    "Freemantle Australia": "https://mywebcams.com.au/WA/Fremantle.php",
    "Bunbury Airport Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/Bunbury_Airport/Bunbury_Airport_340.jpg",
    "Augusta Australia": "https://view.myairportcams.com/YAUG/showimagecamera1.php",
    "Peaceful Australia": "https://mywebcams.com.au/WA/Peaceful.php",
    "AlbanyNE Western Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/009999/009999_225.jpg",
    "AlbanySW Western Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/009999/009999_045.jpg",
    "Esperance Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/009542/009542_225.jpg",
    "Jacinth Ambrosia Australia": "https://view.myairportcams.com/YJAC/showimagecamera1.php",
    "Ceduna Australia": "https://view.myairportcams.com/YCDU/showimagecamera1.php",
    "Cairns Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/031011/031011_180.jpg",
    "Archerfield Airport Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/040211/040211_225.jpg",
    "Gold Coast Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/040717/040717_360.jpg",
    "Toowomba Airport Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/041529/041529_045.jpg",
    "Narrandera Australia": "https://assets3.webcam.io/w/z5G0w9/latest_hd.jpg",
    "Wagga Wagga Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/072150/072150_135.jpg",
    "Hamilton East Mountains Australia": "https://view.myairportcams.com/YHML/eastmtn.php",
    "Warrnambool Australia": "https://view.myairportcams.com/YWBL/showimagecamera1.php",
    "Tintinara Australia": "https://view.myairportcams.com/OZTIA/showimagecamera1.php",
}

logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

# Remove all old test images
for item in os.listdir(IMAGE_ROOT_DIRECTORY):
    targetPath = os.path.join(IMAGE_ROOT_DIRECTORY, item)
    if os.path.isdir(targetPath):
        shutil.rmtree(targetPath)
    else:
        os.remove(targetPath)

NEW_SOURCES_JSON = {
    "Version": 2,
    "CloudSources":[],
}

for name, url in CLOUD_SOURCE_URLS.items():
    logging.info("-"*80)
    source = CloudSource.CloudSource(name, url, None, "00:00")
    logging.info(f"TESTING SOURCE {source.name} STARTED")
    if source.get_image(download_root_directory=IMAGE_ROOT_DIRECTORY, separate_by_source=False):
        logging.info("GET SUCCESSFUL")
    else:
        logging.info("GET FAILED")
    
    if source.get_image(download_root_directory=IMAGE_ROOT_DIRECTORY, separate_by_source=False):
        logging.info("GET SUCCESSFUL")
    else:
        logging.info("GET FAILED")
        continue

    new_crop_coords = []
    def click_callback(event):
        new_crop_coords.append(event.x)
        new_crop_coords.append(event.y)
        if len(new_crop_coords) >= 4:
            plt.close()

    imPath = os.path.join(IMAGE_ROOT_DIRECTORY, str(source))
    imPath = glob.glob(f"{imPath}.*")[0]
    imageData = Image.open(imPath)
    imageData.load()
    imageData = np.asarray(imageData, dtype="int32")

    fig = plt.figure(figsize=(12,8))
    fig.canvas.callbacks.connect('button_press_event', click_callback)
    plt.imshow(imageData)
    plt.show()

    crop_coords = f"({new_crop_coords[0]},{new_crop_coords[2]},{new_crop_coords[1]},{new_crop_coords[3]})"
    new_cloud_source = {
            "name": name,
            "url": url,
            "crop_coords": crop_coords,
            "time_list": ["00:00"]
    }
    NEW_SOURCES_JSON["CloudSources"].append(new_cloud_source)

    logging.info("-"*80)

with open("new_sources.json", "w") as f:
    json.dump(NEW_SOURCES_JSON, f)