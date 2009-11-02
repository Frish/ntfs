import pycabinet

db='my.tcb'
print "create db",db
pycabinet.create(db)
pycabinet.put2(db,'yanxu','123')
pycabinet.put2(db,'yanxu','456')
print pycabinet.list2(db)

db='my.tch'
print "create db",db
pycabinet.create(db)
pycabinet.put(db,'yanxu','123')
pycabinet.put(db,'qingfeng','456')
print pycabinet.list(db)
print "out key yanxu:"
pycabinet.out(db,'yanxu')
print pycabinet.list(db)
