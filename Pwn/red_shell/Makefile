CC=gcc
CFLAGS=-fPIE -fstack-protector-all
LDFLAGS=-Wl,-z,now,-z,relro

all: redshll redshll_debug

redshll:
	$(CC) $(CFLAGS) -s $(LDFLAGS) shell.c -o redshll

redshll_debug:
	$(CC) $(CFLAGS) -g $(LDFLAGS) shell.c -o redshll_debug

clean:
	rm redshll redshll_debug
