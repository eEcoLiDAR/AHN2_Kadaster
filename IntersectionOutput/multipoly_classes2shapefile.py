#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:23:46 2018

@author: elena
"""
test = True # true for the artificial test case, for generig purpose, please, make False!

# imports
import argparse
import fiona
from shapely.geometry import Polygon, MultiPolygon, mapping
if test:
    from descartes.patch import PolygonPatch # for visualization
    from matplotlib import pyplot # for plots
from os.path import join, splitext

# functions
# visualization
if test:
    def plot_coords(ax, ob):
        """ plot_coords - plots a point (as circle) with the given coordinates
            inputs:
                ax - plot axes
                ob - coordinates with fields x and y
        """
        x, y = ob.xy
        ax.plot(x, y, 'o', color='#999999', zorder=1)
                
    def show_multipolygon(multipolygon, axis, show_coords, extent, color, alpha,
                          title):
        """ show_multipolygon - displayes a multipolygon with specified visualizaiton parameters
            inputs:
                multipolygon - the shapely multipolygon to display
                axis - the figure axis
                show_coords - Boolean wheerhter to show the multipolygon verticies or not
                extent - the extent of the figure canvas
                color - the color to display in
                alpha - the alpha
                title - title of the figure
        """
    
        for polygon in multipolygon:
            if show_coords:
                plot_coords(axis, polygon.exterior)
            patch = PolygonPatch(
                polygon, facecolor=color, edgecolor=color, alpha=alpha, zorder=2)
            axis.add_patch(patch)
    
        xmin, ymin, xmax, ymax = extent
        xrange = [xmin, xmax]
        yrange = [ymin, ymax]
        axis.set_xlim(*xrange)
        # axis.set_xticks(range(*xrange))
        axis.set_ylim(*yrange)
        # axis.set_yticks(range(*yrange))
        axis.set_aspect(1)
    
        axis.set_title(title)
    
        return axis


def save_multipoly_and_classes2shapefile(multipolygon, classes, shapefilename):
    """ save_mutlipoly_and classes2shapefile - saving the multipolygon and the containing polygon's classes to a shapefile
        inputs:
            multipolygon- the shapely multipolygon to save
            classes- list of the classes of each of the polygon (take care for the ones within a multipolygon!)
            shapefilename - the shape filename to store the multipolygon and all classes"""
    # define the shapefile schema
    schema = {
        'geometry': 'Polygon',
        'properties': {
            'class': 'int'
        },
    }

    # write to a shapefile with the Amersfoort CRS
    with fiona.open(shapefilename, 'w', 'ESRI Shapefile', schema, crs={'init': "epsg:28992"}) as file:
        for i, poly in enumerate(multipolygon, start=0):
            file.write({
                'geometry': mapping(poly),
                'properties': {
                    'class': classes[i]
                },
            })
            
    return


# Main
def main():
    """ main- script to load set of (multi)polygons and their respective kadaster classes and save it to a shape file.
        The script has a test and generic mode. In test mode- 6 simple generated shapes illustrate how the script works.
        argumets:
            fname - input filename containing list of (multi)polygons and their kadaster classes
            shapepath - the path of the output shapefile
    """
    if test: # test case
        # Define planar shapes by thier verticies
        a = [(2,6), (4,6), (4,9), (2,9), (2,6)]
        b = [(6,9), (7,6), (9,4),(9,8), (7,9),(6,9)]
        c = [(1,1), (5,1),(5,4),(3,4),(1,1)]
        d = [(6,1), (10,1),(7,3),(6,1)]
        e = [(4,12), (6, 15), (8, 13), (4, 12)]
        f = [(2,12), (3,14), (4, 13), (2,12)]

        # create test list containing polygons and multipolygons    
        poly_d = Polygon(d)       
        multi_abc = MultiPolygon([[a, []], [b, []] ,[c, []]])
        multi_ef = MultiPolygon([[e, []], [f, []]])
        multi_poly_list = [multi_abc, poly_d, multi_ef]
              
        classes = [4, 5, 4, 3, 3, 3]
        
        # filename
        shapefilename = 'simple_example_multipolygon.shp'
        
        # full filename
        path = '.'
        full_shapefilename = join(path, shapefilename)
        
    else:
        # argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fname', help='File name with polygons and their classes', type=str)
        parser.add_argument('-shpp', '--shapepath', help='Shape file path', type=str)
        
        # parse the input arguments arguments
        args = parser.parse_args()
        
        # construct the shapefilename from the input filename
        base_fname, ext = splitext(args.fname)
        shapefilename = base_fname + '.' + 'shp'
        full_shapefilename = join(args.shapepath, shapefilename)
        
        # TO DO!!! parse the file and extract the list of (multi)polygons and their classes
        multi_poly_list = []
        classes = []
        
    # create a multipolygon from all (multi)polygons in the input list
    multi = []
    for el in multi_poly_list: # for all (potential) multipolygons
        if el.geom_type == 'MultiPolygon':
            for p in el: # for all polygons in each (potential) multipolygon
                multi.append(p)
                #TO DO: take care of somehow exanding the classes from inside multipolygons
        elif el.geom_type == 'Polygon':
            multi.append(el) # just add a polygon
    
    multipoly = MultiPolygon(multi)
    
    print('Multipolygon is valid?: ', multipoly.is_valid)
    
    if test:
        # Visualization        
        ORANGE = '#FF6600'
        al = 0.8
        show_verticies = True
        extent = [0, 0, 11, 16] # format of extent is [xmin, ymin, xmax, ymax]
        
        # Display the multipolygon
        fig = pyplot.figure(1, dpi=90)
        ax = fig.add_subplot(111)
        
        show_multipolygon(multipoly, ax, show_verticies, extent, ORANGE, al, 'multipolygon')
        
        pyplot.show()
    
    # saving to shape file (!)
    save_multipoly_and_classes2shapefile(multipoly, classes, full_shapefilename)
    
    print("Please, check with a GIS weather this file contains a valid polygon! \n", full_shapefilename)

if __name__ == '__main__':
    main()        