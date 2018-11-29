#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:23:46 2018

@author: elena
"""

# imports
import fiona
from shapely.geometry import Polygon, MultiPolygon, mapping
#from descartes.patch import PolygonPatch # for visualization
#from matplotlib import pyplot # for plots
from os.path import join

# functions
# visualization
'''
def plot_coords(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, 'o', color='#999999', zorder=1)
            
def show_multipolygon(multipolygon, axis, show_coords, extent, color, alpha,
                      title):

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
'''

def save_multipoly_and_classes2shapefile(multipolygon, classes, shapefilename):
    """ Saving the multipolygons and their classes to a shapefile"""
    # define the shapefile schema
    # define the schema
    schema = {
        'geometry': 'Polygon',
        'properties': {
            'class': 'int'
        },
    }

    # write to a shapefile
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
    # Define planar shapes by thier verticies
    a = [(2,6), (4,6), (4,9), (2,9), (2,6)]
    b = [(6,9), (7,6), (9,4),(9,8), (7,9),(6,9)]
    c = [(1,1), (5,1),(5,4),(3,4),(1,1)]
    d = [(6,1), (10,1),(7,3),(6,1)]
    e = [(4,12), (6, 15), (8, 13), (4, 12)]
    f = [(2,12), (3,14), (4, 13), (2,12)]

    # multipolygon from coordinates
    # multipoly = MultiPolygon([[a, []], [b, []] ,[c, []], [d, []]])

    # convert shapes to polygons
    #poly_a = Polygon(a)
    #poly_b = Polygon(b)
    #poly_c = Polygon(c)
    poly_d = Polygon(d)
    
    # multipolygon from polygons
    #multi = []
    #multi.append(poly_a)
    #multi.append(poly_b)
    #multi.append(poly_c)
    #multi.append(poly_d)
    #multipoly = MultiPolygon(multi)
    
     # multipolygon from collections of polygons and multipolygons
    all_multi = []
    multi_abc = MultiPolygon([[a, []], [b, []] ,[c, []]])
    multi_ef = MultiPolygon([[e, []], [f, []]])
    for p in multi_abc:
        all_multi.append(p)
    all_multi.append(poly_d)
    for p in multi_ef:
        all_multi.append(p)

    multipoly = MultiPolygon(all_multi)

    print('Multipolygon is valid?: ', multipoly.is_valid)
    
    # Visualization parameters
    '''
    ORANGE = '#FF6600'
    al = 0.8
    show_verticies = True
    extent = [0, 0, 11, 16] # format of extent is [xmin, ymin, xmax, ymax]
    
    # Display the multipolygon
    fig = pyplot.figure(1, dpi=90)
    ax = fig.add_subplot(111)
    
    show_multipolygon(multipoly, ax, show_verticies, extent, ORANGE, al, 'multipolygon')
    
    pyplot.show()
    '''
    classes = [4, 5, 4, 3, 3, 3]
    
    # filename
    ext = 'shp'
    fname = 'simple_example_multipolygon' + '.' + ext
    
    # full filename
    path = '.'
    shapefname = join(path, fname)
    
    # saving to shape file (!)
    save_multipoly_and_classes2shapefile(multipoly, classes, shapefname)

    print("Please, check with a GIS weather this file contains a valid polygon! \n", shapefname)
if __name__ == '__main__':
    main()        