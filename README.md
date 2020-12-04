# search-and-upload-images

## Usage
```bash
git clone https://github.com/Yashkataria/search-and-upload-images.git
cd search-and-upload-images
pip install -r requirements.txt

# Add images (*.jpg) in upload/img/ folder

# Running this script generates image embeddings of all the images in upload/img/ folder
python offline.py

# Search and upload images on localhost:5000. After uploading images, run python offline.py again in another terminal window.
python server.py
```
