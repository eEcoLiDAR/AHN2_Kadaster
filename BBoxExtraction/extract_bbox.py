#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:29:52 2018

@author: elena
"""

import argparse
import pylas
from os import listdir
from os.path import isfile, join, splitext
import csv

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


def csv_header(csv_path, csv_fname):
    full_csv_fname = join(csv_path, csv_fname)
    
    with open(full_csv_fname, mode='w') as csv_file:
        fieldnames = ['name','geom']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ';')

        writer.writeheader()
        
    return
    
    
def bbox2csv(csv_path, csv_fname, bbox_fname, BBox):
    full_csv_fname = join(csv_path, csv_fname)
    bbox_base_fname, ext = splitext(bbox_fname)
    minX = BBox[0]
    minY = BBox[1]
    maxX = BBox[2]
    maxY = BBox[3]
    
    point1 = str(minX) + ' ' + str(minY)
    point2 = str(maxX) + ' ' + str(minY)
    point3 = str(maxX) + ' ' + str(maxY)
    point4 = str(minX) + ' ' + str(maxY)    
    point5 = point1

    geom_str = 'polygon(('+point1+', '+point2+', '+point3+ ', '+point4+ ', '+point5+'))';

    with open(full_csv_fname, mode='a') as csv_file:
        fieldnames = ['name','geom']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ';')
        writer.writerow({'name': bbox_base_fname, 'geom': geom_str})
        
    return 
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fname', help='Single LAZ file name', type=str, default=argparse.SUPPRESS)
    parser.add_argument('-p', '--path', help='LAZ files path', type=str)    
    parser.add_argument('-csvf', '--csvfname', help='CSV file name', type=str, default='bounding_boxes_geom.wkt')
    parser.add_argument('-csvp', '--csvpath', help='CSV file path', type=str)
    
    #parser.parse_args()
    args = parser.parse_args()
    
    csv_header(args.csvpath,args.csvfname)
    
    if "fname" in args:
        # explicit single file is specified
        BBox = get_laz_bbox(args.path,args.fname)
        print(args.fname)
        print("Bounding box ([minX minY maxX maxY]): ", BBox)        
        bbox2csv(args.csvpath,args.csvfname, args.fname, BBox)
        print("Bounding box written to csv file.")
        
    else:
        # only path is specified => we want to computer all BBoxes       
       files = [f for f in listdir(args.path) if isfile(join(args.path, f))] 
       for f in files:        
           BBox = get_laz_bbox(args.path,f)
           print(f)
           print("Bounding box ([minX minY maxX maxY]): ", BBox) 
           bbox2csv(args.csvpath,args.csvfname, f, BBox)
           print("Bounding box written to csv file.")    
    
if __name__ == '__main__':
    main()    