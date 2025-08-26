#include <stdio.h>
#include <string.h>
#include <stdint.h>

static const uint8_t target[] = {
    // Precomputed from "CTF{babyre_xor_123}"
    // transform: ((ch ^ 0x37) - 3) for each character
    0x71,0x60,0x6E,0x49,0x52,0x53,0x52,0x4B,0x42,0x4F,0x65,0x4C,0x55,0x42,0x65,0x03,0x02,0x01,0x47
};
static const size_t target_len = sizeof(target) / sizeof(target[0]);

static void banner(void) {
    puts("== baby-re-1 ==");
    puts("I hide a password. Give it to me and I'll say 'Correct!'.");
    puts("Hint: XOR + a tiny shift. No network, just local check.");
}

int main(void) {
    char in[128];
    banner();
    printf("Enter password: ");
    if (!fgets(in, sizeof(in), stdin)) {
        puts("Input error.");
        return 1;
    }
    // strip newline
    size_t n = strcspn(in, "\r\n");
    in[n] = '\0';

    if (n != target_len) {
        puts("Wrong length.");
        return 1;
    }

    // check transform: ((in[i] ^ 0x37) - 3) == target[i]
    for (size_t i = 0; i < n; i++) {
        uint8_t t = ((uint8_t)in[i] ^ 0x37) - 3;
        if (t != target[i]) {
            puts("Nope.");
            return 1;
        }
    }

    puts("Correct! 🎉");
    return 0;
}
