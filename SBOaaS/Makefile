CC=gcc
CFLAGS=-Wall -O1 -std=c99

stack: stack.c
	$(CC) -no-pie -fno-stack-protector -D_FORTIFY_SOURCE=0 -o stack stack.c $(CFLAGS)
	cp stack distrib/stack
