# search-and-upload-images

## Overview
- Simple Platform for image hosting and image-based image searching using tensorflow and Flask.
- `offline.py`: This script generates image embeddings from all the uploaded images. It uses VGG16 model pretrained on Imagenet dataset and generates a (4096,) vector.
- `app.py`: This script runs a web-server. You can upload multiple images and search related images based on your image query.
- Tested on macOS 11.0.1

## Usage
```bash
git clone https://github.com/Yashkataria/search-and-upload-images.git
cd search-and-upload-images
pip install -r requirements.txt

# Add images (*.jpg) in upload/img/ folder

# Running this script generates image embeddings of all the images in upload/img/ folder
python offline.py

# Search and upload images on localhost:5000. After uploading images, run python offline.py again in another terminal window.
python app.py
```
## Improvements Needed
- The search operations is performed as a linear scan. It needs optimised approach.
- Currently only supports .jpg images. Support for other formats is required.
- Host on AWS or Azure.

## Note
- The deployment on Heroku doesnt work due to exceeded limit of slug size.
