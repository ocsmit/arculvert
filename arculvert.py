################################################################################
# Title: ArCulvert
# Purpose: A Python module for ArcGIS Pro designed to detect culverts
# Author: Owen Smith
################################################################################

import arcpy
import os


def process_dem(workspace, dem_path, mask=None,
                masked_raster_name='masked_dem'):
    arcpy.env.addOutputsToMap = False
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



