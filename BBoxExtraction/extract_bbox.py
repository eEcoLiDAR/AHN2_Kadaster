#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:29:52 2018

@author: elena
"""

import argparse
import pylas
from os import listdir
from os.path import isfile, join

def get_laz_bbox(path, fname):
    full_fname = join(path, fname)
    laz_file = pylas.open(full_fname);
    mins = laz_file.header.mins
    maxs = laz_file.header.maxs
    minX = mins[0] 
    minY = mins[1]
    maxX = maxs[0]
    maxY = maxs[1]
    
    return minX, minY, maxX, maxY
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fname', help='Single LAZ file name', type=str, default=argparse.SUPPRESS)
    parser.add_argument('-p', '--path', help='LAZ files path', type=str)
    
    #parser.parse_args()
    args = parser.parse_args()
    
    if "fname" in args:
        # explicit single file is specified
        BBox = get_laz_bbox(args.path,args.fname)    
        print("Bounding box ([minX minY maxX maxY]): ", BBox)
    else:
        # only path is specified => we want to computer all BBoxes
       files = [f for f in listdir(args.path) if isfile(join(args.path, f))] 
       for f in files:        
           BBox = get_laz_bbox(args.path,f)    
           print("Bounding box ([minX minY maxX maxY]): ", BBox)                  
    
if __name__ == '__main__':
    main()    