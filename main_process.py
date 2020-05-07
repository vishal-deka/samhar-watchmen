import torch.nn as nn
import torch
import torch.nn.functional as F
from torch.utils.data import  DataLoader
import torch.optim as optim
#from torchvision import models

import os
import numpy as np
from time import time

import math
import pandas as pd
import csv

from IOtools import txt_write

from Network.SDCNet import SDCNet_VGG16_classify
from predictor import test_phase
from custom_data_loader import ToTensor, customDataset
import sqlite3 as sql
import threading

def main(opt):

    num_workers = opt['num_workers']

    
    if opt['partition'] =='one_linear':
        label_indice = np.arange(opt['step'],opt['max_num']+opt['step']/2,opt['step'])
        add = np.array([1e-6])
        label_indice = np.concatenate( (add,label_indice) )
    elif opt['partition'] =='two_linear':
        label_indice = np.arange(opt['step'],opt['max_num']+opt['step']/2,opt['step'])
        add = np.array([1e-6,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45]) 
        label_indice = np.concatenate( (add,label_indice) )
    

    opt['label_indice'] = label_indice
    opt['class_num'] = label_indice.size+1

    # init networks
    
    label_indice = torch.Tensor(label_indice)
    class_num = len(label_indice)+1
    div_times = 2
    net = SDCNet_VGG16_classify(class_num,label_indice,psize=opt['psize'],\
        pstride = opt['pstride'],div_times=div_times,load_weights=True)

    # test the exist trained model
    mod_path='best_epoch.pth' 
    mod_path=os.path.join(opt['trained_model_path'],mod_path)

    if os.path.exists(mod_path):
        all_state_dict = torch.load(mod_path, map_location=torch.device('cpu'))
        net.load_state_dict(all_state_dict['net_state_dict'])

        batch_size = 32
        while(True):

          ## for deployment
          """
          f = open("globalQueue.txt", "r")
          l = f.read()
          f.close()
          l = l.split(",")

          f = open("globalQueue.txt", "w")
          f.write(','.join(l[32:]))
          f.close()
          """
          #workingset = l[:batch_size]

          ## for testing
          
          workingset = ['football_20200123-101548.jpg','street_20200402-123414.jpg']

          transformer = ToTensor()
          testset = customDataset(workingset, transform = transformer)
          loader = DataLoader(testset, shuffle=False, num_workers=num_workers)

          predictions = test_phase(opt, net, loader)
          print(predictions)
          x = threading.Thread(target=writer, args=(predictions,))
          x.start()
          """
          for i in workingset:
            prediction.append([i, test_phase(opt,net, i)])
          """
          print(predictions)
          break
    else:
      print("trained model does not exist, please download")
          

def writer(pred):
  conn = sql.connect('example.db')
  c = conn.cursor()
  for record in pred:
    name = record[0][0].split('_')
    cam_id = name[0]
    timestamp = name[1][:-4]
    print(cam_id, timestamp)
    count = record[1]

    ## for creating csv files
    """
    path = 'S-DCNet/pred_dir/'+cam_id+'.csv'

    if not os.path.exists(path):
      f = open(path, 'a+')
      f.write('timestamp,people_count\n')
      f.write(timestamp+','+ str(count) + '\n')
    else:
      f = open(path, 'a+')
      f.write(timestamp+','+ str(count) + '\n')
    f.close()
    """
    ## for real time database update
    ## database is already created with id, latitude and longitude of all cameras
    c.execute('UPDATE maindb set timestamp=?, count=? where id=?', (timestamp, count, cam_id))
    conn.commit()







