#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>


#include "http.h"
#include "header.h"

int read_entire_file(char* path, char** buff)
{
    FILE* fp;
    long file_size;
    int bytes_read;

    fp = fopen(path, "rb");
    if(fp == NULL)
    {
        printf("Error Opening File: %s\n", path);
        return -1;
    }

    fseek(fp, 0, SEEK_END);
    file_size = ftell(fp);
    rewind(fp);

    *buff = malloc(sizeof(char) * file_size);
    if(*buff == NULL)
    {
        puts("Memory Error");
        exit(1);
    }    

    bytes_read = fread(*buff, 1, file_size, fp);
    if(bytes_read != file_size)
    {
        printf("Error Reading File: %s\n", path);
        exit(1);
    }

    fclose(fp);
    return file_size;
}

int handle_request(int conn_fd, int status, ReqLine* rl)
{
    StatusLine sl;
    Header* res_h;
    char* response;
    unsigned int response_len = 0;
    int free_space;
    char* body;
    int body_size;
    char content_len[12];
	// for level 2, turn index_page into a list of strings that gets loaded before the req header gets parsed.
	// header ptr is overwritten, and with header_put, write a key (or value) == flag.txt. carefully assign header_ptr, so the header write sits right on top of the list of pages
	// boom, it opens flag.txt instead of index.html
	//char index_page[];
    
    res_h = init_header();
    header_put(res_h, "Server", "mcchttp");
    header_put(res_h, "Content-Type", "text/html");
    
    if(status < 400)
    {
        if(!strcmp("/", rl->uri))
        {
            status = 200;
            body_size = read_entire_file("index.html", &body);
            
            if(body_size < 0)
            {
                free(body);
                body = NULL;
                status = 500;
            }
            
        }
		else if(!strcmp("/debug/status_line", rl->uri))
		{
			status = 200;
			body = malloc(sizeof(char) * 64);
			body_size = 64;
			snprintf(body, body_size, "%p %p %p", sl.version, sl.status_code, sl.reason_phrase);
		}
		else
        {
            status = 404;
        }
    }

    strcpy(sl.version, HTTP_VERSION);
    sl.status_code = status;
    switch(sl.status_code)
    {
        case 200:
            strncpy(sl.reason_phrase, MSG_200, REASON_PHRASE_SIZE);
            break;
        case 400:
            strncpy(sl.reason_phrase, MSG_400, REASON_PHRASE_SIZE);
            body = malloc(sizeof(char) * REASON_PHRASE_SIZE);
            body_size = REASON_PHRASE_SIZE;
            strcpy(body, MSG_400);
            break;
        case 404:
            strncpy(sl.reason_phrase, MSG_404, REASON_PHRASE_SIZE);
            body = malloc(sizeof(char) * REASON_PHRASE_SIZE);
            body_size = REASON_PHRASE_SIZE;
            strcpy(body, MSG_404);
            break;
        case 405:
            strncpy(sl.reason_phrase, MSG_405, REASON_PHRASE_SIZE);
            body = malloc(sizeof(char) * REASON_PHRASE_SIZE);
            body_size = REASON_PHRASE_SIZE;
            strcpy(body, MSG_405);
            break;
        case 500:
		default:
            strncpy(sl.reason_phrase, MSG_500, REASON_PHRASE_SIZE);
            body = malloc(sizeof(char) * REASON_PHRASE_SIZE);
            body_size = REASON_PHRASE_SIZE;
            strcpy(body, MSG_500);
            break;
    }
    printf("%s %d %s\n", sl.version, sl.status_code, sl.reason_phrase);
    snprintf(content_len, 11, "%d", body_size);
    header_put(res_h, "Content-Length", content_len);
    
    free_space = 2048 + body_size;
    response = malloc(sizeof(char) * free_space);

    response_len = snprintf(response, free_space, "%s %d %s\r\n", sl.version, sl.status_code, sl.reason_phrase);
    free_space -= response_len;
    int i;
    for(i=0; i<res_h->len; i++)
    {
        if(res_h->table[i])
        {
            response_len += snprintf(response + response_len, free_space, "%s: %s\r\n", res_h->table[i]->key, res_h->table[i]->value);
            free_space -= response_len;
        }
    }

    // If response line and header where > 1KB then allocate the necessary amount for the HTTP response
    if(free_space < body_size + 2)
    {
        response = realloc(response, response_len + body_size + 2);
        free_space = body_size + 2;
    }

	strcat(response + response_len, "\r\n");
    response_len += 2;

    memcpy(response + response_len, body, body_size);
    response_len += body_size;    

    send(conn_fd, response, response_len, 0);

    free_header(res_h);
    free(response);
    response = NULL;
    free(body);
    body = NULL;
    return 0;
}

char* parse_req_line(char* buff,  ReqLine* rl)
{        
    char* sp1 = strstr(buff, SP);
    if (sp1 == NULL) return NULL;
    if (sp1 - buff > 7) return NULL;

    // VULN: No Length check on URI parsing
    char* sp2 = strstr(sp1+1, SP);
    if (sp2 == NULL) return NULL;

    char* end = strstr(sp2+1, CRLF);
    if (end == NULL) return NULL;
    if (end-sp2 > 10) return NULL;

    strncpy(rl->method, buff, sp1-buff);
    strncpy(rl->uri, sp1+1, sp2-sp1-1);
    strncpy(rl->version, sp2+1, end-sp2-1);    

    return end+2;
}

