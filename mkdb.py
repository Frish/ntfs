#!/usr/local/bin/python
#encoding: utf-8

from glob import glob
from utils import genkey
import os,sys
import pycabinet

def getdbpath(fid=1):
    dbpath = os.path.join("data/",str(fid))
    try:
        os.makedirs( dbpath )
    except:
        pass
    if len(glob("%s/*.tch"%dbpath))>=10000:
        getdbpath(fid+1)
    return fid,dbpath
    

def main(key):
    fid,dbpath = getdbpath()
    #e.g "IDC|播客|前端|d"
    dbname = "%s.tch" % genkey(key)
    pycabinet.create( os.path.join(dbpath,dbname) )

if __name__ == '__main__':
    main(sys.argv[1])
