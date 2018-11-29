#!/usr/bin/env python

import psycopg2
from read_config import config
import numpy as np
import pandas as pd
 
def get_intersections_from_db(db_name='', save_output=False):
    """ Connects to the PostGIS database server """
    conn = None
    try:
        # read PostGIS connection parameters
        params = config()

        # connect to db_name and ignore config file
        if db_name != '':
            params['database'] = db_name
        print('Database:', db_name)

        # connect to the POSTGIS server
        print('Connecting to the POSTGIS database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()

        geo_item_classes = [ 'gebouw', 'inrichtingselement','terrein', 'waterdeel', 
                         'geografischGebied', 'functioneelGebied', 'plaats', 
                         'registratiefGebied', 'hoogte', 'relief', 'wegdeel']

        # create an empty dataframe to store the data from all classes
        tile_instersections = pd.DataFrame()

        # loop over list of classes
        for geo_class_id, geo_class_name in enumerate(geo_item_classes):
            geo_class_id += 1 # class id starts from 1

            # run SQL statement to get instersections
            print('\nChecking the intersections for ', geo_class_name)
            cur.execute('''
                SELECT 
                    bboxes.ogc_fid, bboxes.name, 
                    {0}.ogc_fid AS {0}_ogc_fid, {0}.lokaalid AS {0}_lokaalid, 
                    ST_INTERSECTION(bboxes.wkb_geometry, {0}.wkb_geometry),
                    ST_AsText(ST_INTERSECTION(bboxes.wkb_geometry, {0}.wkb_geometry)),
                    ST_GeometryType(ST_INTERSECTION(bboxes.wkb_geometry, {0}.wkb_geometry))
                FROM bboxes, {0}
                WHERE (ST_GeometryType({0}.wkb_geometry) = 'ST_Polygon' AND ST_Intersects(bboxes.wkb_geometry, {0}.wkb_geometry) AND bboxes.ogc_fid > 0)
                GROUP BY bboxes.ogc_fid, {0}.ogc_fid
            '''.format(geo_class_name))
    
            # create a new dataframe for the class
            tempDF = pd.DataFrame(cur.fetchall())
            tempDF['class'] = pd.Series(geo_class_name, index=tempDF.index)
            tempDF['class_id'] = pd.Series(geo_class_id, index=tempDF.index)
            tile_instersections = tile_instersections.append(tempDF) # add class to the main file

        # set column names
        tile_instersections.columns = ["bbox_ogc_fid", "name", "ogc_fid", "lokaalid", "wkb_intersect", "wkt_intersect", "postgis_geometry_type", "class", "class_id"]

        # close the communication with the POSTGIS
        cur.close()

        # save the data if requested
        if save_output:
            np.save('{0}_intersections.npy'.format(db_name), tile_instersections)
            tile_instersections.to_pickle('{0}_intersections.pkl'.format(db_name))

        return tile_instersections


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('POSTGIS connection closed.')
 
 
if __name__ == '__main__':

    intersections_Tile02O = get_intersections_from_db(db_name='Tile02O', save_output=True)
    print(intersections_Tile02O.head())

    # intersections_Tile06O = get_intersections_from_db(db_name='Tile06O', save_output=True)
    # print(intersections_Tile06O.head())
