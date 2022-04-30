CC=gcc
CFLAGS=-fPIE -fstack-protector-all
LDFLAGS=-Wl,-z,now,-z,relro

all: grnshll grnshll_debug

grnshll:
	$(CC) $(CFLAGS) $(LDFLAGS) shell.c -o grnshll

grnshll_debug:
	$(CC) $(CFLAGS) -g $(LDFLAGS) shell.c -o grnshll_debug

clean:
	rm grnshll grnshll_debug
