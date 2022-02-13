import logging
import datetime
import time
logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.date.today())}.log", 
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

from typing import List
import json
from time import sleep
from Clouds.CloudSource import CloudSource, get_cloud_sources


logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

logging.info("LOAD DATA")
data_file = open("Clouds/CloudSourcesData.json")
# cloud_data = data_file.readlines()
cloud_data = json.load(data_file)
data_file.close()
logging.info(cloud_data)
logging.info("DATA LOADED")
logging.info("-"*80)


def test_url_wget():
    logging.info("-"*80)
    cloud_sources:List[CloudSource] = get_cloud_sources()
    logging.debug(cloud_sources)
    logging.info("-"*80)

    for source in cloud_sources:
        logging.info(f"GET IMAGE FROM {source}")
        source.get_image()
    logging.info("TEST SUCCESS")
    logging.info("-"*80)

def test_time_wget():
    cloud_sources:List[CloudSource] = get_cloud_sources()
    logging.debug(cloud_sources)
    logging.info("-"*80)

    logging.info("GET TARGET TIMES")
    for source in cloud_sources:
        now = datetime.datetime.utcnow()
        logging.debug(f"{now=}")
        logging.debug(f"{source=}")
        source.set_target_time(now)

    logging.info("TARGET TIMES CREATED")
    logging.info("-"*80)
    logging.info("SORTING SOURCES")
    cloud_sources.sort(key = lambda x:x.target_time)
    logging.info("SOURCES SORTED")
    for source in cloud_sources:
        logging.info(f"{str(source):<50}{source.target_time}")

    logging.info("-"*80)

    logging.info("START GET FROM SOURCES")
    for source in cloud_sources:
        logging.info(f"{source=}")
        logging.info(f"CURRENT TIME (LOCAL): {datetime.datetime.now()}")
        logging.info(f"CURRENT TIME (UTC): {datetime.datetime.utcnow()}")
        now = datetime.datetime.utcnow()
        delta = source.target_time - now
        if delta.total_seconds() > 0:
            logging.info(f"SLEEPING FOR {delta.total_seconds()}s")
            logging.info(f"SLEEP FINISH SCHEDULED FOR (LOCAL): {datetime.datetime.now()+delta}")
            logging.info(f"SLEEP FINISH SCHEDULED FOR (UTC): {datetime.datetime.utcnow()+delta}")
            sleep(delta.total_seconds())
        else:
            logging.info(f"NO SLEEP NEEDED")
        logging.info(f"GET {str(source)}")
        source.get_image()
        logging.info("GET SUCCESSFUL")
        logging.info("-"*80)
    logging.info("GOT ALL SOURCES SUCCESSFULLY")
    logging.info("-"*80)