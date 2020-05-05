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
    accum = arcpy.sa.FlowAccumulation(raster, data_type='INTEGER',
                                      flow_direction_type='D8')
    accum.save(out_file)


def process_road(workspace, shp_path, field, cell_size=10, mask=None,
                 masked_shp_name='masked_dem'):

    arcpy.env.addOutputsToMap = False
    arcpy.env.overwriteOutput = True

    if not os.path.exists(workspace):
        os.mkdir(workspace)

    if mask:
        if not masked_shp_name.endswith('.shp'):
            out_path = '%s/%s%s' % (workspace, masked_shp_name, '.tif')
            out_mask = arcpy.Clip_analysis(shp_path, mask, 'in_memory/tmp')
            raster = arcpy.PolygonToRaster_conversion("in_memory/tmp", field,
                                                      out_path)
            outCon = arcpy.sa.Con(arcpy.Raster(out_path), 1)
            out_path = '%s/%s%s%s' % (workspace, 're_', masked_shp_name, '.tif')
            outCon.save(out_path)
        else:
            out_path = '%s/%s' % (workspace, masked_shp_name)
            raster = arcpy.PolygonToRaster_conversion("in_memory/tmp", field,
                                                      out_path)
            outCon = arcpy.sa.Con(arcpy.Raster(out_path), 1)
            out_path = '%s/%s%s' % (workspace, 're_', masked_shp_name)
            outCon.save(out_path)
    if not mask:
        out_path = '%s/%s' % (workspace, os.path.basename(
            shp_path))
        raster = arcpy.PolygonToRaster_conversion("in_memory/tmp", field,
                                                  out_path)
        outCon = arcpy.sa.Con(arcpy.Raster(out_path), 1)
        out_path = '%s/%s%s' % (workspace, 're_', os.path.basename(
            shp_path))
        outCon.save(out_path)
