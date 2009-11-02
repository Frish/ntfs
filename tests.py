#encoding: utf-8
from ntdata import NTData
from ntmapreduce import NTMapReduce,safesum,avg,changetime
from datetime import datetime,timedelta
from random import random
import time
import pycabinet
import unittest

class NTDataTest(unittest.TestCase):
    def setUp(self):
        self.port1_week_max = 0
        self.port1_week_min = 9999999
        self.port1_week_avg = 0
        self.port_out_week_feng = {}
        self.port_out_week_feng_3out = {}
        self.multi_sep_week_feng = {}
        self.__putdata()
    def __putdata(self):
        print "__putdata"
        port1_sum = []
        for node in [
            'TEST|GZ|port1 Out|d',
            'TEST|GZ|port1 In|d',
            'TEST|GZ|port2 Out|d',
            'TEST|GZ|port2 In|d',
            'TEST|GZ|port3 Out|d',
            'TEST2|GZ|port1 Out|d'
        ]:
            d = NTData(node)
            stime = datetime(2009,5,20)
            etime = datetime(2009,6,1)
            stime,etime = changetime(stime),changetime(etime) 
            while stime < etime:
                v = random()*3000
                d[str(stime)] = v
                # print str(stime),v
                if node == 'TEST|GZ|port1 Out|d':
                    port1_sum.append(v)
                    self.port1_week_max = max(v,self.port1_week_max)
                    self.port1_week_min = min(v,self.port1_week_min)
                if node.find("Out")!=-1 and node.find("TEST|")!=-1:
                    self.port_out_week_feng_3out.setdefault(str(stime),0)
                    self.port_out_week_feng_3out[str(stime)] += float(v)
                    if node.find("port3")==-1:
                        self.port_out_week_feng.setdefault(str(stime),0)
                        self.port_out_week_feng[str(stime)] += float(v)
                if node=='TEST|GZ|port1 Out|d' or node=='TEST2|GZ|port1 Out|d':
                    self.multi_sep_week_feng.setdefault(str(stime),0)
                    self.multi_sep_week_feng[str(stime)] += float(v)
                stime += timedelta(0,5*60)
            if node == 'TEST|GZ|port1 Out|d':
                self.port1_week_avg = sum(port1_sum)/len(port1_sum)
            d.save()
        self.port_out_week_feng = max(self.port_out_week_feng.values())
        self.port_out_week_feng_3out = max(self.port_out_week_feng_3out.values())
        self.multi_sep_week_feng = max(self.multi_sep_week_feng.values())
    def test_all(self):
        test_start_time = time.time()
        
        stime = datetime(2009,5,20)
        etime = datetime(2009,6,1)
        
        node = "TEST|GZ|port1 Out|d"
        d = NTData(node)
        print d.path,d.datapath
        v = NTMapReduce(d,stime,etime,"week_max") \
                    .reduce_func(max)
        self.assertEqual("%.2f"%v,"%.2f"%self.port1_week_max)
        print node,"2009-4-1 to 2009-4-9 周最大值:",v
        v = NTMapReduce(d,stime,etime,"week_min") \
                    .reduce_func(min)
        self.assertEqual("%.2f"%v,"%.2f"%self.port1_week_min)
        print node,"2009-4-1 to 2009-4-9 周最小值:",v
        v = NTMapReduce(d,stime,etime,"week_avg") \
                    .execute_func(avg)
        self.assertEqual("%.2f"%v,"%.2f"%self.port1_week_avg)
        print node,"2009-4-1 to 2009-4-9 周平均值:",v
        
        
        
        node1 = 'TEST|GZ|port1 Out|d'
        d1 = NTData(node1)
        v = NTMapReduce([d1,],stime,etime,"week_feng") \
                    .map_func(safesum) \
                    .reduce_func(max)
        self.assertEqual("%.2f"%v,"%.2f"%self.port1_week_max)
        print node1,"2009-4-1 to 2009-4-9 峰值:",v
        
        
        
        node1 = 'TEST|GZ|port1 Out|d'
        node2 = 'TEST|GZ|port2 Out|d'
        d1 = NTData(node1)
        d2 = NTData(node2)
        v = NTMapReduce([d1,d2],stime,etime,"week_feng") \
                    .map_func(safesum) \
                    .reduce_func(max)
        self.assertEqual("%.2f"%v,"%.2f"%self.port_out_week_feng)
        print node1,node2,"2009-4-1 to 2009-4-9 峰值:",v
        
        
        #test_fix_multitchs
        node1 = 'TEST|GZ|port1 Out|d'
        node2 = 'TEST|GZ|port2 Out|d'
        node3 = 'TEST|GZ|port3 Out|d'
        d1 = NTData(node1)
        d2 = NTData(node2)
        d3 = NTData(node3)
        v = NTMapReduce([d1,d2,d3],stime,etime,"week_feng") \
                    .map_func(sum) \
                    .reduce_func(max)
        self.assertEqual("%.2f"%v,"%.2f"%self.port_out_week_feng_3out)
        print node1,node2,node3,"2009-4-1 to 2009-4-9 峰值:",v


        node1 = 'TEST|GZ|port1 Out|d'
        node2 = 'TEST2|GZ|port1 Out|d'
        d1 = NTData(node1)
        d2 = NTData(node2)
        v = NTMapReduce([d1,d2],stime,etime,"week_feng") \
                    .map_func(safesum) \
                    .reduce_func(max)
        self.assertEqual("%.2f"%v,"%.2f"%self.multi_sep_week_feng)
        print node1,node2,"2009-4-1 to 2009-4-9 峰值:",v



        test_end_time = time.time()
        print "test_end_time-test_start_time:",test_end_time-test_start_time
        

if __name__ == '__main__':
    unittest.main()
