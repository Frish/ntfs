#!/bin/sh

PROJ_PATH=/data0/ntfs
TT_PATH=$PROJ_PATH/tt
echo $TT_PATH

ttserver -host 10.88.15.47 -port 11216 -thnum 4 -dmn -pid $TT_PATH/ttserver.pid -log $TT_PATH/ttserver.log -uas -le -ulog $TT_PATH/ulog -ulim 512m -sid 1 -ext $TT_PATH/usherette.lua $PROJ_PATH/cachedb.tch
