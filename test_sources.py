import logging, datetime, time, json
import os, shutil
from ast import literal_eval
from Clouds import CloudSource
logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-cloud-sources.log", 
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

IMAGE_ROOT_DIRECTORY = "images/test_images"

# Remove all old test images
for item in os.listdir(IMAGE_ROOT_DIRECTORY):
    targetPath = os.path.join(IMAGE_ROOT_DIRECTORY, item)
    if os.path.isdir(targetPath):
        shutil.rmtree(targetPath)
    else:
        os.remove(targetPath)

logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

# logging.info("LOAD SOURCES")
# with open("Clouds/CloudSourcesData.json", "r") as f:
#     cloudSourcesJSON = json.load(f)
# logging.info("LOAD SUCCESSFUL")

# logging.info("TEST SOURCES")
# for sourceJSON in cloudSourcesJSON["CloudSources"]:
#     logging.info("-"*80)
#     source = CloudSource.CloudSource(sourceJSON["name"], sourceJSON["url"], literal_eval(sourceJSON["crop_coords"]), "00:00")
#     logging.info(f"TESTING SOURCE {source.name} STARTED")
#     if source.get_image(directory="images/test_images"):
#         logging.info("GET SUCCESSFUL")
#     else:
#         logging.info("GET FAILED")
#     logging.info("-"*80)

# Map of names to urls to test
CLOUD_SOURCE_URLS = {
    "BridgemanTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_bridgeman.jpg",
    "TuahuTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_tuahu.jpg",
}
logging.info("TEST SOURCES")
for name, url in CLOUD_SOURCE_URLS.items():
    logging.info("-"*80)
    source = CloudSource.CloudSource(name, url, None, "00:00")
    logging.info(f"TESTING SOURCE {source.name} STARTED")
    if source.get_image(download_root_directory="images/test_images"):
        logging.info("GET SUCCESSFUL")
    else:
        logging.info("GET FAILED")
    logging.info("-"*80)


