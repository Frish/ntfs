#!/bin/sh
NTFS_PATH=/data0/ntfs/myfs
/usr/local/bin/ttserver -dmn -pid $NTFS_PATH/ntfs.pid -log $NTFS_PATH/ntfs.log -port 1978 -ulog $NTFS_PATH/ulog-1 -sid 1 -skel $NTFS_PATH/ntfs.so $NTFS_PATH/data
