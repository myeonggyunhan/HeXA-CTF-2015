# Basic BOF

Simple Buffer Overflow


ssh guest@play.hexa.pro (pw: guest)

Problem location: /home/basic/basic


Hint 1: Just overflow the stack and overwrite return address to shellcode address.

Hint 2: (gdb) print &shellcode

Hint 3: [ char buffer[64] ] [ 12 byte dummy ] [ return address ]

- l34p
