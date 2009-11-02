#encoding: utf-8
from utils import genkey,ntsha1,autodir
import os
import memcache
import urllib


def tchfiles(datapath):
    print datapath.split('|')[0], datapath
    return [[genkey(datapath.split('|')[0]), genkey(datapath)]]

def safefloat(n):
    try:
        return float(n)
    except:
        if n==None:return 0
        return n

class TTData(object):
    """
    Network traffic data
    """
    def __init__(self, datapath):
        self.pycabinet = memcache.Client(['10.88.15.61:1978'])
        self.path = datapath
        self.datapath = tchfiles(datapath)
        print self.datapath
        self.data = {}
    def __setitem__(self,k,v):
        self.data[k]=v
    def __getitem__(self,k):
        if len(self.datapath)==1:
            return safefloat(self.pycabinet.get("_".join([self.datapath[0][0],self.datapath[0][1],urllib.quote(k)])))
        return [safefloat(self.pycabinet.get("_".join([db[0],db[1],urllib.quote(k)]))) for db in self.datapath]
    def __str__(self):
        return str(self.datapath)
    def save(self):
        for k,v in self.data.items():
            if len(self.datapath)==1:
                self.pycabinet.set("_".join([self.datapath[0][0],self.datapath[0][1],urllib.quote(k)]),str(v))

if __name__ == '__main__':
    #print "finddb ZX|静安-广州",finddb("ZX|静安-广州",[])
    #print "finddb ZX|静安-广州|Gi-5/2 Traffic Out|d",finddb("ZX|静安-广州|Gi-5/2 Traffic Out|d",[])
    
    d=TTData("ZX|静安-广州|Gi-5/2 (GZ_TO_JA) Traffic Out|d")
    print d["2009-05-09 17:00:00"]
    
    #d["2009-05-09 17:00:00"] = 125.2
    #d["2009-05-09 17:05:00"] = 130
    #d.save()
    
    #d1=TTData("ZX|静安-广州|Gi-5/2 Traffic In|d")
    #d1["2009-05-09 17:00:00"] = 100.2
    #d1["2009-05-09 17:05:00"] = 110.4
    #d1.save()
    
    #assert d["2009-05-09 17:00:00"]=="125.2"
    #assert d1["2009-05-09 17:05:00"]=="110.4"
    
    #d3 = NTData("mc|conf")
    #print "mc|conf datapath",d3.datapath
    #d3["XD_JA_xxx"] = "123"
    #d3.save()
    #print "mc|conf XD_JA_xxx",d3["XD_JA_xxx"]
    #assert d3["XD_JA_xxx"]=="123"
    
    