char* parse_header(char* buff, Header* h)
{
    char* delimiter;
    char* crlf;
    int done = 0;
    int ret;
    char* pos = buff;

    do {
        delimiter = strstr(pos, FIELD_SEP);
        // If there is no field seperator, then there shouldn't be any more header fields
        if (delimiter == NULL)
            done = 1;

        crlf = strstr(delimiter, CRLF);
        // If there is no CRLF after a Field Seperator, then we have a malformed header field
        if (crlf == NULL)
            return NULL;

        // If another CRLF occurs after the last CRLF, then we at at the last header field
        if(crlf[2] == '\r' && crlf[3] == '\n')
            done = 1;

        int field_name_len = delimiter - pos;
        int value_len = crlf - (delimiter + 2);
        // We dont know size of header key/value at runtime, so allocat space to put the strings in
        char* key = malloc(sizeof(char) * field_name_len + 1);
        char* value = malloc(sizeof(char) * value_len + 1);
        strncpy(key, pos, field_name_len);
        strncpy(value, delimiter+2, value_len);
        // printf("%s %s\n", key, value);
        ret = header_put(h, key, value);
        free(key);
        free(value);
        key = NULL;
        value = NULL;
        
        pos = crlf+2;

    } while(!done);

    return pos;
}

int parse_request(int conn_fd, char* buff)
{
	ReqLine rl;
	//char buff[BUFF_LEN+1];
    //int bytes_read;
	//Header* h = NULL;
    char* pos = buff;
    int ret;
    int status = 200;

    puts("Received Connection");

    //h = init_header();
    bzero(&rl, sizeof(ReqLine));

    // Zero out Buffer and read data in
    //bzero(buff, BUFF_LEN+1);
    //bytes_read = recv(conn_fd, buff, BUFF_LEN, 0);
    
    //if(bytes_read < 0)
    //{
    //    status = 500;
    //    goto response;
    //}

    //pos = parse_header(pos, h);
    //if(pos == NULL)
    //{
    //    status = 400;
    //    goto response;
    //}

	// MUST OVERFLOW STATUS WITH 200? do we tho?
    pos = parse_req_line(pos, &rl);
    if(pos == NULL)
    {
        status = 400;
        goto response;
    }
        
    printf("Request Line:\n\tMETHOD: %s\n\tURI: %s\n\tVERSION: %s\n", rl.method, rl.uri, rl.version);

    if (strcmp(rl.method, "GET"))
    {
        status = 405;
        goto response;
    }

	//pos = strstr(pos, "\r\n\r\n");

    /*pos = parse_header(pos, h);
    if(pos == NULL)
    {
        status = 400;
        goto response;
    }*/
        
    /*puts("Headers:");
    int i;
    for(i=0; i < h->len; i++)
    {
        if(h->table[i])
            printf("\t%s: %s\n", h->table[i]->key, h->table[i]->value);
    }*/

    //if (pos[0] != '\r' || pos[1] != '\n')
    //{
    //    status = 400;
    //}
    
    response:
        ret = handle_request(conn_fd, status, &rl);

 //   free_header(h);
    return ret;

}

pid_t start_req_handler(int conn_fd)
{
	char buff[BUFF_LEN+1];
	int bytes_read;
	int status = 200;
	pid_t pid;
	pid = fork();

	// Child
	if(pid == 0)
	{
   		// Zero out Buffer and read data in
    	bzero(buff, BUFF_LEN+1);
    	bytes_read = recv(conn_fd, buff, BUFF_LEN, 0);
    
    	//if(bytes_read < 0)
    	//{
        //	status = 500;
		//}

		parse_request(conn_fd, buff);

		close(conn_fd);
	}

	return pid;
}


int run_server(int port)
{
    int sock_fd, conn_fd;
    struct sockaddr_in server_addr;

    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if(sock_fd < 0)
    {
        puts("Error creating listen socket");
        return 1;
    }

    bzero(&server_addr, sizeof(struct sockaddr_in));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);

    if (bind(sock_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0)
    {
        printf("Error Binding to Port: %d\n", port);
        return 1;
    }
    
    if(listen(sock_fd, LISTEN_QUEUE) < 0)
    {
        puts("Error Listening");
        return 1;
    }
    
    
    puts("Server Started");
    while(1)
    {
        int ret;
        conn_fd = accept(sock_fd, (struct sockaddr*)NULL, NULL);
        ret = start_req_handler(conn_fd);
		if(ret == 0)
		{
			puts("Connection Ended");
			return 0;
		}
        
    }

    close(sock_fd);
	return 0;
}

int main(int argc, char** argv)
{
    char* help = "Runs a very simple (and very not vulnerable?) HTTP Server on PORT";
    if(argc < 2)
    {
        printf("USAGE: %s PORT\n%s\n", argv[0], help);
        return 1;
    }
    int port = atoi(argv[1]);
    puts("Initializing mcchttp");
    return run_server(port);
}
