#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/err.h>

void handleErrors(void) {
    ERR_print_errors_fp(stderr);
    abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
            unsigned char *iv, unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx;
    int len;
    int ciphertext_len;

    if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv)) handleErrors();
    if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)) handleErrors();
    ciphertext_len = len;
    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) handleErrors();
    ciphertext_len += len;
    EVP_CIPHER_CTX_free(ctx);
    return ciphertext_len;
}

int main(void) {

    const char* b64_key_str = "TXlTZWNyZXRLZXkxMjM0NQ=="; 
    const char* b64_iv_str  = "TXlBd2Vzb21lSVY2Nzg5MA=="; 

    unsigned char key[16]; 
    unsigned char iv[16];  

    EVP_DecodeBlock(key, (const unsigned char*)b64_key_str, strlen(b64_key_str));
    EVP_DecodeBlock(iv, (const unsigned char*)b64_iv_str, strlen(b64_iv_str));

    FILE *f_in = fopen("flag.txt", "rb");
    if (f_in == NULL) {
        printf("Error: flag.txt not found.\n");
        return 1;
    }

    fseek(f_in, 0, SEEK_END);
    long f_size = ftell(f_in);
    fseek(f_in, 0, SEEK_SET);

    unsigned char *plaintext = malloc(f_size);
    fread(plaintext, 1, f_size, f_in);
    fclose(f_in);

    unsigned char ciphertext[f_size + 16];
    int ciphertext_len = encrypt(plaintext, f_size, key, iv, ciphertext);

    FILE *f_out = fopen("flag.txt.enc", "wb");
    fwrite(ciphertext, 1, ciphertext_len, f_out);
    fclose(f_out);

    printf("Successfully encrypted flag.txt to flag.txt.enc\n");

    free(plaintext);
    return 0;
}
