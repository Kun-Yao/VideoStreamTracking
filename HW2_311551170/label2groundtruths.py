# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 22:15:22 2022

@author: Lin
"""
import os

path = './val_labels'
path2 = './Code/Original/Object-Detection-Metrics-master/groundtruths'
path3 = './Code/SE/Object-Detection-Metrics-master/groundtruths'
dirs = os.listdir(path)

for d in dirs:
    p = os.path.join(path, d)
    p2 = os.path.join(path2, d)
    p3 = os.path.join(path3, d)
    f = open(p, "r")
    ff = open(p2, "w")
    fff = open(p3, "w")
    for line in f.readlines():
        l = line.split()
        x0 = (float(l[1])*1920*2 - float(l[3])*1920)/2
        x1 = (float(l[1])*1920*2 + float(l[3])*1920)/2
        y0 = (float(l[2])*1080*2 - float(l[4])*1080)/2
        y1 = (float(l[2])*1080*2 + float(l[4])*1080)/2
        one_line = ('0', str(int(x0)), str(int(y0)), str(int(x1)), str(int(y1)))
        str_one_line = " ".join(one_line)
        ff.write(str(str_one_line) + '\n')
        fff.write(str(str_one_line) + '\n')
    f.close()
    ff.close()
    fff.close()