import smtplib, ssl, os, logging, random, json
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

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
    password = email_data["app_password"]
    return sender_email, password

server_address = "smtp.gmail.com"
port = 465
context = ssl.create_default_context()
sender_email, password = get_sender_login()
SMTP_SERVER = smtplib.SMTP_SSL(server_address, port, context=context)
SMTP_SERVER.login(sender_email, password)

@dataclass
class Receiver:
    """
    A dataclass to hold information about a particular receiver
    """

    address: str
    random_message: bool
    attach_original_name: bool

def send_email(receiver_address:str, subject:str, body:str, image = None, server:smtplib.SMTP_SSL=SMTP_SERVER):
    """
    Send an email to the receiver address, handelling all the backend MIME interactions

    ---

    Params

    receiver_address : str
        The email address to send this email to

    subject : str
        The subject of the email to be sent

    body : str
        The body of the email to be sent

    image : str, optional (defaults to None)
        Path to an image to attach to this email
        If None, no image is attached

    server : smtplib.SMTP_SSL
        The email server to send the email via
        Should already be logged in

    ---

    Returns : Boolean
        True if email is sent successfully, False otherwise

    """
            
    logging.info("Connect to email server")
    logging.info("Starting MIME generation")
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_address

    msg.attach(MIMEText(body))

    if image is not None:
        logging.info(f"Accessing file {image=}")
        with open(image, 'rb') as f:
            img_data = f.read()
        logging.info(f"File {image=} successfully loaded")
        image_attachment = MIMEImage(img_data, name=os.path.basename(image))
        msg.attach(image_attachment)

    logging.info("MIME msg metadata loaded")        
    logging.info(f"Sending email to {receiver_address}")
    try:
        server.sendmail(sender_email, receiver_address, msg.as_string())
        logging.info("Email sent successfully")
        logging.info("-"*80)
        return True
    except Exception as e:
        logging.info(f"ERROR: An error occurred during emailing!")
        logging.info(f"{e=}")
        logging.info(f"{type(e)=}")
        logging.info("-"*80)
        return False
    
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
            send_email(admin_email, "Warning: Cloud Emails Running Out!", f"Only {len(images)} remain in directory!")    