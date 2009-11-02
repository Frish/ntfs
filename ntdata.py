#encoding: utf-8
from utils import genkey,ntsha1,autodir
import pycabinet
import os


def tchfiles(datapath):
    return [os.path.join( autodir(datapath), "%s.tch" % genkey(datapath)),]

def safefloat(n):
    try:
        return float(n)
    except:
        if n==None:return 0
        return n

class NTData(object):
    """
    Network traffic data
    """
    def __init__(self, datapath):
        self.path = datapath
        self.datapath = tchfiles(datapath)
        self.data = {}
    def __setitem__(self,k,v):
        self.data[k]=v
    def __getitem__(self,k):
        if len(self.datapath)==1:
            return safefloat(pycabinet.get(self.datapath[0],k))
        return [safefloat(pycabinet.get(db,k)) for db in self.datapath]
    def __str__(self):
        return str(self.datapath)
    def save(self):
        for k,v in self.data.items():
            if len(self.datapath)==1:
                pycabinet.put(self.datapath[0],str(k),str(v))
            else:
                for db in self.datapath:
                    pycabinet.put(db,str(k),str(v))

if __name__ == '__main__':
    print "finddb ZX|静安-广州",finddb("ZX|静安-广州",[])
    print "finddb ZX|静安-广州|Gi-5/2 Traffic Out|d",finddb("ZX|静安-广州|Gi-5/2 Traffic Out|d",[])
    
    d=NTData("ZX|静安-广州|Gi-5/2 Traffic Out|d")
    d["2009-05-09 17:00:00"] = 125.2
    d["2009-05-09 17:05:00"] = 130
    d.save()
    
    d1=NTData("ZX|静安-广州|Gi-5/2 Traffic In|d")
    d1["2009-05-09 17:00:00"] = 100.2
    d1["2009-05-09 17:05:00"] = 110.4
    d1.save()
    
    assert d["2009-05-09 17:00:00"]=="125.2"
    assert d1["2009-05-09 17:05:00"]=="110.4"
    
    d3 = NTData("mc|conf")
    print "mc|conf datapath",d3.datapath
    d3["XD_JA_xxx"] = "123"
    d3.save()
    print "mc|conf XD_JA_xxx",d3["XD_JA_xxx"]
    assert d3["XD_JA_xxx"]=="123"
    
    
