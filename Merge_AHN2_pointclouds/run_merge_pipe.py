import os.path
import numpy as np
from invoke import run
import argparse
import time


"""
    This python script runs the pdal pipeline merge-pipe-v0.json for a list of ground and object las files.
    The top level directory must be specified by hand. merge-pipe-v0.json should be located in the directory
    from which this script is run.
    
    merge-pipe-v0.json has the form:
    
{
    "pipeline":[
        {
            "tag":"ground_laz",            reads the ground las file
            "type":"readers.las",
            "filename":"ground_file"
        },
        {
            "type":"filters.assign",        sets the Classification value to ground ==2
            "assignment":"Classification[:]=2",
            "tag":"ground_classed"
        },
        {
            "tag":"objects_laz",            reads the object file
            "type":"readers.las",
            "filename":"objects_file"
        },
        {
            "type":"filters.assign",        sets the claqssification value to unclassified
            "assignment":"Classification[:]=1",
            "tag":"objects_classed"
        },
        {
            "tag":"merging",                merges the two files
            "type":"filters.merge",
            "inputs":["ground_classed" , "objects_classed"]
        },
        {
            "tag":"output_merged",           writes output
            "type":"writers.las",
            "filename":"merged_file",
            "forward":"all"
        }
    ]
}
    
    
   See pdal.io for a documentation of the individual pdal filters
"""



"""
++++++++++++++++++++++++++++++++++
Define utility functions
"""

# create pdal pipeline command to run the merge-pipe-v0.json pipeline using filenames specified at runtime

def run_pipe_cmd(ingroundfile,inobjectfile,mergedfile):
    rp_cmd = "pdal pipeline 'merge-pipe-v0.json' --writers.las.filename="+mergedfile+".laz --stage.ground_laz.filename="+ingroundfile+".laz --stage.objects_laz.filename="+inobjectfile+".laz --nostream"

    return rp_cmd



# extract unique tile names from a directory containing AHN2 files (ground files in this case located in the subdirectory terrain

def get_parent_list(data_path):
    object_file_path = data_path+'/terrain'
    all_tile_names = os.listdir(object_file_path)
    unique_tile_names = list(set([tn.split('_')[0][1:] for tn in all_tile_names]))
    return unique_tile_names


# construct file names at subtile level during run time. This assumes that the subdirectory merged has been created previously (manually)

def set_file_names(datapath,tile,index):

    files_exist = 0
    if index < 10:
        ground_file_name = data_path+'/terrain/'+'g'+tile+'_0'+str(index)
        object_file_name = data_path+'/objects/'+'u'+tile+'_0'+str(index)
        merged_file_name = data_path+'/merged/'+'ahn2_'+tile+'_0'+str(index)


    else:
        ground_file_name = data_path+'/terrain/'+'g'+tile+'_'+str(index)
        object_file_name = data_path+'/objects/'+'u'+tile+'_'+str(index)
        merged_file_name = data_path+'/merged/'+'ahn2_'+tile+'_'+str(index)

    if os.path.isfile(ground_file_name+'.laz') and os.path.isfile(object_file_name+'.laz'):
        print('mergeing files for tile:'+tile+' subtile:'+str(index)+' ')

    else:
        print('subtile '+str(index)+' does not exist for tile '+tile+' .')
        files_exist = 1

        
    return files_exist, ground_file_name, object_file_name, merged_file_name


# loop over all tiles with their subtiles and run pipeline merging ground and object files in each case
        
def merge_loop(parent_tile_list,data_path):

    for tile in parent_tile_list:
        tile_start_time = time.time()

        for i in range(25):
            subtile_start_time=time.time()
            index = i+1

            files_exist, ground_file, object_file,merged_file = set_file_names(data_path,tile,index)

            if files_exist == 0:

                run_merge_cmd = run_pipe_cmd(ground_file, object_file, merged_file)
                
                result_merge_pipe = run(run_merge_cmd, hide=True, warn=True)

                if result_merge_pipe.ok != True:
                    print('pipeline failure for tile: '+tile+' subtile: '+str(index))

            else:
                print('subtile '+str(index)+' does not exist.')

            subtile_end_time=time.time()
            subtile_diff_time = subtile_end_time - subtile_start_time
            print(('total time for subtile: % sec') % (subtile_diff_time))

        tile_end_time = time.time()
        tile_diff_time = tile_end_time - tile_start_time
        print(('total time for tile: % sec') % (tile_diff_time))
       
                                             
                                            

"""
++++++++++++++++++++++++
Main()
"""
start_time = time.time()

#set data path manually
data_path = '/path/to/top-level/data_directory'

#get tile list
parent_tile_list = get_parent_list(data_path)

#execute merge for all subtiles of tiles in tile list
merge_loop(parent_tile_list,data_path)

full_time = time.time()
total_diff_time = full_time - start_time
print('done')
print(('total time : % sec') % (total_diff_time))

