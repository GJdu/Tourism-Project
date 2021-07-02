import sys
import cv2
import glob
import requests
import os
import numpy as np
import torch
import torchvision.models as models
from tensorflow import keras
from os import listdir,makedirs
from os.path import isfile,join
import matplotlib.pyplot as plt

PLACES_PATH = '/Users/brian/Documents/GitHub/instagram-filter-removal-pytorch'
sys.path.insert(1, PLACES_PATH)

from configs.default import get_cfg_defaults
from modeling.build import build_model
from utils.data_utils import linear_scaling

def setupFilterRemoval():
    if not os.path.exists("ifrnet.pth"):
        with open("ifrnet.pth", 'wb') as f:
            url = "https://www.dropbox.com/s/y97z812sxa1kvrg/ifrnet.pth?dl=1"
            r = requests.get(url, stream=True)
            for data in r:
                f.write(data)

    cfg = get_cfg_defaults()
    cfg.MODEL.CKPT = "ifrnet.pth"
    net, _ = build_model(cfg)
    net = net.eval()
    vgg16 = models.vgg16(pretrained=True).features.eval()

    return net, vgg16, cfg

def load_checkpoints_from_ckpt(net, ckpt_path):
    checkpoints = torch.load(ckpt_path, map_location=torch.device('cpu'))
    net.load_state_dict(checkpoints["ifr"])

# Only accept images of 256 * 256
def filterRemoval(net, vgg16, img):
    arr = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)
    arr = torch.tensor(arr).float() / 255
    arr = linear_scaling(arr)
    with torch.no_grad():
        feat = vgg16(arr)
        out, _ = net(arr, feat)
        out = torch.clamp(out, max=1., min=0.)
        return out.squeeze(0).permute(1, 2, 0).numpy()

path = '/Users/brian/ml/DetectSelfie/data/Selfie-Image-Detection-Dataset/Training_data_reduced/Selfie' # Source Folder
dstpath = '/Users/brian/ml/DetectSelfie/data/Selfie-Image-Detection-Dataset-No-Filter/Training_data/Selfie' # Destination Folder

try:
    makedirs(dstpath)
except:
    print ("Directory already exist, images will be written in same folder")
# Folder won't used
files = list(filter(lambda f: isfile(join(path,f)), listdir(path)))

net, vgg16, cfg = setupFilterRemoval()
load_checkpoints_from_ckpt(net, cfg.MODEL.CKPT)

for image in files:
    try:
        img = keras.preprocessing.image.load_img(os.path.join(path,image), target_size=(256, 256))
        img_no_filter = filterRemoval(net, vgg16, img)
        dstPath = join(dstpath,image)
        keras.preprocessing.image.save_img(dstPath, img_no_filter)
    except:
        print('{} is not converted')

for fil in glob.glob("*.jpg"):
    try:
        img = keras.preprocessing.image.load_img(fil, target_size=(256, 256))
        img_no_filter = filterRemoval(net, vgg16, img) # convert to greyscale
        keras.preprocessing.image.save_img(os.path.join(dstpath,fil), img_no_filter)
    except:
        print('{} is not converted')