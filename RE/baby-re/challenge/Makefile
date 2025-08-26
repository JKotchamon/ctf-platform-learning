CC=gcc
CFLAGS=-O2 -s -fno-stack-protector -fno-asynchronous-unwind-tables -fno-ident
LDFLAGS=
TARGET=baby-re-1

all: $(TARGET)

$(TARGET): baby-re-1.c
	$(CC) $(CFLAGS) -o $(TARGET) baby-re-1.c $(LDFLAGS)
	strip -s $(TARGET)

clean:
	rm -f $(TARGET)
