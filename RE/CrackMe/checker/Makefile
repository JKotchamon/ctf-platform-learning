CC=gcc
CFLAGS=-O2 -s -Wall -Wextra
LDFLAGS=-lcrypto

all: target.h checker

checker: main.o
	$(CC) $(CFLAGS) -o checker main.o $(LDFLAGS)

main.o: main.c target.h

gen_target: gen_target.c
	$(CC) $(CFLAGS) -o gen_target gen_target.c $(LDFLAGS)

target.h: gen_target
	# FLAG is read from environment by gen_target
	./gen_target

clean:
	rm -f checker *.o gen_target target.h
