import smtplib, ssl, os, logging, random, datetime, json, time
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-email.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

@dataclass
class Receiver:
    """
    A dataclass to hold information about a particular receiver
    """

    address: str
    random_message: bool
    attach_original_name: bool


def get_admin_emails(email_data_file = "Emails/email_list.json"):
    """
    Get the admin addresses from the email data file

    ---

    Params

    email_data_file : Str, optional (defaults to "Emails/email_list.json")
        The location of the email data json file
    ---

    Returns : List[str]
        A list of email addresses of admins
    """
   
    logging.info("LOAD ADMIN ADDRESSES")
    data_file = open(email_data_file)
    email_data = json.load(data_file)
    data_file.close()
    admins = email_data["admins"]
    logging.info(admins)
    logging.info("ADMINS LOADED")
    return admins

def get_sender_login(data_json = "emails/login_data.json"):
    """
    Get the login details for the sender email account

    ---

    Params 

    data_json : Str
        The path to the json file containing the sender login data
        Organized by "sender_address" and "email_password"

    ---

    Returns : 2-tuple of strings 
        sender_email, password
    """

    # Get the email account data to log into server
    email_data_file = open(data_json)
    email_data = json.load(email_data_file)
    email_data_file.close() 
    sender_email = email_data["sender_address"]
    password = email_data["email_password"]
    return sender_email, password

def get_receivers(receiver_emails_file = "emails/email_list.json"):
    """
    Get all of the receiver email addresses to send emails to

    ---

    Params

    receiver_emails_file : Str
        The path to the file containing the receiver email addresses

    ---

    Returns : List[Receiver]
        A list of receiver data objects representing receivers
    """
    
    logging.info("LOAD RECEIVER ADDRESSES")
    data_file = open(receiver_emails_file)
    email_data = json.load(data_file)
    data_file.close()
    receivers = []
    for receiver_json in email_data["receivers"]:
        try:
            receivers.append(Receiver(
                receiver_json["address"], 
                bool(receiver_json["random_message"]),
                bool(receiver_json["attach_original_name"])))
        except Exception as e:
            logging.info(f"ERROR: {receiver_json} failed to parse into Receiver object")
            logging.debug(f"{e=}")
            logging.debug(f"{type(e)=}")

    logging.info(receivers)
    logging.info("RECEIVERS LOADED")
    return receivers

def get_message(message_list_file = "emails/message_list.txt"):
    """
    Get a random message from a file containing messages.

    Will be used to set the email body.

    ---

    Params

    message_list_file : Str
        The path to the file containing the messages

    ---

    Returns : Str
        A single string, one message from the message list file 
    """
    
    messages = []
    with open(message_list_file, "r") as f:
        messages = f.readlines()
    message = random.choice(messages)
    return message

def get_image(image_directory="images/email_images"):
    """
    Get a single random image from a folder

    ---

    Params

    image_directory : Str
        The path to the file containing the images to choose from

    ---

    Returns : (Str, Str)
        The path to the image chosen, and the original image name (without extension)
    """
    
    images = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]
    # I want this to fail if no images present, something has gone wrong!
    try:
        image = random.choice(images)
        orig_image_name = image
    except IndexError as e:
        logging.info("ERROR: No images to select from!")
        logging.debug(f"{e=}")
        logging.debug(f"{type(e)=}")
        exit(1)

    orig_path = os.path.join(image_directory, image)
    logging.info(f"Selected image {orig_path}")

    try:
        logging.info(f"Renaming {os.path.join(image_directory, image)} to {os.path.join(image_directory,'cloud.png')}")
        os.replace(orig_path, os.path.join(image_directory,"cloud.png"))
    except FileExistsError as e:
        logging.info(f"ERROR: Destination {os.path.join(image_directory,'cloud.png')} already exists!")
        logging.debug(f"{e=}")
        logging.debug(f"{type(e)=}")
        return orig_path, orig_image_name.split(".")[0]
    except Exception as e:
        logging.info("ERROR: An unexpected error occurred during image renaming!")
        logging.debug(f"{e=}")
        logging.debug(f"{type(e)=}")
        exit(1)

    return os.path.join(image_directory,'cloud.png'), orig_image_name.split(".")[0]

