#include <stdio.h>
#include <stdlib.h>

struct Packet {
    char buf[8];
    unsigned int key;
};

void win(void) {
    FILE *f = fopen("flag.txt", "r");
    if (!f) { puts("flag.txt missing"); return; }
    char flag[128];
    if (fgets(flag, sizeof(flag), f)) {
        printf("🎉 Flag: %s\n", flag);
    } else {
        puts("flag read error");
    }
    fclose(f);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("== Tiny Overflow ==");
    puts("Goal: set key to 0x44434241 (ASCII 'ABCD')");
    puts("Send your input:");
    struct Packet p;
    p.key = 0;
    /* intentionally unsafe for CTF learning */
    gets(p.buf); /* NOLINT */
    if (p.key == 0x44434241u) {
        win();
    } else {
        printf("Nope. key=0x%08X\n", p.key);
    }
    return 0;
}
