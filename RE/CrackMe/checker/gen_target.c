#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <openssl/aes.h>

// Build-time: reads FLAG from env (or uses default), AES-128-ECB encrypts it,
// PKCS#7 pads, and writes target.h with TARGET/TARGET_LEN.

static void pkcs7_pad(uint8_t *buf, size_t *len, size_t cap) {
    size_t pad = 16 - (*len % 16);
    if (pad == 0) pad = 16;
    if (*len + pad > cap) return;
    for (size_t i = 0; i < pad; i++) buf[*len + i] = (uint8_t)pad;
    *len += pad;
}

int main(void) {
    const char *flag = getenv("FLAG");
    if (!flag || !*flag) flag = "CTF{AES_is_more_fun}";

    static const uint8_t KEY[16] = {
        0x13,0x37,0xC0,0xDE,0x42,0x21,0x69,0x00,
        0xAA,0x55,0x44,0x33,0x22,0x11,0xFE,0xED
    };

    uint8_t buf[256] = {0};
    size_t len = strlen(flag);
    if (len > 200) { fprintf(stderr, "FLAG too long\n"); return 1; }
    memcpy(buf, flag, len);
    pkcs7_pad(buf, &len, sizeof(buf));

    uint8_t out[256] = {0};
    AES_KEY aes;
    AES_set_encrypt_key(KEY, 128, &aes);
    for (size_t i = 0; i < len; i += 16) {
        AES_ecb_encrypt(buf + i, out + i, &aes, AES_ENCRYPT);
    }

    FILE *f = fopen("target.h", "w");
    if (!f) { perror("target.h"); return 1; }

    fprintf(f, "#pragma once\n");
    fprintf(f, "static const unsigned int TARGET_LEN = %u;\n", (unsigned)len);
    fprintf(f, "static const unsigned char TARGET[%u] = {", (unsigned)len);
    for (unsigned i = 0; i < len; i++) {
        if (i) fprintf(f, ",");
        fprintf(f, "0x%02X", out[i]);
    }
    fprintf(f, "};\n");
    fclose(f);

    return 0;
}
