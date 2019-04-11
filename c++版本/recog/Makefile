CC = g++
BOOSTLIB = -std=c++11 -pthread -I/usr/include/python2.7 -lpython2.7

MIDFILE = c_plus_dirsfiles.cpp c_plus_dirsfiles.h 
LIB = $(shell pkg-config --libs opencv)
INC = $(shell pkg-config --cflags opencv)
SRCFILE = recgnize_main.cpp
DEBUGFLG= 
all:
		$(CC) $(SRCFILE) $(DEBUGFLG) $(INC) $(BOOSTLIB) $(LIB) $(MIDFILE) -o recgnize_main
clean:
		rm -rf recgnize_main
