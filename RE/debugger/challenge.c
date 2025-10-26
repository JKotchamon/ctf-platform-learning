#include <stdio.h>
#include <stdlib.h>

/*
This is a 'helper' function.
You don't need to reverse this function, 
just see what it does to our variable!
*/
void scramble_code(int *code) {
    *code = (*code * 2) + 1337;
}

void print_flag() {
    // In a real CTF, this would read from a 'flag.txt' file
    printf("\n>>> Success! <<<\n");
    printf("Flag: CTF{gDb_c4n_s33_th3_fUtUr3}\n");
}

int main() {
    int secret_code = 12345;
    int user_input;

    printf("--- Welcome to the GDB Jumpstart Challenge ---\n");
    printf("The original secret code is: %d\n", secret_code);
    
    // The code is modified by this function
    scramble_code(&secret_code);

    printf("\nPlease enter the secret code: ");
    
    // We get your input
    if (scanf("%d", &user_input) != 1) {
        printf("Invalid input!\n");
        return 1;
    }

    // --- The crucial comparison happens here ---
    if (user_input == secret_code) {
        print_flag();
    } else {
        printf("\nNope, that's not it. Keep trying!\n");
        printf("Hint: What is the value of 'secret_code' at line 40?\n");
    }

    return 0;
}
