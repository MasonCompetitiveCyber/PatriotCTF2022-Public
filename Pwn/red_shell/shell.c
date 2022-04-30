#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

#define BUF_SIZE 256
#define MAX_ARGS 8
#define SHELL_PRFX "RShll> "

// #include <errno.h>

// extern int errno;

int parse_cmd(char** argv, char* input)
{
    char* pos;
    int found_tok = 0;
    int argc = 0;
    char* curr_arg;
    int arg_pos;

    for(pos=input; *pos; pos++)
    {
        if (found_tok)
        {
            if (isspace(*pos))
            {
                found_tok = 0;
                curr_arg[arg_pos] = '\0';
                if (argc == MAX_ARGS)
                    break;
            }
            else
            {
                curr_arg[arg_pos] = *pos;
                arg_pos++;
                if (arg_pos == BUF_SIZE-1)
                {
                    found_tok = 0;
                    curr_arg[arg_pos] = '\0';
                }

            }   
        }
        else
        {
            if (!isspace(*pos))
            {
                // Token Start
                found_tok = 1;
                argv[argc] = calloc(BUF_SIZE, sizeof(char));
                curr_arg = argv[argc];
                arg_pos = 0;
                curr_arg[arg_pos] = *pos;
                arg_pos++;
                argc++;
            }
        }
    }

    return argc;
}


// Restrict user into cwd (no cd)
// Create directory on run?
// Restrict reads outside of cwd (no cat)
// commands cannot start with .. or /
// Implement stdout redirect
	// destination cannot start with .. or /
// Write a script with a Shebang -> giving them a full shell i.e. /bin/sh

int handle_stdout_redirect(int argc, char** argv, int* fd)
{
    char* arg;
    char* target_file;
    int found = 0;
    int count = 0;
    int i;

    if(argv[0][0] == '.' && argv[0][1] == '.')
    {
        goto naughty_cmd;
    }

    if(argv[0][0] == '/')
    {
        goto naughty_cmd;
    }

    // for(arg = *argv; arg; arg=*(++argv))
    for(i = 0; i < argc; i++)
    {

        if(!strcmp(argv[i], ">"))
        {
            if(i < MAX_ARGS-1)
            {
                found = 1;
                target_file = argv[i+1];
                if(target_file[0] == '/')
                {
                    goto naughty_cmd;
                }

                if(target_file[0] == '.' && target_file[1] == '.')
                {
                    goto naughty_cmd;
                }

                *fd = open(target_file, O_WRONLY | O_CREAT | O_TRUNC, 0777);
                dup2(*fd, STDOUT_FILENO);
                close(*fd);

                argc -= 2;
                free(argv[i]);
                free(argv[i+1]);
                argv[i] = NULL;
                argv[i+1] = NULL;

                return 1;

            }else
            {
                puts("STDOUT redirect cannot be last in argv");
                return 0;
            }
        }
        // count++;
    }

    return 1;

naughty_cmd:
    puts("Access Restricted");
    return 0;

}

void print_cmd(char** argv)
{
    char* cur_arg;
    for(cur_arg = *argv; cur_arg; cur_arg=*(++argv))
    {
        printf("%s ", cur_arg);
    }
    printf("\n");
}

int handle_cmd(char* input)
{
    pid_t pid;
    int child_status;
    char* argv[MAX_ARGS + 1];
    int argc;
    int rdir_stdout;
    int i;

    rdir_stdout = -1;
    memset(argv, 0, sizeof(char*) * MAX_ARGS);

    if (input[0] == '\n')
    {
        return 0;
    }
    
    argc = parse_cmd(argv, input);

    if(!strcmp(argv[0], "exit"))
    {
        for(i = 0; i < argc; i++)
        {
            free(argv[i]);
            argv[i] = NULL;
        }
        exit(0);
    }

    // print_cmd(argv);
    pid = fork();
    if(pid == 0)
    {
        if(handle_stdout_redirect(argc, argv, &rdir_stdout))
        {
            execv(argv[0], argv);
            printf("Could not execute %s\n", argv[0]);
            // printf("%s\n", strerror(errno));
        }

        close(rdir_stdout);
        for(i=0;i<argc; i++)
        {
            free(argv[i]);
            argv[i]=NULL;
        }
        
    }else
    {
        wait(&child_status);
        if (rdir_stdout != -1)
            close(rdir_stdout);
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

    
