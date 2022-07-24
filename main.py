import logging, datetime, time, smtplib

logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-email.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

from Emails import EmailSender


logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

logging.info("Started email method...")

default_message = "Enjoy the clouds today!"
receivers = EmailSender.get_receivers()
img_file, location_info = EmailSender.get_image()
logging.info(f"{img_file=}")

    
logging.info(f"Accessing file {img_file=}")
with open(img_file, 'rb') as f:
    img_data = f.read()
logging.info(f"File {img_file=} successfully loaded")

logging.info("-"*80)

for receiver in receivers:
    logging.info(f"RECEIVER: {receiver}")

    message = ""        
    # If the receiver wants a random message
    if receiver.random_message:
        message += EmailSender.get_message()
        logging.info(f"{message=}")
    else:
        message += default_message

    # If the receiver wants the location information
    if receiver.attach_original_name:
        message+=f"\n{location_info}"

    EmailSender.send_email(receiver.address, "Wow! New clouds just dropped!", message, img_file)

logging.info("Deleting image")
EmailSender.delete_image(img_file)
logging.info("Image deleted")
logging.info("EMAILING FINISHED")
logging.info("*"*80)

EmailSender.check_images_remaining()

logging.info("Quitting the SMTP server")
try:
    EmailSender.SMTP_SERVER.quit()
    logging.info("Session closed")
except smtplib.SMTPServerDisconnected as e:
    logging.info("Session already disconnected")
logging.info("-"*80)