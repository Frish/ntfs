#!/bin/sh

NTFS_PATH=/data0/ntfs/myfs

kill `cat $NTFS_PATH/ntfs.pid`
rm $NTFS_PATH/ntfs.pid

/usr/local/bin/ttserver -dmn -pid $NTFS_PATH/ntfs.pid -log $NTFS_PATH/ntfs.log -port 1978 -ulog $NTFS_PATH/ulog-2 -sid 2 -mhost 10.88.15.61 -mport 1978 -rts $NTFS_PATH/2.rts -skel $NTFS_PATH/ntfs.so -ext $NTFS_PATH/newfs.lua $NTFS_PATH/data

