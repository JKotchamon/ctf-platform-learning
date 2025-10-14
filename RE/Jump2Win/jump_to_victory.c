#include <stdio.h>
#include <string.h>

// This function is never called from main!
void print_flag() {
    printf("Congratulations! You found it!\n");
    printf("Flag: CTF{jUmP_iN_tHe_cAdIlLaC}\n");
}

void main() {
    char name[32];
    
    printf("Welcome, challenger!\n");
    printf("What is your name? ");
    gets(name); 
    
    printf("Hello, %s! The flag is somewhere, but not here...\n", name);
}