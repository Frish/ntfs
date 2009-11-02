#encoding: utf-8
from hashlib import sha1
import pycabinet
import os

PROJ_PATH = '/data0/ntfs'
DATA_PATH = os.path.join(PROJ_PATH,'data/')

def safetch(dbname,dbpath=PROJ_PATH):
    dbname = os.path.join(dbpath,dbname)
    try:
        os.stat(dbname)
    except:
        pycabinet.create(dbname)
    return dbname

def ntsha1(k):
    """
    >>> ntsha1("IDC|西单网通|port1|d")
    '7ab0512e54099ce5be8819eabc41be2dc46fa106'
    """
    return sha1(k).hexdigest()

def autodir(s,dirpath=DATA_PATH):
    """
    >>> autodir("IDC|西单网通|port1|d")
    '267a011c682b67839e358faf6ba016ac7fed1d4c'
    """
    p = os.path.join(dirpath,ntsha1(s.split("|")[0]))
    try:
        os.stat(p)
    except:
        os.makedirs(p)
    return p

def genkey(s):
    hashdb = safetch('hashkey.tch')
    key = pycabinet.get(hashdb,s)
    if key==None:
        key=ntsha1(s)
        pycabinet.put(hashdb,s,key)
    fname = safetch( "%s.tch" % key, autodir(s) )
    return key

if __name__ == '__main__':
    import doctest
    doctest.testmod()

