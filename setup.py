from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'A Python package to automate video uploads to Instagram at set intervals using web requests.'
LONG_DESCRIPTION = '''instaAutoUpload is a Python package that allows users to automate the process of uploading videos to Instagram at specified intervals. The package uses direct web requests to interact with Instagram's API, enabling users to upload videos seamlessly. instaAutoUpload can be customized to handle different scheduling options, video formats, and captions, making it easy to tailor the upload process to your needs. Whether you're managing a personal account or a business profile, this package simplifies the process of keeping your feed updated automatically, saving time and effort.'''

setup(
    name="insta-upload-py",
    version=VERSION,
    author="djalti",
    author_email="abdeldjalilselamnia@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['moviepy', 'opencv-python', 'pillow', 'requests', 'urllib'],
    keywords=['python', 'instagram', 'upload', 'requests', 'reels', 'pages', 'bot', 'automation'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)