#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct AdminData {
    int is_admin;
    char secret_message[32];
};

struct UserProfile {
    char username[32];
};

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
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    
    struct UserProfile *user = malloc(sizeof(struct UserProfile));
    struct AdminData *admin = malloc(sizeof(struct AdminData));
    
    admin->is_admin = 0; // 0 = false
    strcpy(admin->secret_message, "You are a regular user.");
    
    printf("Welcome! Please enter your username:\n> ");
    
    gets(user->username);
    
    printf("\nHello, %s\n", user->username);
    printf("Checking permissions...\n");
    
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
