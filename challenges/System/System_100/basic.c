//gcc -o basic basic.c -m32 -fno-stack-protector -z execstack
#include <string.h>

char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80";

int main(int argc, char* argv[])
{
    char buffer[64];
    puts("Attack me and read the flag :)");

    // Buffer Overflow! If you know shellcode address, return to there!
    if(argc > 1)
        strcpy(buffer, argv[1]);
}
