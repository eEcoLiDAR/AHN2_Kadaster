#!/usr/bin/env python

import psycopg2
from read_config import config
import pandas as pd
 
def get_intersections_from_db(db_name=''):
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
        
        # run SQL statement to get instersections
        print('Checking the intersections:')
        cur.execute('''
            SELECT bboxes.ogc_fid, bboxes.name, waterdeel.ogc_fid AS waterdeel_ogc_fid, waterdeel.lokaalid AS waterdeel_lokaalid, ST_INTERSECTION(bboxes.wkb_geometry, waterdeel.wkb_geometry), ST_GeometryType(ST_INTERSECTION(bboxes.wkb_geometry, waterdeel.wkb_geometry))
            FROM bboxes, waterdeel
            WHERE (ST_GeometryType(waterdeel.wkb_geometry) = 'ST_Polygon' AND ST_Intersects(bboxes.wkb_geometry, waterdeel.wkb_geometry) AND bboxes.ogc_fid > 1)
            GROUP BY bboxes.ogc_fid, waterdeel.ogc_fid
        ''')
 
        # display the POSTGIS database server version
        tile_instersections = pd.DataFrame(cur.fetchall())
        tile_instersections.columns = ["ogc_fid", "name", "waterdeel_ogc_fid", "waterdeel_lokaalid", "geometry", "geometry_type"]

        # close the communication with the POSTGIS
        cur.close()

        return tile_instersections


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('POSTGIS connection closed.')
 
 
if __name__ == '__main__':
    intersections = get_intersections_from_db('Tile02O')
    print(intersections.describe())
    print(intersections.head())