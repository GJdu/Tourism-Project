import sys
import os
import cv2
import torch
import torch.nn.parallel
from PIL import Image

# Clone repo at https://github.com/JunjH/Revisiting_Single_Depth_Estimation
PLACES_PATH = '/Users/brian/Documents/GitHub/Revisiting_Single_Depth_Estimation'
sys.path.insert(1, PLACES_PATH)

from models import modules, net, resnet, densenet, senet
import numpy as np
import loaddata_demo as loaddata
import pdb

import matplotlib.image
import matplotlib.pyplot as plt

plt.set_cmap("gray")


def define_model(is_resnet, is_densenet, is_senet):
    if is_resnet:
        original_model = resnet.resnet50(pretrained=True)
        Encoder = modules.E_resnet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel=[256, 512, 1024, 2048])
    if is_densenet:
        original_model = densenet.densenet161(pretrained=True)
        Encoder = modules.E_densenet(original_model)
        model = net.model(Encoder, num_features=2208, block_channel=[192, 384, 1056, 2208])
    if is_senet:
        original_model = senet.senet154(pretrained='imagenet')
        Encoder = modules.E_senet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel=[256, 512, 1024, 2048])
    else:
        print("No model selected")
        model = None

    return model

def test(nyu2_loader, model):
    out = None
    for i, image in enumerate(nyu2_loader):
        image = torch.autograd.Variable(image, volatile=True)
        out = model(image)
    return out

def setupModels():
    model = define_model(is_resnet=False, is_densenet=False, is_senet=True)
    model = torch.nn.DataParallel(model)
    model.load_state_dict(torch.load('./pretrained_model/model_senet', map_location=torch.device('cpu')))
    model.eval()
    return model

def generateDepthMap(model, image_path):
    image = matplotlib.image.imread(image_path)
    size = np.shape(image)[1], np.shape(image)[0]
    output_path = os.path.splitext(image_path)[0] + '_depth_map' + os.path.splitext(image_path)[1]
    nyu2_loader = loaddata.readNyu2(image_path)
    out = test(nyu2_loader, model)
    img = out.view(out.size(2), out.size(3)).data.cpu().numpy()
    img = cv2.resize(img, dsize=size, interpolation=cv2.INTER_CUBIC)

    # Create visualisation depth map
    matplotlib.image.imsave(output_path, img)
    # image = Image.open(output_path)
    # image = image.resize(size, Image.ANTIALIAS)
    # image.save(output_path)

    return img

# model = setupModels()
# image_path = 'FOTOS-Sample/180430100_365117691585384_4844866814362487843_n.jpg'
# generateDepthMap(model=model, image_path=image_path)