#encoding: utf-8
from __future__ import with_statement
import sys,os
import pycabinet


def totsv(f):
    tsvf = open("/tmp/tsv.tmp.tsv","w")
    for k,v in pycabinet.list(f).items():
        s = "%s\t%s" % (k,v)
        print >> tsvf,s
    tsvf.close()

def forceimport(f1,f2):
    totsv(f1)
    print importsv(f2)
    return f1,f2

def runimport(f1,f2,maxtomin=False):
    s1,s2 = os.path.getsize(f1),os.path.getsize(f2)
    if maxtomin:
        s1,s2 = s2,s1
    if s1<=s2:
        totsv(f1)
        importsv(f2)
    else:
        totsv(f2)
        importsv(f1)
    return f1,f2

def importsv(f):
    cmd = "/usr/local/bin/tchmgr importtsv %s /tmp/tsv.tmp.tsv" % f
    return os.popen(cmd).read()


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-s", "--file1", dest="f1",
                      help="tokyo cabinet tch file")
    parser.add_option("-e", "--file2", dest="f2",
                      help="tokyo cabinet tch file")
    parser.add_option("-m", "--maxtomin", dest="maxtomin", default=False,
                      help="default min size file merge to max size file")

    (options, args) = parser.parse_args()
    if not options.f1 and not options.f2:
        print "please setting tch files"

    print runimport(options.f1,options.f2,options.maxtomin)

