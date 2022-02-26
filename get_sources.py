import logging, datetime, time

logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-cloud-sources.log", 
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

from Clouds import CloudSource

logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

logging.info("LOAD SOURCES")
cloud_sources = CloudSource.get_cloud_sources()
logging.info("LOAD SUCCESSFUL")
logging.debug(cloud_sources)
logging.info("-"*80)

# logging.info("GET TARGET TIMES")
# for source in cloud_sources:
#     now = datetime.datetime.utcnow()
#     logging.debug(f"{now=}")
#     logging.debug(f"{source=}")
#     source.set_target_time(now)

# logging.info("TARGET TIMES CREATED")
# logging.info("-"*80)

logging.info("SORTING SOURCES")
cloud_sources.sort(key = lambda x:x.target_time)
logging.info("SOURCES SORTED")
for source in cloud_sources:
    logging.info(f"{str(source):<50}{source.target_time}")

logging.info("-"*80)
logging.info(f"TOTAL OF {len(cloud_sources)} SOURCES")
logging.info("-"*80)

logging.info("START GET FROM SOURCES")
try:
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
            time.sleep(delta.total_seconds())
        else:
            logging.info(f"NO SLEEP NEEDED")
        logging.info(f"GET {str(source)}")
        if source.get_image():
            logging.info("GET SUCCESSFUL")
        else:
            logging.info("GET FAILED")
        logging.info("-"*80)
    logging.info("ALL SOURCES GET FINISHED")
    logging.info("-"*80)
except KeyboardInterrupt:
    logging.info("*"*80)
    logging.info("KEYBOARD INTERRUPT")
    logging.info("ARCHIVE CURRENT IMAGES")
    logging.info("*"*80)
logging.info("MOVE IMAGES TO BACKUP FOLDER")
CloudSource.archive_images()
logging.info("-"*80)