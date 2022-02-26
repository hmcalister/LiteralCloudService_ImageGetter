# Clouds
## Hayden McAlister 

---

A collection of python scripts and packages to get images of cloud from webcams around the world, then email clouds to a list of receivers.

Ethical use of this project includes getting consent from receivers before adding their email accounts to the mailing list, as well as spacing emails out to avoid spam.

This project uses the `smtplib` python library to send emails, meaning an email account must already be set up. Currently, I have a gmail account set up to email clouds, so the smtp server is set to the gmail web server. More information can be found below. 

---

## Running this project

To get the cloud images from webcams, use the `get_sources.py` script. Logs are output to the `logs` directory, but you can expect the script to take roughly 24 hours to finish. Webcams are scrapped at the times specified under `Clouds/CloudSourceData.json`. Notice that the simple call to `CloudSource.wget_sources()` uses all of the default directories, so if you want to use your own directory structure please note the source code of `CloudSource.wget_sources()` and pass the correct arguments to function calls.

To email clouds out, use the `main.py` script. Logs are again output to the `logs` directory. You should set up a cron job (or equivalent) to automate this, as well as prevent spam (by making the emails more consistent).

---

## Collecting the clouds

Under the `Clouds` directory you can find the scripts used to get images from webcams as well as the webcam information itself.

### CloudSourcesData.json

Webcam data was collected from various internet sites that offer free and open webcams. These sources are compiled into `Clouds/CloudSourcesData.json` file, which also hold information on the time of day to get images and the crop coordinates (the dimensions to crop the source image to, mainly to remove any watermarks or bars from the webcams). These were all found manually, and should be self explanatory enough to expand on in future if needed.

In order to expand this data later, a version number has been attached to the data. This version number can control the format of the data in future. Versions should be backwards compatible. Version 2.0 is defined below:

```
CloudSourcesData.json - Version: 2
{
    "Version": 1,
    "CloudSources": [
        {
            "name": String,
            "url": String,
            "crop_coords": String,
            "time_list": [String],
            "time_interval": [String]
        },
        ...
    ]
}

```

Where :
- `name` is a string representing the name of the webcam source (conventionally of the form "Region-Country")
- `url` is the publicly accessible url to `wget` to get an image from
- `crop_coords` is a string of the form `(a,b,c,d)` where a,b,c,d are integers that define the crop. This four-tuple is used directly by PIL.Image.crop, so ensure this form is met
- `time_list` is a list of strings, each string of the form "HH:MM" where HH is the hour in 24 hour time, and MM is the minutes, such that "HH:MM" form the 24 time to `wget` the source. This should be changed to account for the seasons changing sunrise and sunset times. Currently these are all relative to UTC, not system time.
- `time_interval` is a list of three strings exactly. The first string is the start time (defined exactly like the `time_list` string), which is the first time (inclusive) that the source is queried. The second string is the interval, which is added to the start time to get each time to get a new time. The third string is the end time (defined the same as the start time), which is the final time (inclusive) which terminates the source querying. For example, 
    
    `time_interval`: ["12:00", "01:30", "00:30"] 
    
    is equivalent to 

    `time_list`: ["12:00", "13:30", "15:00", "16:30", "18:00", "19:30", "21:00", "22:30", "00:00", "00:30"]

### CloudSource.py

The `CloudSource.py` file exposes the `CloudSource` class, which represents a single webcam and time of day to get an image. More information can be 
- The scraping is done by the [python wget](https://pypi.org/project/wget/) library, which functions like the bash `wget` command but is platform independent.
- The cropping of the image is done by the [Python Image Library](https://pillow.readthedocs.io/en/stable/) 

This file also has several useful methods, including:
- `get_cloud_sources`: Get all of the cloud sources specified in `CloudSourcesData.json`
- `archive_images`: Move all of the images from `images/current_downloads` to `images/{date}`, although this should not need to be called externally

See `pydocs/Clouds` for more detailed documentation.

## How to Use CloudSource

A script in the root directory called `wget_sources` is set up to handle getting all of the source images over the course of a day. Logging from this is sent to `logs/{date}-cloud-sources.log` and are fairly comprehensive. Most errors possible are handled and logged (as a single error could prevent future sources from resolving).

---

## Sending emails

To distribute the clouds, I have decided to use email. Emails are sent using an existing email account. The details of this account are kept in `Emails/login_data.json`.

### `Emails/login_data.json`

A simple json file to hold the login information for the sender email account. The email address and password are stored in plaintext, so for obvious reason consider removing this file from your git using `git update-index --skip-worktree Emails/login_data.json`

### `Emails/email_list.json`

This file details the list of receivers for cloud emails. This file also specifies a list of admin email addresses that are emailed if an error occurs (or if the email images need to be updated)

```
email_list.json - Version: 1
{
    "Version": 1,
    "admins": ["", ...],
    "receivers" : [
        {
            "address": "",
            "random_message": 1,
            "attach_original_name": 1
        },
        ...
    ]
}

```

Where :
- `admins` defines a list of email addresses of admins, which are emailed upon an error
- `receivers` defines a list of receivers for the emails.
  - `address` defines the email address of the receiver
  - `random_message` is a boolean (0 or 1) defining if this receiver wants a random message or the default message
  - `attach_original_name` is a boolean (0 or 1) defining if this receiver wants the original file name attached to the email (usually defining the date, time, and location of the image)

### EmailSender.py

This is where the magic happens! Using `smtplib` and `email.mime` cloud images are sent to receivers. Receivers are stored in `Receiver` dataclass objects, which also stores if that instance of the receiver wants a random message or the default, and if the instance wants the original name (all of which is derived from json file above).

A basic email sending method is offered (`send_email`) that abstracts the sending of an email to giving the receiver address, subject, body, and an optional image path. This uses the default SMTP server which is logged in to when this module is imported, so no need to connect to the SMTP server each time.

Please be aware that this means you will need to manually close the SMTP server at the end of your script, or rely on timeout.

See `pydocs/Emails` for more detailed documentation, and see `main.py` for an example of how this module can be used.

---

## Images

In this directory the images for the project are managed. To avoid unnecessary bloat, no images are stored in this repository (as per .gitignore) so the size is not vastly increased. Specifics on each subdirectory can be found under `images/README.md`