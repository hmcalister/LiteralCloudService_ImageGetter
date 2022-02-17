import smtplib, ssl, os, logging, random, datetime, json, time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

logging.Formatter.converter = time.gmtime
logging.basicConfig(filename=f"logs/{str(datetime.datetime.utcnow().date())}-email.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

ADMIN_EMAIL = "haydenmcalister49@gmail.com"

logging.info("-"*80)
logging.info("*"*80)
logging.info(f"SCRIPT START AT LOCAL {datetime.datetime.now()}")
logging.info(f"SCRIPT START AT UTC {datetime.datetime.utcnow()}")
logging.info("*"*80)
logging.info("-"*80)

def get_sender_login(data_json = "emails/email_data.json"):
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

def get_receiver_emails(receiver_emails_file = "emails/email_list.txt"):
    """
    Get all of the receiver email addresses to send emails to

    ---

    Params

    receiver_emails_file : Str
        The path to the file containing the receiver email addresses

    ---

    Returns : List[Str]
        A list of strings of the receiver email addresses
    """
    
    emails = []
    with open(receiver_emails_file, "r") as f:
        emails = f.readlines()
    return emails

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

    Returns : Str
        The path to the image chosen
    """
    
    images = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]
    # I want this to fail if no images present, something has gone wrong!
    try:
        image = random.choice(images)
    except IndexError as e:
        logging.info("ERROR: No images to select from!")
        logging.debug(f"{e=}")
        logging.debug(f"{type(e)=}")
        exit(1)
    return os.path.join(image_directory, image)

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
        logging.info(f"Notifying admin {ADMIN_EMAIL}")
        server = "smtp.gmail.com",
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            sender_email, password = get_sender_login()
            server.login(sender_email, password)
            msg = MIMEMultipart()
            msg['Subject'] = "Warning: Cloud Emails Running Out!"
            msg['From'] = sender_email
            msg['To'] = ADMIN_EMAIL
            msg.attach(MIMEText(f"Only {len(images)} remain in directory!"))
            logging.info(f"Sending email to {ADMIN_EMAIL}")
            server.sendmail(sender_email, ADMIN_EMAIL, msg.as_string())
            logging.info("Email sent successfully")
            logging.info("-"*80)
    
def send_email():
    """
    Send an email to the list of email recipients, choosing a random message and image, then deleting that image to avoid duplicates
    """

    logging.info("Started email method...")

    server = "smtp.gmail.com",
    port = 465

    receiver_emails = get_receiver_emails()
    message = get_message()
    logging.info(f"{message=}")
    img_file = get_image()
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

        for receiver_email in receiver_emails:
            logging.info(f"RECEIVER: {receiver_email}")
            logging.info("Starting MIME generation")
            msg = MIMEMultipart()
            msg['Subject'] = "Wow! New cloud just dropped!"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            logging.info("MIME msg metadata loaded")
            text = MIMEText(message)
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename(img_file))
            msg.attach(image)
            logging.info("MIME msg body loaded")

            logging.info(f"Sending email to {receiver_email}")
            server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("Email sent successfully")
            logging.info("-"*80)

    logging.info("Deleting image")
    delete_image(img_file)
    logging.info("Image deleted")
    logging.info("EMAILING FINISHED")
    logging.info("*"*80)