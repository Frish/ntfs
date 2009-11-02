#!/usr/local/bin/python
#encoding: utf-8

import os

def inserttsv(tsvpath):
    tsvs = os.listdir(tsvpath)
    for i in tsvs:
        if i.split('.')[1] == 'tsv':
            tchname = i.split('.')[0]+'.tch'
            shell = 'tchmgr importtsv %s  %s'%(os.path.join('/data0/ntfs/data/1/',tchname),os.path.join(tsvpath,i))
            print shell
            #os.popen(shell)
        

if __name__ == '__main__':
    import sys
    tsvpath = sys.argv[1]
    inserttsv(tsvpath)
