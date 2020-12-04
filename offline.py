from PIL import Image
from CNN_classifier import FeatureExtractor
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    CNN = FeatureExtractor()

    for img_path in sorted(Path("./uploads/img/").glob("*")):
        print(img_path)
        feature = CNN.extract(img=Image.open(img_path))
        feature_path = Path("./uploads/feature") / (img_path.stem + ".npy")  
        np.save(feature_path, feature)