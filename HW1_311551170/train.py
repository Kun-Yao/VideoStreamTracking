# -*- coding: utf-8 -*-
"""vs_assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t0tI_s0BNHDePZdp5_K7YHBqxymeTcSj
"""

import torch
from torch.utils import data
from torch.utils.data import DataLoader
from torch import optim
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import resize
import os
from torchsummary import summary



class SportLoader(data.Dataset):
    def __init__(self, mode, transform=None):
        self.mode = mode
        self.sport = pd.read_csv("D:/Lab1/" + self.mode + ".csv")
        self.img_name = self.sport['names']
        self.label = self.sport['label']
        self.transform=transform
    
    def __len__(self):
        return len(self.img_name)
    
    def __getitem__(self, index):
        image_path="D:/Lab1/" + self.mode + "/" + self.img_name[index]
        self.img = io.imread(image_path)
        self.img = resize(self.img, (3,224,224))
        self.img = self.img.astype('float32')/255.0
        self.target = self.label[index]
        
        if self.transform:
          self.img = self.transform(self.img)
        return self.img, self.target

train_dataset = SportLoader("train")
valid_dataset = SportLoader("val")

#batch_size可調
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=64, shuffle=True)


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


#train
def train(epoch):
    max_valid_acc = 0
    max_train_acc = 0
    model.train()
    for i in range(epoch):
        total_train_accuracy = 0
        total_train_loss = 0
        print("第{}輪訓練".format(i+1))
        for data in train_loader:
            imgs, targets = data
            if torch.cuda.is_available():
                imgs = imgs.cuda()
                targets = targets.cuda()
            outputs = model(imgs)
            loss = loss_fn(outputs, targets)
        
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
            total_train_loss = total_train_loss + loss.item()
            accuracy = (outputs.argmax(1) == targets).sum()
            total_train_accuracy += accuracy
      
        train_acc.append((total_train_accuracy/train_dataset.img_name.size).cpu().data.numpy())
        train_loss.append(total_train_loss/len(train_loader))
        
      
        total_eval_loss = 0
        total_eval_accuracy = 0
        model.eval()
        with torch.no_grad():
            for data in valid_loader:
                imgs, targets = data
                if torch.cuda.is_available():
                    imgs = imgs.cuda()
                    targets = targets.cuda()
                outputs = model(imgs)
                loss = loss_fn(outputs, targets)
                total_eval_loss = total_eval_loss + loss.item()
                accuracy = (outputs.argmax(1) == targets).sum()
                total_eval_accuracy += accuracy
        eval_acc.append((total_eval_accuracy/valid_dataset.img_name.size).cpu().data.numpy())
        eval_loss.append(total_eval_loss/len(valid_loader))
        
        print("valid acc: {}" .format(eval_acc[i]))
        if eval_acc[i] > max_valid_acc and eval_acc[i] > 0.55:
            torch.save(model, "C:/Users/Lin/Desktop/vs_assignment1/HW1_311551170.pt")
            max_valid_acc = eval_acc[i]
            print("model is saved")
            print("train acc: {}" .format(train_acc[i]))
            print("train loss: {}".format(train_loss[i]))
            print("valid loss: {}".format(eval_loss[i]))


model = Network()
number_of_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

if torch.cuda.is_available():
    model = model.cuda()
    summary(model, (3, 224, 224))
    print("Active on GPU")
else:
    print("Active on CPU")

loss_fn = nn.CrossEntropyLoss()
if torch.cuda.is_available():
    loss_fn = loss_fn.cuda()
learning_rate = 0.005
optimizer = optim.SGD(model.parameters(),lr=learning_rate)

train_acc = []
train_loss = []
eval_acc = []
eval_loss = []
epoch = 100
train(epoch)

def show_loss_curve():
    plt.figure(1)
    plt.xlim(1, epoch)
    plt.ylim(0, 3)
    plt.xlabel('epoch') 
    plt.ylabel('loss') 
    plt.title("Loss curve")
    
    plt.plot(train_loss, 'b-', label='train')
    plt.plot(eval_loss, 'y-', label='validation')
    plt.legend(loc='upper right')
    plt.savefig('C:/Users/Lin/Desktop/vs_assignment1/loss_curve.png')#儲存圖片

def show_accuracy_curve():
    plt.figure(2)  
    plt.xlim(1, epoch)
    plt.ylim(0, 1)
    plt.xlabel('epoch') 
    plt.ylabel('accuracy') 
    plt.title("Accuracy curve")
    
    plt.plot(train_acc, 'b-', label='train')
    plt.plot(eval_acc, 'y-', label='validation')
    plt.legend(loc='upper right')
    plt.savefig('C:/Users/Lin/Desktop/vs_assignment1/acc_curve.png')

show_loss_curve()
show_accuracy_curve()



