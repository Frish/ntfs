CC = gcc
CPPFLAGS = -I. -I/opt/local/include/python2.5 -I/usr/local/include/python2.5 -I/usr/local/include
CFLAGS = -g -O2 -std=c99 -Wall -fPIC -fsigned-char -DNDEBUG
LIBS = -ltokyocabinet -lbz2 -lz -lpthread -lm -lc 
LDFLAGS = -L. -L/usr/local/lib -L/opt/local/lib
OS=$(shell uname)
objects = pycabinet.o pycabinet.so

ifeq ($(OS),Darwin)
	SHAREDFLAGS = -bundle -flat_namespace -undefined suppress
	PYSITEPACKAGE = /opt/local/lib/python2.5/site-packages/
else
	SHAREDFLAGS = -shared
	PYSITEPACKAGE = /usr/local/lib/python2.5/site-packages/
endif


pycabinet.so : pycabinet.o
	$(CC) $(CFLAGS) $(SHAREDFLAGS) -o $@ pycabinet.o \
		$(LDFLAGS) $(LIBS)


pycabinet.o : pycabinet.c
	$(CC) -c $(CPPFLAGS) $(CFLAGS) pycabinet.c


install :
	cp pycabinet.so $(PYSITEPACKAGE)


.PHONY : clean
clean :
	rm $(objects)
