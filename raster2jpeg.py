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
    # 2011 - 2015
    #dst_ds = gdal.Translate(outfile, src_ds, creationOptions = ['COMPRESS=JPEG', 'TILED=YES', 'PHOTOMETRIC=YCBCR', 'PROFILE=GeoTIFF'])
    
    # 2006 - 2007
    # These images had an alpha channel before which was introduced by me some time ago. 
    # I think the originales ones don't have one. -> Processing could be different.
    #
    # 2002 
    # Outside is black. It neens further investigations: solve it on the application side (wms server) or try to "fix" image (e.g. nearblack etc. etc.)
    # and:
    # Basisplan.
    # Outside is black too. Change of production process.
    dst_ds = gdal.Translate(outfile, src_ds, bandList = [1,2,3], creationOptions = ['COMPRESS=JPEG', 'TILED=YES', 'PHOTOMETRIC=YCBCR', 'PROFILE=GeoTIFF'])

    # 1993 
    # Outside is black. It neens further investigations: solve it on the application side (wms server) or try to "fix" image (e.g. nearblack etc. etc.)
    # and:
    # DTM/DOM 2014 relief
    # DTM/DOM 2002 relief
    #dst_ds = gdal.Translate(outfile, src_ds, bandList = [1], creationOptions = ['COMPRESS=JPEG', 'TILED=YES', 'PROFILE=GeoTIFF'])

    # DTM/DOM 2014 grid
    #dst_ds = gdal.Translate(outfile, src_ds, creationOptions = ['COMPRESS=DEFLATE', 'PREDICTOR=2', 'TILED=YES', 'PROFILE=GeoTIFF'])

    dst_ds = None

    cmd = GDAL_PATH + "/gdal_edit.py -unsetmd " + outfile
    os.system(cmd)

    # mmmh, acutally I wanted -r average...
    cmd = GDAL_PATH + "/gdaladdo -r cubic "
    
    
    cmd += " --config COMPRESS_OVERVIEW JPEG"
    
    # only for 3 band rgb
    # disable for 1993
    cmd += " --config PHOTOMETRIC_OVERVIEW YCBCR"
    
    cmd += " --config INTERLEAVE_OVERVIEW PIXEL "
    
    cmd += " " + outfile 
    cmd += " 2 4 8 16 32 64 128"
    os.system(cmd)
