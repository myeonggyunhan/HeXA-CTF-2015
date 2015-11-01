// gcc -o thecow thecow.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char cow_face[8]={'w', 't', 'y', 'p', 's', 'd', 'g', 'b'};

int select_menu(void);
void clear_stdin(void);

void cow_fortune(void);
void cow_time(void);
void cow_echo(void);
void cow_exit(void);

int main(void)
{
	srand(time(0));
	while(1)
	{
		switch(select_menu()){
			case 1: cow_fortune(); break;
			case 2: cow_time(); break;
			case 3: cow_echo(); break;
			case 4: cow_exit(); break;
			default: puts("Available menu is 1~4! Please select again."); break;
		}
	}

	return 0;
}

int select_menu(void)
{
	int num, check;
	printf("\nWhat does the cow say!\n\n");
	puts("1. Cow fortune");
	puts("2. Cow time");
	puts("3. Cow echo");
	puts("4. Exit");	

	printf("\nSelect: ");
	fflush(stdout);
	check = scanf("%d", &num);
	if(check == 0){
		puts("Input must be integer!");
		fflush(stdout);
		exit(1);
	}

	return num;
}

void cow_fortune(void)
{
	system("/usr/games/fortune -s | /usr/games/cowsay");
}

void cow_time(void)
{
	system("/bin/date | /usr/games/cowsay");
}

void clear_stdin(void)
{
	int c;
	while ((c = getchar()) != '\n' && c != EOF);
}

void cow_echo(void)
{
	char message[256]={0};
	char cmd[1024]={0};

	printf("What do you want to say? ");
	fflush(stdout);
	clear_stdin();
	fgets(message, 256, stdin);
	snprintf(cmd, 1024, "/usr/games/cowsay -%c %s", cow_face[rand()%8], message);

	system(cmd);
}

void cow_exit(void)
{
	system("/usr/games/cowsay \'bye~\'");
	exit(0);
}
