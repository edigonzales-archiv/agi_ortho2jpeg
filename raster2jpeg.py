#!/usr/bin/python
# -*- coding: utf-8 -*-

from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import os
import sys

gdal.UseExceptions()
ogr.UseExceptions()

version_num = int(gdal.VersionInfo('VERSION_NUM'))
print version_num

GDAL_PATH = "/usr/local/gdal_master/bin/"
INPUT_PATH = "/home/stefan/mnt/NAS-DS215j/tmp/2012/"
OUTPUT_PATH = "/home/stefan/tmp/2012/"

gpkg = ogr.Open(os.path.join(INPUT_PATH,"ortho2012_idx.gpkg"))
layer = gpkg.GetLayerByName("ortho2012_idx")

for feature in layer:
    infileName = feature.GetField('location')
    print "**********************: " + os.path.basename(infileName)
        
    infile = os.path.join(INPUT_PATH, infileName)
    outfile = os.path.join(OUTPUT_PATH, os.path.basename(infileName))
    


    src_ds = gdal.Open(infile)
    dst_ds = gdal.Translate(outfile, src_ds, creationOptions = ['COMPRESS=JPEG', 'TILED=YES', 'PHOTOMETRIC=YCBCR', 'PROFILE=GeoTIFF'])
    dst_ds = None

    cmd = GDAL_PATH + "/gdal_edit.py -unsetmd " + outfile
    os.system(cmd)

    cmd = GDAL_PATH + "/gdaladdo -r cubic --config COMPRESS_OVERVIEW JPEG"
    cmd += " --config PHOTOMETRIC_OVERVIEW YCBCR"
    cmd += " --config INTERLEAVE_OVERVIEW PIXEL " + outfile 
    cmd += " 2 4 8 16 32 64 128"
    os.system(cmd)
