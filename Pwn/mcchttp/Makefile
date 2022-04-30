CC = gcc
CFLAGS = -fno-stack-protector -no-pie -z execstack

all: http test http_debug

header.o:
	$(CC) -c $(CFLAGS) header.c

test: header.o
	$(CC) $(CFLAGS) test.c header.o -o unit_tests

http: header.o
	$(CC) $(CFLAGS) http.c header.o -o mcchttp
	sha256sum mcchttp > mcchttp.sha256

http_debug: header.o
	$(CC) $(CFLAGS) -g http.c header.o -o mcchttp_debug

clean:
	rm *.o mcchttp unit_tests peda-session-unit_tests.txt
