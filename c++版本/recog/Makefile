CC = g++
BOOSTLIB = -std=c++11 -pthread -I/usr/include/python2.7 -lpython2.7

LIB = $(shell pkg-config --libs opencv)
INC = $(shell pkg-config --cflags opencv)
SRCFILE = recognize_main.cpp
DEBUGFLG= 
all:
		$(CC) $(SRCFILE) $(DEBUGFLG) $(INC) $(BOOSTLIB) $(LIB) -o recognize_main
clean:
		rm -rf recognize_main
