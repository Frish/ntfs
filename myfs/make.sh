#!/bin/sh
gcc -g -O2 -std=c99 -Wall -fPIC -fsigned-char -DNDEBUG -I/usr/local/include -bundle -ltokyocabinet -lbz2 -lz -lpthread -lm -lc -o ttk.so ttk.c
