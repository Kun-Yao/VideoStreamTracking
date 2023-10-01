# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 15:39:43 2022

@author: Lin
"""
import os
import pandas as pd
import torch
from torchvision import io
import torch.nn as nn

class Network(nn.Module):
    def __init__(self): #定義神經層
        super(Network, self).__init__()
        
        self.net = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=10, kernel_size=5, stride=1, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2,2),
                                 nn.BatchNorm2d(10),
                                 nn.Conv2d(in_channels=10, out_channels=20, kernel_size=5, stride=1, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2,2),
                                 nn.BatchNorm2d(20),
                                 nn.Conv2d(in_channels=20, out_channels=40, kernel_size=5, stride=1, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2,2),
                                 nn.BatchNorm2d(40),
                                 nn.Conv2d(in_channels=40, out_channels=80, kernel_size=3, stride=1, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2,2),
                                 nn.Conv2d(in_channels=80, out_channels=160, kernel_size=3, stride=1, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2,2),
                                 nn.Flatten(),
                                 nn.Linear(160*6*6, 10)
                                 )
      
    def forward(self, input): #串聯神經層
        output = self.net(input)
        return output


def predict():
    model = torch.load("C:/Users/Lin/Desktop/vs_assignment1/HW1_311551170.pt",  map_location=torch.device('cpu'))
    #model = model.cuda()
    
    model.eval()
    
    with torch.no_grad():
        for i in range(len(img_path)):
            img = io.read_image(path + "/" + img_path[i])
            img = torch.reshape(img, (1,3,224,224))
            img = img/255.0

            if torch.cuda.is_available():
                img = img.cuda()
            output = model(img)
            result['names'].append(img_path[i])
            index = output.cpu().data.numpy().argmax(1)[0]
            result['label'].append(index)


result = {'names':[], 'label':[]}

path = "D:/Lab1/test"
img_path = os.listdir(path)

predict()

result_df = pd.DataFrame(result)
result_df.to_csv("C:/Users/Lin/Desktop/vs_assignment1/HW1_311551170.csv")