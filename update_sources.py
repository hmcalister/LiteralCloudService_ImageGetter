import logging, datetime, time, json
import os, shutil, glob
from PIL import Image
from ast import literal_eval
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np

from Clouds import CloudSource


logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-cloud-sources.log", 
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

IMAGE_ROOT_DIRECTORY = "images/test_images"

# Map of names to urls to test
CLOUD_SOURCE_URLS = {
    # "GearldtonNE Australia": "https://view.myairportcams.com/YGEL/showimagecamera1.php",
    # "GearldtonSE Australia": "https://view.myairportcams.com/YGEL/showimagecamera4.php",
    "Bunbury Airport Australia": "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/Bunbury_Airport/Bunbury_Airport_340.jpg",
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
    "Hobart-Australia": "https://hccapps.hobartcity.com.au/webcams/platform",
    "Bauang-Philippines": "https://admin.meteobridge.com/cam/57287b66aef052a0bb33df9e62f6ff05/camplus.jpg",
    "Stavrakia-Crete": "http://penteli.meteo.gr/stations/stavrakia/webcam.jpg",
    "MountShasta-USA": "https://sc.snowcrest.net/images/camera/snowcam-high000M.jpg",
    "BodegaBay-USA": "https://boonproducts.ucdavis.edu/dyn/Netcam/latest.jpg",
    "AliceSprings-Australia": "http://www.alice.skycam.net.au/CAM1/image.jpg",
    "Geraldton-Australia": "https://mywebcams.com.au/WA/Geraldton.php",
    "Guadalajara-Mexico": "http://www.webcamsdemexico.net/guadalajara1/live.jpg",
    "RevolutionMonument-Mexico": "https://webcamsdemexico.net/mexicodf7/live.jpg",
    "Victoria-Malta": "http://content.meteobridge.com/cam/56e447b3ef709bce2e6bee72b922b61a/camplus.jpg",
    "Alicante-Spain": "https://www.runekvinge.no/alicante/cam1.jpg",
    "Bulandshofoi-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/bulandshofdi_1.jpg",
    "Siglufjaroarvegur-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/siglufjardarvegur_1.jpg",
    "Bolungarvikurgong-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/bolungarvikurgong_1.jpg",
    "Blikdalsa-Iceland": "https://www.vegagerdin.is/vgdata/vefmyndavelar/blikdalsa_1.jpg",
    "PraiaDaVitoria-Portugal": "http://www.climaat.angra.uac.pt/weathercams/0012.jpg",
    "HampsteadHeath-UK": "http://nw3weather.co.uk/skycam.jpg",
    "Frankfurt-Germany": "https://www.mainhattan-webcam.de/live/frankfurt01_1920.JPG",
    "SanFrancisco-USA": "https://castrocam.net/img/castrocam.jpg",
    "Boulder-USA": "https://boulderflatironcam.com/bfc/bfcsc.jpg",
    "BridgemanTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_bridgeman.jpg",
    "TuahuTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_tuahu.jpg",
    "MidhirstTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_midhirst.jpg",
    "MangawheroTaranaki-NZ": "https://www.primo.nz/webcameras/snapshot_mangawhero.jpg",
    "AshburtonN-NZ": "https://view.myairportcams.com/NZSite1/showimagecamera1.php",
    "AshburtonW-NZ": "https://view.myairportcams.com/NZSite1/showimagecamera3.php",
    "Omarama-NZ": "https://public.aopa.nz/omarama.jpg",
    "Moutere-NZ": "https://public.aopa.nz/moutere.jpg",
    "Danseys-NZ": "https://public.aopa.nz/danseys.jpg",
    "DunedinHospital-NZ": "https://public.aopa.nz/dh1.jpg",
    "Balcutha-NZ": "https://public.aopa.nz/balclutha.jpg",
    "WanakaTarras-NZ": "https://public.aopa.nz/wanaka-tarras.jpg?dt=latest",
    "WanakaCardrona-NZ": "https://public.aopa.nz/wanaka-cardrona.jpg?dt=latest",
    "QueenstownCoronet-NZ": "https://public.aopa.nz/queenstown-coronet.jpg?dt=latest",
    "MtNicholasStation-NZ": "https://public.aopa.nz/mtnicqn.jpg",
    "Glenorchy-NZ": "https://public.aopa.nz/mtnicgy.jpg",
    "HarrisSaddle-NZ": "https://www.metdata.net.nz/doc/harris/cam3/image.php",
    "MacKinnonPass-NZ": "https://metdata.net.nz/doc/mackinnon/cam1/image.php",
    "MilfordSound-NZ": "https://metdata.net.nz/es/stanne/cam1/image.php",
    "StewartIsland-NZ": "https://www.sailsashore.co.nz/image/cam/snapshot1.jpg",
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

def processImage(name: str, source: str):
    def click_callback(event):
        new_crop_coords.append(int(event.xdata))
        new_crop_coords.append(int(event.ydata))
        if len(new_crop_coords) >= 4:
            plt.close()

    imPath = os.path.join(IMAGE_ROOT_DIRECTORY, str(source))
    imPath = glob.glob(f"{imPath}.*")[0]
    try:
        imageData = Image.open(imPath)
        imageData.load()
        imageDataArray = np.asarray(imageData, dtype="int32")
    except:
        logging.info(f"SOURCE {name} FAILED")
        return None

    while True:
        new_crop_coords = []
        try:
            fig = plt.figure(figsize=(12,8))
            fig.canvas.callbacks.connect('button_press_event', click_callback)
            plt.imshow(imageDataArray)
            plt.show()
        except:
            plt.close()
            logging.info(f"SOURCE {name} FAILED")
            return None

        left  = max(min(new_crop_coords[0], new_crop_coords[2]), 0)
        right = min(max(new_crop_coords[0], new_crop_coords[2]), imageData.size[0])
        upper = max(min(new_crop_coords[1], new_crop_coords[3]), 0)
        lower = min(max(new_crop_coords[1], new_crop_coords[3]), imageData.size[1])
        crop_coords = f"({left},{upper},{right},{lower})"
        logging.info(new_crop_coords)
        logging.info(crop_coords)
        new_cloud_source = {
                "name": name,
                "url": url,
                "crop_coords": crop_coords,
                "time_list": ["00:00"]
        }
        try:
            croppedIm = imageData.crop((left,upper,right,lower))
            plt.imshow(croppedIm)
            plt.show()
        except KeyboardInterrupt:
            plt.close()
            continue
        except Exception as e:
            plt.close()
            logging.info(e)
            logging.info(f"Cropping {crop_coords} Failed!")
            continue
        
        return new_cloud_source

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

    result = processImage(name, source)
    if result is not None:
        NEW_SOURCES_JSON["CloudSources"].append(result)
        

with open("new_sources.json", "w") as f:
    json.dump(NEW_SOURCES_JSON, f)