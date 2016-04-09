#!/bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/gdal_master/lib
export PYTHONPATH=$PYTHONPATH:/usr/local/gdal_master/lib/python2.7/site-packages/

./raster2jpeg.py $1
