#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// A structure to hold secret admin data.
// Our goal is to overwrite the 'is_admin' member.
struct AdminData {
    int is_admin;
    char secret_message[32];
};

// A structure to hold the user's data.
struct UserProfile {
    char username[32];
};

// This function now reads the flag from "flag.txt".
void print_flag() {
    char flag[128];
    FILE *file = fopen("flag.txt", "r");

    if (file == NULL) {
        printf("\nError: Could not open flag.txt. Ensure the file exists.\n");
        return;
    }

    if (fgets(flag, sizeof(flag), file) != NULL) {
        printf("\nSuccess! Here is your flag: %s", flag);
    }

    fclose(file);
}

int main() {
    // Disable buffering for smooth interaction.
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    
    // 1. Allocate space for the user profile on the heap.
    struct UserProfile *user = malloc(sizeof(struct UserProfile));
    
    // 2. Allocate space for the admin data on the heap, right after the user.
    struct AdminData *admin = malloc(sizeof(struct AdminData));
    
    // Initialize admin data. You start as a regular user.
    admin->is_admin = 0; // 0 = false
    strcpy(admin->secret_message, "You are a regular user.");
    
    printf("Welcome! Please enter your username:\n> ");
    
    // THE VULNERABILITY: gets() reads input without checking the buffer size.
    // It will read into user->username, which is only 32 bytes long.
    gets(user->username);
    
    printf("\nHello, %s\n", user->username);
    printf("Checking permissions...\n");
    
    // 3. The check: If is_admin is not 0, you win!
    if (admin->is_admin != 0) {
        printf("Wait... you have admin permissions? How?!");
        print_flag();
    } else {
        printf("Permission check complete. You are not an admin.\n");
    }
    
    free(user);
    free(admin);
    
    return 0;
}
