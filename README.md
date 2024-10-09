# instaUploadPy

instaUploadPy is a Python package designed to automate video uploads to Instagram using web requests. This package allows you to schedule video uploads at a specified interval, making it ideal for users who want to keep their Instagram feed updated without manual intervention.

## Features

- **Automated Uploads**: Schedule and upload videos to Instagram automatically at set intervals.
- **Customizable Scheduling**: Set upload intervals based on your preference.
- **Web Requests**: Uses direct web requests to handle video uploads without relying on third-party apps.
- **Video and Caption Support**: Upload videos along with customizable captions.
- **Easy to Integrate**: Simple and flexible to integrate into any Python project.

## Installation

You can install instaAutoUpload via pip:

```bash
pip install insta-upload-py
```

## Example

Make sure to replace the placeholders with the correct values:

```python
from instaUploadPy import InstaUpload

# Define your variables
VIDEOS_PATH = 'path/to/your/videos'  # Replace with the path to the videos you want to upload
COOKIES = {'should be a json object'}  # Get your Instagram account cookies 
INTERVAL = 10  # Set the interval for posting (in minutes)

# Initialize InstaUpload with your Instagram cookies
insta_upload = InstaUpload(COOKIES)

# Schedule video uploads
insta_upload.startPosting(VIDEOS_PATH, INTERVAL)
```
