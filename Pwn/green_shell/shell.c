#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define BUF_SIZE 256
#define SHELL_PRFX "GShll> "
#define HELP_MSG "Valid Commands: ls, whoami, help\n"

int check_cmd(char* input)
{
    char* pos;
    int found_first=0;
    char argv1[32]; 
    int count = 0;

    memset(argv1, 0, 32);

    for(pos=input; *pos; pos++)
    {
        if (found_first)
        {
            if(isspace(*pos))
            {
                break;
            }else
            {
                argv1[count] = *pos;
                count++;
                if (count == 31)
                {
                    break;
                }
            }
        }else
        {
            if(!isspace(*pos))
            {
                found_first=1;
                argv1[count] = *pos;
                count++;
                if (count == 31)
                {
                    break;
                }
            }
        }
    }

    if (!strcmp(argv1, "ls"))
        return 0;
    if (!strcmp(argv1, "whoami"))
        return 0;
    if (!strcmp(argv1, "help"))
        return 0;

    return 1;

}

int handle_cmd(char* input)
{
    pid_t pid;
    int child_status;

    if (input[0] == '\n')
    {
        return 0;
    }
    
    if (check_cmd(input))
    {
        puts(HELP_MSG);
        return -1;
    }

    if (!strcmp(input, "help\n"))
    {
        puts(HELP_MSG);
        return 0;
    }

    pid = fork();
    if(pid == 0)
    {
        if(execlp("/bin/bash", "/bin/bash", "-c", input, (char*)NULL) == -1)
        {
            printf("An error running \"%s\" has occured\n", input);
            exit(-1);
        }
    }else
    {
        wait(&child_status);
        return child_status;    
    }

}

int main(int argc, char** argv)
{
	setvbuf(stdout, NULL, _IONBF, 0);
    char input[BUF_SIZE];
    int ret = 0;
    while(1)
    {
        printf("%s", SHELL_PRFX);
        fgets(input, BUF_SIZE, stdin);
        
        ret = handle_cmd(input);
    }
}

