#include <stdio.h>
#include <unistd.h>


void stack() {

	printf( "\n"
			"------------------------------------------------------------------\n"
            "                              SBOaaS                              \n"
			"------------------------------------------------------------------\n"
			"\n"
			"Welcome to Stack Buffer Overflow as a Service\n"
            "\n"
			"Since modern mitigations made it more difficult to exploit vulnerabilities,\n"
            "we decided to offer an easy and convenient service for everyone\n"
            "to experience the joy of exploiting a stack-based buffer overflow.\n"
            "Simply enter your data and win!\n"
            "\n");

    printf("Please enter your data. Good luck!\n> ");
    
    char buf[1337];
    gets(buf);

}



void spawn_shell() {
    char* args[] = {(char*)"/bin/bash", NULL};
    execve("/bin/bash", args, NULL);
}

int main(int argc, char* argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);

    stack();
    printf("Thank you for using SBOaaS :)\n");
    
    return 0;
}
