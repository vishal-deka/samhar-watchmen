# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 20:06:33 2018

@author: poppinace
"""

import torch.nn as nn
import torch
import torch.optim as optim
from torch.utils.data import  DataLoader
import torch.nn.functional as F
#from torchvision import models

import os
import numpy as np
from time import time

import math
import pandas as pd
import csv

from IOtools import txt_write 

from PIL import Image
from custom_data_loader import ToTensor    

def get_pad(inputs,DIV=64):
    h,w = inputs.size()[-2:]
    ph,pw = (DIV-h%DIV),(DIV-w%DIV)
    # print(ph,pw)

    if (ph!=DIV) or (pw!=DIV):
        tmp_pad = [pw//2,pw-pw//2,ph//2,ph-ph//2]
        # print(tmp_pad)
        inputs = F.pad(inputs,tmp_pad)

    return inputs

def test_phase(opt,net, loader):
    with torch.no_grad():
        net.eval()
        
        predictions = []
        for i, data in enumerate(loader):
          
          
          image = data['image']
          img_name = data['name']

          image = image.type(torch.float32)
        
        

          features = net(image)
          div_res = net.resample(features)
          merge_res = net.parse_merge(div_res)
          outputs = merge_res['div'+str(net.args['div_times'])]
          del merge_res
        
          pre =  round(float((outputs).sum()))
          
          predictions.append((img_name,pre))

    return predictions



    






 



