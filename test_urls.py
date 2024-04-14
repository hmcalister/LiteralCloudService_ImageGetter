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

# Map of names to urls to test
CLOUD_SOURCE_URLS = {
    #  "Hobart-Australia": "https://hccapps.hobartcity.com.au/webcams/platform",
    #  "Bauang-Philippines": "https://admin.meteobridge.com/cam/57287b66aef052a0bb33df9e62f6ff05/camplus.jpg",
    #  "Stavrakia-Crete": "http://penteli.meteo.gr/stations/stavrakia/webcam.jpg",
    #  "Regina-Canada": "http://users.accesscomm.ca/saskweather/webcam/webcam32.jpg",
    #  "MountShasta-USA": "https://sc.snowcrest.net/images/camera/snowcam-high000M.jpg",
    #  "BodegaBay-USA": "https://boonproducts.ucdavis.edu/dyn/Netcam/latest.jpg",
    #  "AliceSprings-Australia": "http://www.alice.skycam.net.au/CAM1/image.jpg",
    #  "Geraldton-Australia": "https://mywebcams.com.au/WA/Geraldton.php",
    #  "Guadalajara-Mexico": "http://www.webcamsdemexico.net/guadalajara1/live.jpg",
    #  "RevolutionMonument-Mexico": "https://webcamsdemexico.net/mexicodf7/live.jpg",
    #  "Victoria-Malta": "http://content.meteobridge.com/cam/56e447b3ef709bce2e6bee72b922b61a/camplus.jpg",
    #  "Alicante-Spain": "https://www.runekvinge.no/alicante/cam1.jpg",
    #  "Bulandshofoi-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/bulandshofdi_1.jpg",
    #  "Siglufjaroarvegur-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/siglufjardarvegur_1.jpg",
    #  "Bolungarvikurgong-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/bolungarvikurgong_1.jpg",
    #  "Blikdalsa-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/blikdalsa_1.jpg",
     "PraiaDaVitoria-Portugal": "http://www.climaat.angra.uac.pt/weathercams/0012.jpg",
     "HampsteadHeath-UK": "http://nw3weather.co.uk/skycam.jpg",
     "Frankfurt-Germany": "https://www.mainhattan-webcam.de/live/frankfurt01_1920.JPG",
     "SanFrancisco-USA": "https://castrocam.net/img/castrocam.jpg",
     "Boulder-USA": "https://boulderflatironcam.com/bfc/bfcsc.jpg",
     "BridgemanTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_bridgeman.jpg",
     "TuahuTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_tuahu.jpg",
     "MidhirstTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_midhirst.jpg",
     "MangawheroTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_mangawhero.jpg",
     "Dunedin-NZ": "https://www.physics.otago.ac.nz/eman/weather_station/weather_data/lemcam4.jpg",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
    # "": "",
}
logging.info("TEST SOURCES")
for name, url in CLOUD_SOURCE_URLS.items():
    logging.info("-"*80)
    source = CloudSource.CloudSource(name, url, None, "00:00")
    logging.info(f"TESTING SOURCE {source.name} STARTED")
    if source.get_image(download_root_directory=IMAGE_ROOT_DIRECTORY, separate_by_source=False):
        logging.info("GET SUCCESSFUL")
    else:
        logging.info("GET FAILED")
    logging.info("-"*80)