def delete_image(file_path):
    """
    Delete a file located at file_path, handeling errors.

    ---

    Params

    file_path : str
        The path to the file to remove

    ---

    Returns : Bool
        True if the file no longer exists after method call
        False otherwise
    """

    if os.path.exists(file_path):
        logging.debug(f"REMOVING FILE {file_path}")
        try:
            os.remove(file_path)
        except IsADirectoryError as e:
            logging.info(f"ERROR: {file_path} is a directory")
            logging.debug(f"{e=}")
            logging.debug(f"{type(e)=}")
            return False
        except OSError as e:
            logging.info(f"ERROR: {file_path} CANNOT BE REMOVED")
            logging.debug(f"{e=}")
            logging.debug(f"{type(e)=}")
            return False
        logging.info(f"FILE REMOVED")
        return True
    else:
        logging.debug(f"{file_path} DOES NOT EXIST! REMOVAL NOT NEEDED")
        return True

def check_images_remaining(image_directory="images/email_images"):
    """

    Check how many images remain in the directory, and sends an email to an admin if this is below a threshold

    ---

    Params
    
    image_directory : Str
        The path to the file containing the images to choose from
    """

    MIN_IMAGES = 3
    images = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]
    logging.info(f"{len(images)} remain in {image_directory}")
    if len(images)<=MIN_IMAGES:
        admins = get_admin_emails()
        for admin_email in admins:
            logging.info(f"Notifying admin {admin_email}")
            server = "smtp.gmail.com",
            port = 465
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                sender_email, password = get_sender_login()
                server.login(sender_email, password)
                msg = MIMEMultipart()
                msg['Subject'] = "Warning: Cloud Emails Running Out!"
                msg['From'] = sender_email
                msg['To'] = admin_email
                msg.attach(MIMEText(f"Only {len(images)} remain in directory!"))
                logging.info(f"Sending email to {admin_email}")
                server.sendmail(sender_email, admin_email, msg.as_string())
                logging.info("Email sent successfully")
                logging.info("-"*80)
    
def send_email():
    """
    Send an email to the list of email recipients, choosing a random message and image, then deleting that image to avoid duplicates
    """

    logging.info("Started email method...")

    server = "smtp.gmail.com",
    port = 465

    default_message = "Enjoy the clouds today!"
    receivers = get_receivers()
    img_file, location_info = get_image()
    logging.info(f"{img_file=}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        logging.info("Accessed email server...")
        logging.info("Logging into server with credentials...")
        sender_email, password = get_sender_login()
        server.login(sender_email, password)
        
        logging.info(f"Accessing file {img_file=}")
        with open(img_file, 'rb') as f:
            img_data = f.read()
        logging.info(f"File {img_file=} successfully loaded")
        
        logging.info("-"*80)

        for receiver in receivers:
            logging.info(f"RECEIVER: {receiver}")
            logging.info("Starting MIME generation")
            msg = MIMEMultipart()
            msg['Subject'] = "Wow! New cloud just dropped!"
            msg['From'] = sender_email
            msg['To'] = receiver.address
            message = ""
            logging.info("MIME msg metadata loaded")
            # If the receiver wants a random message
            if receiver.random_message:
                message += get_message()
                logging.info(f"{message=}")
            else:
                message += default_message
            # If the receiver wants the location information
            if receiver.attach_original_name:
                message+=f"\nToday's location: {location_info}"

            msg.attach(MIMEText(message))
            image = MIMEImage(img_data, name=os.path.basename(img_file))
            msg.attach(image)
            logging.info("MIME msg body loaded")

            logging.info(f"Sending email to {receiver.address}")
            server.sendmail(sender_email, receiver.address, msg.as_string())
            logging.info("Email sent successfully")
            logging.info("-"*80)

    logging.info("Deleting image")
    delete_image(img_file)
    logging.info("Image deleted")
    logging.info("EMAILING FINISHED")
    logging.info("*"*80)