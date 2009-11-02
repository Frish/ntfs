import pycabinet
import os,sys

p = sys.argv[1]
dbname = pycabinet.get('hashkey.tch',p)
data = pycabinet.list('data/1/%s.tch' % dbname)

print "\n".join(data)