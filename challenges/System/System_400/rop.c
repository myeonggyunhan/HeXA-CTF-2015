//gcc -o rop rop.c -m32 -fno-stack-protector -z execstack -static
#include <string.h>
int main(int argc, char* argv[])
{
    char buffer[64];
    puts("Attack me and read the flag :)");

    // Buffer Overflow! but... we can't know exact stack address because of ASLR!
    // Can you break ASLR? (hint: Return Oriented Programming, ROP)
    if(argc > 1)
        strcpy(buffer, argv[1]);
}
