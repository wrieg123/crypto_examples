CC=gcc
CFLAGS=-I $(IDIR)
IDIR = ../../../../dependency
LFLAGS = -lstdc++ -lssl -lcrypto -lpthread

sync_client: sync_client.cc
	$(CC) sync_client.cc ${CFLAGS} -o sync_client $(LFLAGS)
