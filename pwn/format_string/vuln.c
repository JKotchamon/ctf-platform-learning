#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Function to print the flag
void print_flag() {
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("Flag file not found! Make sure flag.txt is in the same directory.\n");
        exit(1);
    }
    char flag[64];
    fgets(flag, sizeof(flag), f);
    printf("Congratulations! Here is your flag: %s\n", flag);
    fclose(f);
}

int main() {
    // Disable buffering for predictable I/O
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    // Variables on the stack
    int access_level = 0;
    char announcement[128];

    printf("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n");
    printf(" Welcome to the 32-bit Announcer! 🗣️\n");
    printf("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n");
    printf("I will announce anything you tell me.\n");
    printf("Only special announcers can get the flag.\n");

    // Give the player the address they need to overwrite.
    printf("To prove your worth, you must change the value at %p\n", &access_level);

    while (1) {
        printf("\n> ");
        fgets(announcement, sizeof(announcement), stdin);
        
        announcement[strcspn(announcement, "\n")] = 0;

        printf("Announcing: ");
        printf(announcement);
        printf("\n");

        if (access_level == 0x1337) {
            printf("\nWow! That was a powerful announcement!\n");
            print_flag();
            break;
        } else {
            printf("Hmm, that wasn't very convincing.\n");
        }
    }

    return 0;
}
