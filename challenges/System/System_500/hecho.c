// gcc -o hecho hecho.c -m32 -fno-stack-protector -z execstack
#include <stdio.h>
#include <string.h>

void intro(void);
void do_echo(void);

int main(void)
{
	intro();

	while(1)
		do_echo();
}

void do_echo(void)
{
	char buffer[256];
	fgets(buffer, 1024, stdin);

	printf(buffer);
	fflush(stdout);
}

void intro(void)
{
	char welcome[] ="	    __  __     ________  ______ 	\n"
			"	   / / / /__  / ____/ / / / __ \\	\n"
			"	  / /_/ / _ \\/ /   / /_/ / / / /	\n"
			"	 / __  /  __/ /___/ __  / /_/ /		\n"
			"	/_/ /_/\\___/\\____/_/ /_/\\____/	\n\n"
			"	 Welcome to HeXA Echo Service!		\n";

	puts(welcome);
	fflush(stdout);
}

