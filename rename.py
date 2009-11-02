#encoding: utf-8
from utils import ntsha1
import sys,os

def rename(old,new):
    return ntsha1(old),ntsha1(new)

if __name__ == '__main__':
    old,new = sys.argv[1],sys.argv[2]
    cmd = "tchmgr list hashkey.tch|grep '%s'" % old
    for old_r in os.popen(cmd).read().split("\n"):
        if old_r.strip()=="":continue
        new_r = old_r.replace(old,new)
        oldsha1,newsha1 = rename(old_r,new_r)
        print "old sha1:",old_r,"->",oldsha1
        print "new sha1:",new_r,"->",newsha1
        print "mv data/1/%s.tch data/1/%s.tch" % (oldsha1,newsha1)
