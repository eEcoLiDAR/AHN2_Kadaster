#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:29:52 2018

@author: elena
"""

# imports

import argparse
import pylas
from os import listdir
from os.path import isfile, join, splitext
import csv

# functions

def get_laz_bbox(path, fname):
    """ get_laz_bbox: function to read the bounding box of the point cloud (PC) data from a LAZ file header.
        inputs:
            path: the path (only) to the LAZ file
            fname: the LAZ filename (only) with extension (.laz)
        outputs:
            minX - the minimum value of the X coordinate of all PC points
            minY - the minimum value of the Y coordinate of all PC points            
            maxX - the maximum value of the X coordinate of all PC points
            maxY - the maximum value of the Y coordinate of all PC points"""
            
    # open the LAZ file
    full_fname = join(path, fname)
    laz_file = pylas.open(full_fname);
    
    # get the info from the header
    mins = laz_file.header.mins
    maxs = laz_file.header.maxs
    
    # assign BBox limits to the outputs
    minX = mins[0] 
    minY = mins[1]
    maxX = maxs[0]
    maxY = maxs[1]
    
    return minX, minY, maxX, maxY


def csv_header(csv_path, csv_fname):
    """ csv_header: function to write the header of the CSV (.wkt) file.
        inputs:
            csv_path: the path (only) to the CSV file
            csv_fname: the CSV filename (only) with extension (.wkt)
        The fieldnames are hard-coded to be 'name' and 'geom' for the name of the PC tile and geometry.""" 
    
    # generate the full filename    
    full_csv_fname = join(csv_path, csv_fname)
   
    # define the header (fieldnames), format of the writer and write the header
    with open(full_csv_fname, mode='w') as csv_file:
        fieldnames = ['name','geom']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ';')

        writer.writeheader()
        
    return
    
    
def bbox2csv(csv_path, csv_fname, bbox_fname, BBox):
    """ bbox2csv: function to write the bounding box of the point cloud (PC) data as a row in a CSV file.
        The function appends rows to a file with already created header.
        inputs:
            csv_path: the path (only) to the CSV file
            csv_fname: the CSV filename (only) with extension (.wkt)
            bbox_fname: the LAZ filename (only) with extension (.laz) of the file for  which we calculated the BBox
        The format of the Bounding Box (BBox) is a tuplr:
            minX - the minimum value of the X coordinate of all PC points
            minY - the minimum value of the Y coordinate of all PC points            
            maxX - the maximum value of the X coordinate of all PC points
            maxY - the maximum value of the Y coordinate of all PC points"""
            
    # create CSV full file, get the base BBox filename        
    full_csv_fname = join(csv_path, csv_fname)
    bbox_base_fname, ext = splitext(bbox_fname)
    # get the limits of the BBox
    minX = BBox[0]
    minY = BBox[1]
    maxX = BBox[2]
    maxY = BBox[3]
    
    # contruct the point of th epolygon representing the BBox. The last (5th) point should overlap with the first point
    point1 = str(minX) + ' ' + str(minY)
    point2 = str(maxX) + ' ' + str(minY)
    point3 = str(maxX) + ' ' + str(maxY)
    point4 = str(minX) + ' ' + str(maxY)    
    point5 = point1

    # create a geometry string describing the polygon
    geom_str = 'polygon(('+point1+', '+point2+', '+point3+ ', '+point4+ ', '+point5+'))';

    # write the geomerey polygon as a row in the CSV file
    with open(full_csv_fname, mode='a') as csv_file:
        fieldnames = ['name','geom']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ';')
        writer.writerow({'name': bbox_base_fname, 'geom': geom_str})
        
    return 
 
 # main 
def main():
    """ Main fucntion for the extract_bbox.py script. It takes LAZ file(s) as input and generated a CSV (.wkt) file containing
    the bounding box(es) of the file(s). It works in 2 modes- on single PC file or on multiple 
    PC files residing in the same directory. The command line arguments are:
        fname: the signle LAZ filename (only). By default it is supressed.
        path: the path to the LAZ file or files
        csvfname: the CSV filename (only). If not specified the default is bounding_boxes_geom.wkt
        csvpath: the path (only) where to store the generated CSV file. """
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fname', help='Single LAZ file name', type=str, default=argparse.SUPPRESS)
    parser.add_argument('-p', '--path', help='LAZ files path', type=str)    
    parser.add_argument('-csvf', '--csvfname', help='CSV file name', type=str, default='bounding_boxes_geom.wkt')
    parser.add_argument('-csvp', '--csvpath', help='CSV file path', type=str)
    
    # parse the input arguments arguments
    args = parser.parse_args()
    
    # create the CSV file and itsheader
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