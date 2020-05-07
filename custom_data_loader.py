#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 16:41:27 2018

@author: xionghaipeng
"""

__author__='xhp'

'''load the dataset'''
#from __future__ import print_function, division
import os
import torch
from skimage import io, transform#
import numpy as np

from torch.utils.data import Dataset#, DataLoader#
import glob
import scipy.io as sio#use to import mat as dic,data is ndarray

import torch
import torch.nn.functional as F


# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

class customDataset(Dataset):

    def __init__(self, filelist, transform):
        self.filelist = filelist
        self.rgb = np.array([[[0.41595605, 0.37184307, 0.36015078]]]).reshape(1,1,3)
        self.transform = transform

    def __len__(self):
        return len(self.filelist)

    def __getitem__(self, idx):
        
        img_name =self.filelist[idx]
        image = io.imread(img_name) #load as numpy ndarray
        image = image/255. -self.rgb #to normalization,auto to change dtype
        #image = image.transpose((2,0,1))
        #image = torch.from_numpy(img)
        sample = {'image': image, 'name': img_name} 
        sample = self.transform(sample)
        sample['image'] = get_pad(sample['image'])

        return sample
    
    
######################################################################
class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, name = sample['image'], sample['name']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'name': name}


######################################################################
def get_pad(inputs,DIV=64):
    h,w = inputs.size()[-2:]
    ph,pw = (DIV-h%DIV),(DIV-w%DIV)
    # print(ph,pw)

    if (ph!=DIV) or (pw!=DIV):
        tmp_pad = [pw//2,pw-pw//2,ph//2,ph-ph//2]
        # print(tmp_pad)
        inputs = F.pad(inputs,tmp_pad)

    return inputs

if __name__ =='__main__':
    inputs = torch.ones(6,60,730,970);print('ori_input_size:',str(inputs.size()) )
    inputs = get_pad(inputs);print('pad_input_size:',str(inputs.size()) )
