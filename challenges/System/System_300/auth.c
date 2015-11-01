// gcc -o auth auth.c -m32
#include <stdio.h>
#include <string.h>

int main(void)
{
	char user_password[256];
	char real_password[256];
	FILE *fp = NULL;
	
 	fp = fopen("/home/auth/password", "rt");
	if(fp == NULL){
		puts("fopen() error");
		return 1;
	}
	
	// read password from file
	memset(real_password, 0, 256);
	fgets(real_password, 256, fp);

	// read password from user
	printf("password: ");
	memset(user_password, 0, 256);
	scanf("%256s", user_password);

	puts("do not bruteforce...");
	sleep(time(0)%20);

	// check password!
	if(!strncmp(user_password, real_password, strlen(real_password))){
		puts("Great! Here is flag :)");
		system("/bin/cat flag");
	}
	else
		puts("Wrong :(");

	return 0;
}
