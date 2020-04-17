################################################################################
# Title: ArCulvert
# Purpose: A Python module for ArcGIS Pro designed to detect culverts
# Author: Owen Smith
################################################################################

import arcpy
import os


def process_dem(out_folder, dem_path, mask=None,
                masked_raster_name='masked_dem'):
    raster = arcpy.Raster(dem_path)
    if mask:
        if not masked_raster_name.endswith('.tif'):
            out_path = '%s/%s%s' % (out_folder, masked_raster_name, '.tif')
            out_mask = arcpy.sa.ExtractByMask(raster, mask)
            dem = out_mask.save(out_path)
        else:
            out_mask = arcpy.sa.ExtractByMask(raster, mask)
            out_path = '%s/%s' % (out_folder, masked_raster_name)
            dem = out_mask.save(out_path)
    if not mask:
        out_path = '%s/%s' % (out_folder, os.path.basename(dem_path))
        dem = raster.save(out_path)

    return dem


