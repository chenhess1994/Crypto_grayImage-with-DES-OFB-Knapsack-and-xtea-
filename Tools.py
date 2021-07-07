# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 09:09:14 2021

@author: irago
"""
from PIL import Image 
import os
import numpy as np




def setPicFormat(pic_dst):
    if os.path.isfile(pic_dst):
        im = Image.open(pic_dst)
        im=im.convert("L")
        #im.show()
        return im
           # f, e = os.path.splitext(self.image_folder + "\\" + item)
           #imResize = im.resize(self.pic_size, Image.ANTIALIAS)
           #imResize.save(dst + "\\" + item)



#Extended Euclidean algorithms.
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y



#Inverting number in modular functions.
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None  #Modular inverse does not exist.
    else:
        return x % m
    