#!/bin/sh

MASTER_HOST=10.88.15.61

rsync -av $MASTER_HOST:/data0/ntfs/myfs/data .
echo xxxxx > 2.rts
mkdir ulog-2
./slave.sh
