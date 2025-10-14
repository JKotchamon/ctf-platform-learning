#include <stdio.h>
#include <unistd.h>

void useful_gadget() {
    asm("jmp %esp");
}

void submit_report() {
    char report_buffer[80];
    puts("Please submit your anonymous bug report below:");
    gets(report_buffer);
    puts("Thank you. Your report has been submitted.");
}

int main() {
    setuid(0);
    setgid(0);

    submit_report();

    return 0;
}
