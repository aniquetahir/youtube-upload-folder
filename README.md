# Introduction
YouTube has a very restrictive limit for uploading files using its API. 
The objective of this script is to upload all the files in a folder on YouTube using the web api
(which has almost no restrictions).

# Prerequisites
Please make sure geckodriver is installed. Firefox should also be available in the path

# Installation
```
pip install -r requirements.txt
apt install ffmpeg
```

# Running
```
python3 main.py <folder location> <name of firefox profile where channel is logged in>
```

# Folder Structure
Example of folder structure that the script processes:

```
.
├── a
│   ├── 1.mp4
│   └── 2.mp4
└── b
    ├── 3.mp4
    └── 4.mp4

```

Videos in each folder are merged together using ffmpeg and uploaded as a.mp4 and b.mp4
**Finally, after the upload is finished the originals are deleted**
