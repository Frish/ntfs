CC = gcc
CPPFLAGS = -I. -I/usr/local/include
CFLAGS = -g -O2 -std=c99 -Wall -fPIC -fsigned-char -DNDEBUG
LIBS = -ltokyocabinet -lbz2 -lz -lpthread -lm -lc 
LDFLAGS = -L. -L/usr/local/lib -L/opt/local/lib
OS=$(shell uname)
objects = ntfs.so

ifeq ($(OS),Darwin)
	SHAREDFLAGS = -bundle -flat_namespace -undefined suppress
else
	SHAREDFLAGS = -shared
endif


ntfs.so : ntfs.c
	$(CC) $(CFLAGS) $(CPPFLAGS) $(SHAREDFLAGS) -o $@ ntfs.c \
		$(LDFLAGS) $(LIBS)


.PHONY : clean
clean :
	rm $(objects)