################################################################################
# Title: ArCulvert
# Purpose: A Python module for ArcGIS Pro designed to detect culverts
# Author: Owen Smith
################################################################################

import os
from glob import glob
import arcpy

def process_dem(workspace, dem_path, mask=None,
                masked_raster_name='masked_dem'):
    arcpy.env.addOutputsToMap = False
    arcpy.env.overwriteOutput = True

    if not os.path.exists(workspace):
        os.mkdir(workspace)
    raster = arcpy.Raster(dem_path)
    if mask:
        if not masked_raster_name.endswith('.tif'):
            out_path = '%s/%s%s%s' % (workspace, 'fdem_',
                                      masked_raster_name, '.tif')
            out_mask = arcpy.sa.ExtractByMask(raster, mask)
            fill_sink = arcpy.sa.Fill(out_mask)
            dem = fill_sink.save(out_path)
        else:
            out_mask = arcpy.sa.ExtractByMask(raster, mask)
            out_path = '%s/%s%s' % (workspace, 'fdem_', masked_raster_name)
            fill_sink = arcpy.sa.Fill(raster)
            dem = fill_sink.save(out_path)
    if not mask:
        out_path = '%s/%s%s' % (workspace, 'fdem_', os.path.basename(
            dem_path))
        fill_sink = arcpy.sa.Fill(raster)
        dem = fill_sink.save(out_path)

    return dem


def create_flow_direction(workspace):

    arcpy.env.addOutputsToMap = False
    arcpy.env.overwriteOutput = True

    in_file = '%s/%s' % (workspace, 'fdem_*.tif')
    raster = arcpy.Raster(os.path.abspath(glob(in_file)[0]))
    out_file = '%s/%s' % (workspace, 'FlowDirection.tif')
    flow = arcpy.sa.FlowDirection(raster, flow_direction_type='D8')
    flow.save(out_file)

def create_flow_accumulation(workspace):

    arcpy.env.addOutputsToMap = False
    arcpy.env.overwriteOutput = True

    in_file = '%s/%s' % (workspace, 'FlowDirection.tif')
    raster = arcpy.Raster(os.path.abspath(in_file))
    out_file = '%s/%s' % (workspace, 'FlowAccumulation.tif')
    accum = arcpy.sa.FlowAccumulation(in_file, data_type='INTEGER',
                                      flow_direction_type='D8')
    accum.save(out_file)
