#encoding: utf-8
from ntdata import NTData
from datetime import datetime,timedelta
from utils import genkey,ntsha1,safetch
import pycabinet
import os


def changetime(t):
    return t.replace(minute=t.minute-t.minute%5,second=0,microsecond=0)

def rtimerange(stime,etime):
    stime,etime = changetime(stime),changetime(etime) 
    while stime < etime:
        yield stime
        stime += timedelta(0,5*60)


class NTMapReduce(object):
    def __init__(self,ntdata,stime,etime,name):
        if isinstance(ntdata,NTData):
            self.ntdata = ntdata
        else:
            self.ntdata = ntdata[0]
            def ddpath(x,y):
                if isinstance(x,list):
                    return x+y.datapath
                if x=="":return y.datapath
                return x.datapath+y.datapath
            self.ntdata.datapath = reduce(ddpath,ntdata,"")
        self.stime = stime
        self.etime = etime
        self.name = name
        self.data = [self.ntdata[str(t)] for t in rtimerange(self.stime,self.etime)]
    def map_func(self,func=lambda x:x):
        self.data = map(func,self.data)
        return self
    def reduce_func(self,func=lambda x,y:(x,y)):
        v = reduce(func,self.data)
        return v
    def execute_func(self,func):
        return func(self.data)

def safesum(n):
    if n==None:return 0
    if isinstance(n,float):return n
    if isinstance(n,int):return n
    return sum(n)

def avg(data):
    if len(data)!=0:
        return sum(data)/len(data)
    return 0

def safemin(x,y):
    if int(x)==0:return y
    if int(y)==0:return x
    return min(x,y)

if __name__ == '__main__':
    stime = datetime(2008,9,1)
    etime = datetime(2008,9,10)
    name1 = "ZX|静安-广州|Gi-5/2 Traffic In|d"
    name2 = "ZX|静安-广州|Gi-5/2 Traffic Out|d"
    d1 = NTData(name1)
    d2 = NTData(name2)
    m1 = NTMapReduce(d1,stime,etime,"max").reduce_func(max)
    m2 = NTMapReduce(d2,stime,etime,"max").reduce_func(max)
    print "name1 max value is:",m1
    print "name2 max value is:",m2

    name3 = "ZX|静安-广州"
    d3 = NTData(name3)
    print d3.datapath
    f = NTMapReduce(d3,stime,etime,"feng").map_func(safesum).reduce_func(max)
    #f = NTMapReduce(d3,stime,etime).map_func(safesum)
    print "feng value is:",f/1000,"MB"
