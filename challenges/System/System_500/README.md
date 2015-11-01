# HeCHO

HeXA echo server :)

nc play.hexa.pro 12345 or python <a href="https://gist.github.com/L34p/29ff67203755b70e08a1">client.py</a>

<a href="https://gist.github.com/L34p/b9f3df6385ae67c4ce9a">Problem source  code</a>


Hint 1: There are at least two vulnerabilities. Buffer Overflow and Format String Bug.

Hint 2: FSB(Format String Bug) can leak any address. So, ASLR can be defeated.

Hint 3: Input somthing like '%x %x %x' then you can see strange results.

Hint 4: %70$8x give you stack address(argv[0]) and you can overwrite argv[0] by using stack overflow.

- l34p
