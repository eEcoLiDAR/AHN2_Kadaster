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
import re

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

def get_supertile_fname(bbox_fname):
    """ funciton to generate the 'super' (kadaster) tile filename from here the AHN2 sub-tile (fname) came from.
        Image of this mapping should be available in the repository. Rules of mapping:
        Kadaster tiles have alpha numeric filename: with ddL, where d stands for digit 0..9(7) and L is a letter either W(est) or O(ost)
        Any such 'super' Kadaster tile is split in 2 qaudarnts named a, b, c and d for W and e, f, g and h for O.
        Each of these quadrats is split in 4 more- the upper (notherrn) 2 are denoted as nd, where n stands for Noord and d is a digit 1 or 2
        and lower (southern) 2 denoted as zd, where z stands for Zuid and d is 1 or 2. Each of these divisions corresponds to an ahn2 tile
        and each such tile is divided to 5x5 = 25 subtiles. We start with a name pf such sub-tile (in bbox_fname) and want to obtain 
        the corresponding 'super' kadaster tile. The information of the super tile is encoded in the first 3 characters after the first '_'/
        Examples: 
            ahn2_06an2_13, ahn2_06bz1_01 come from 06W 'super' tile
            ahn2_06fz2_08 and ahn2_06g25 comes from 06O 'super' tile
            
        inputs: 
            bbox_fname: the LAZ filename (only) with extension (.laz) of the file for which we calculated the BBox (AHN2 sub-tile)
        outputs:
            csvfname: the CSV filename (only) with extension .csv corresponding to the 'super' kadaster tile"""
            
    # get only the base name       
    bbox_base_fname, ext = splitext(bbox_fname)       
    # parse the base fname for '_' and take the second element       
    fname_parts = re.split(r"_",bbox_fname)
    mid_fname_part = fname_parts[1]
    numeric_part = mid_fname_part[0:2]
    east_or_west_part = mid_fname_part[2]
    east_or_west = ''
    if east_or_west_part in {'a','b','c','d'}:
        east_or_west = 'W'
    elif east_or_west_part in {'e','f','g','h'}:
        east_or_west = 'O'
        
    csvfname = numeric_part + east_or_west + '.csv'
     
     
    return csvfname    

def csv_header(csv_path, csv_fname):
    """ csv_header: function to write the header of the CSV file.
        inputs:
            csv_path: the path (only) to the CSV file
            csv_fname: the CSV filename (only) with extension .csv
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
    """ bbox2csv: function to write the bounding box of the point cloud (PC) data as a row in several CSV files.
        Each CSV file corresponds to a 'super' Kadaster tile (using TopNL data)
        The function appends rows to a file with already created header.
        inputs:
            csv_path: the path (only) to the CSV file
            csv_fname: the CSV filename (only) with extension .csv
            bbox_fname: the LAZ filename (only) with extension (.laz) of the file for which we calculated the BBox (AHN2 sub-tile)
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
    """ Main fucntion for the extract_bbox.py script. It takes LAZ file(s) as input and generated a CSV file containing
    the bounding box(es) of the file(s). It works in 2 modes- on single PC file or on multiple 
    PC files residing in the same directory. The command line arguments are:
        fname: the signle LAZ filename (only). By default it is supressed.
        path: the path to the LAZ file or files        
        csvpath: the path (only) where to store the generated CSV files. """
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fname', help='Single LAZ file name', type=str, default=argparse.SUPPRESS)
    parser.add_argument('-p', '--path', help='LAZ files path', type=str)    
    #parser.add_argument('-csvf', '--csvfname', help='CSV file name', type=str, default='bounding_boxes_geom.csv')
    parser.add_argument('-csvp', '--csvpath', help='CSV file path', type=str)
    
    # parse the input arguments arguments
    args = parser.parse_args()
    
   
                
    if "fname" in args:
        # explicit single file is specified
        # get the BBox
        BBox = get_laz_bbox(args.path,args.fname)
        print(args.fname)
        print("Bounding box ([minX minY maxX maxY]): ", BBox)  
        # generate the proper CSV file name referring to the 'super' Kadaster tile
        csvfname = get_supertile_fname(args.fname)
        print("CSVfname: ", csvfname)
        
        csv_header(args.csvpath,csvfname)
        bbox2csv(args.csvpath,csvfname, args.fname, BBox)
        print("Bounding box written to csv file.")
        
        
    else:
        # only path is specified => we want to computer all BBoxes       
       files = [f for f in listdir(args.path) if isfile(join(args.path, f))] 
       for f in files:        
           # get the BBox
           BBox = get_laz_bbox(args.path,f)
           print(f)
           print("Bounding box ([minX minY maxX maxY]): ", BBox) 
           
           # generate the proper CSV file name referring to the 'super' Kadaster tile
           csvfname = get_supertile_fname(f)
           
           # check if the CSV file already exist, then create a header, if not, just append to the existing file
           csvfname_full = join(args.csvpath, csvfname)
           if not isfile(csvfname_full):
               # create the CSV file and its header
               csv_header(args.csvpath,csvfname)
           
           # add content
           bbox2csv(args.csvpath,csvfname, f, BBox)
           print("Bounding box written to csv file.")    
    
if __name__ == '__main__':
    main()    