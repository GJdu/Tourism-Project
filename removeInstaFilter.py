import sys

PLACES_PATH = '/Users/brian/Documents/GitHub/instagram-filter-removal-pytorch'
sys.path.insert(1, PLACES_PATH)

import requests
import os
import numpy as np
import torch
import torchvision.models as models
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

def filterRemoval(net, vgg16, img):
    arr = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)
    arr = torch.tensor(arr).float() / 255
    arr = linear_scaling(arr)
    with torch.no_grad():
        feat = vgg16(arr)
        out, _ = net(arr, feat)
        out = torch.clamp(out, max=1., min=0.)
        return out.squeeze(0).permute(1, 2, 0).numpy()

# Test remove instagram filter
from tensorflow import keras
img = keras.preprocessing.image.load_img("/Users/brian/Desktop/Screen Shot 2021-06-27 at 11.12.17 am.png", target_size=(256,256))
net, vgg16, cfg = setupFilterRemoval()
load_checkpoints_from_ckpt(net, cfg.MODEL.CKPT)
img = filterRemoval(net, vgg16, img)

# Show Test
import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()