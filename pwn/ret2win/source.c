#include <stdio.h>
#include <stdlib.h>

void ret2win() {
    FILE *fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Error: Could not open flag.txt\n");
        exit(1);
    }
    char flag[100];
    if (fgets(flag, sizeof(flag), fp) != NULL) {
        printf("Flag: %s", flag);
    } else {
        printf("Error: Could not read flag.txt\n");
    }
    fclose(fp);
}

void register_name() {
    char buffer[16];
    printf("Name:\n");
    scanf("%s", buffer);
    printf("Hi there, %s\n", buffer);
}

int main() {
    setbuf(stdout, NULL); // Disable output buffering for consistent behavior
    register_name();
    return 0;
}
