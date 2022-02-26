# `images` subdirectories
I cannot be sure if python will automatically create these directories for you. Before running this script (or, after getting an error more likely) please create the following directories:

## `current_downloads`
The directory for a process to save images from a current run of downloads to. New images are added to this directory before being archived

## `images_archive`
The directory to hold all images, sorted into subdirectories by date. Images are moved here once all images for a day are collected. Subdirectory dates are dated by UTC finish time.

## `email_images`
A directory to hold all of the images that can be emailed out. Images here are selected at random once per day, emailed, then deleted. A warning is sent to the admin if this folder is nearly empty. If empty, no email is sent and the email script crashes.

## `gifs`
Used as the default folder to save gifs to when using the `make_gifs.py` script in the root directory of this repo. Gifs generated are saved here