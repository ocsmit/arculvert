################################################################################
# Title: ArCulvert
# Purpose: A Python module for ArcGIS Pro designed to detect culverts
# Author: Owen Smith
################################################################################

import arcpy
import os

def create_GDB(out_folder, gdb_name):
    arcpy.CreateFileGDB_management(out_folder, gdb_name)
    if not gdb_name.endswith('.gdb'):
        gdb = '%s%s' % (gdb_name, '.gdb')
    else:
        gdb = gdb_name
    gdb_path = os.path.join(out_folder, gdb)
    return gdb_path
