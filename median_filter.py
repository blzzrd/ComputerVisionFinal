#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:24:59 2020

@author: reneewu
"""

import numpy as np

def median_filter(seq,n):
    '''
    Median filter method for background subtraction.
    
    ARGS:
        seq - The sequence of image frames
        n - a parameter for the number of frames
    
    RETURNS:
        An numpy array that outputs the image of the background
    '''
    
    if n <= 0:
        print('Error, level must be a positive, nonzero number')
        return None
    
    s = np.random.choice(len(seq), n, replace=True)
    
    img = []
    
        
    h,w,_ = seq[0].shape
    
    result = np.zeros([h,w])
    
    for y in range(h):
        for x in range(w):
            img = []
            for i in range(n):
                img.append(seq[s[i]][y][x])
            result[y][x] = np.median(img,axis = 0)
    
    return(result)
            