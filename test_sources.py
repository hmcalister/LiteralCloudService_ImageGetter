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
#     if source.get_image(directory=IMAGE_ROOT_DIRECTORY):
#         logging.info("GET SUCCESSFUL")
#     else:
#         logging.info("GET FAILED")
#     logging.info("-"*80)

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
logging.info("TEST SOURCES")
for name, url in CLOUD_SOURCE_URLS.items():
    logging.info("-"*80)
    source = CloudSource.CloudSource(name, url, None, "00:00")
    logging.info(f"TESTING SOURCE {source.name} STARTED")
    if source.get_image(download_root_directory=IMAGE_ROOT_DIRECTORY):
        logging.info("GET SUCCESSFUL")
    else:
        logging.info("GET FAILED")
    logging.info("-"*80)


