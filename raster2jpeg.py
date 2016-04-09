#!/usr/bin/python
# -*- coding: utf-8 -*-

from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import os
import os.path
import sys

# path to gdal devel
GDAL_PATH = "/usr/local/gdal_master/bin/"

# set input and output path
img_path = sys.argv[1]
if img_path[0] == "/":
    img_path = img_path[1:]
    
INPUT_PATH = os.path.join("/home/stefan/mnt/NAS-DS215j/Geodaten/", img_path) 
OUTPUT_PATH = os.path.join("/home/stefan/tmp/", img_path)

# throw exceptions
gdal.UseExceptions()
ogr.UseExceptions()

# check gdal version
version_num = int(gdal.VersionInfo('VERSION_NUM'))
print version_num


# create output path
try:
    os.makedirs(OUTPUT_PATH)
except Exception:
    pass
    
# create index gpkg
raster_idx = "raster_idx.gpkg"

cmd = "gdaltindex -f GPKG -t_srs EPSG:21781  " + OUTPUT_PATH + "/" + raster_idx + " " + INPUT_PATH + "/*.tif"
os.system(cmd)

# loop over index gpkg
gpkg = ogr.Open(os.path.join(OUTPUT_PATH, raster_idx))
layer = gpkg.GetLayer(0)

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
