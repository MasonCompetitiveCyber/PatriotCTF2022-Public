
#ifndef HTTP_H
#define HTTP_H

#include "header.h"

#define CRLF "\r\n"
#define HTTP_VERSION "HTTP/1.1"

#define LISTEN_QUEUE 15

#define BUFF_LEN 1024
#define SP " "

#define REASON_PHRASE_SIZE 32
#define RES_BODY_SIZE 4096

#define GET_ONLY "Sorry, I only handle GET requests."
#define FILE_NOT_FOUND "404 File Not Found. Thanks for visiting! But our Flag is in another castle!"

#define MSG_100 "Continue"
#define MSG_101 "Switching Protocols"
#define MSG_200 "OK"
#define MSG_201 "Created"
#define MSG_202 "Accepted"
#define MSG_203 "Non-Authoritative Information"
#define MSG_204 "No Content"
#define MSG_205 "Reset Content"
#define MSG_206 "Partial Content"
#define MSG_300 "Multiple Choices"
#define MSG_301 "Moved Permanently"
#define MSG_302 "Found"
#define MSG_303 "See Other"
#define MSG_304 "Not Modified"
#define MSG_305 "Use Proxy"
#define MSG_307 "Temporary Redirect"
#define MSG_400 "Bad Request"
#define MSG_401 "Unauthorized"
#define MSG_402 "Payment Required"
#define MSG_403 "Forbidden"
#define MSG_404 "Not Found"
#define MSG_405 "Method Not Allowed"
#define MSG_406 "Not Acceptable"
#define MSG_407 "Proxy Authentication Required"
#define MSG_408 "Request Time-out"
#define MSG_409 "Conflict"
#define MSG_410 "Gone"
#define MSG_411 "Length Required"
#define MSG_412 "Precondition Failed"
#define MSG_413 "Request Entity Too Large"
#define MSG_414 "Request-URI Too Large"
#define MSG_415 "Unsupported Media Type"
#define MSG_416 "Requested range not satisfiable"
#define MSG_417 "Expectation Failed"
#define MSG_500 "Internal Server Error"
#define MSG_501 "Not Implemented"
#define MSG_502 "Bad Gateway"
#define MSG_503 "Service Unavailable"
#define MSG_504 "Gateway Time-out"
#define MSG_505 "HTTP Version not supported"



typedef struct ReqLine
{
    char method[8];
    char uri[128];
    char version[12];
} ReqLine;

typedef struct StatusLine
{
    char version[10];
    int status_code;
    char reason_phrase[REASON_PHRASE_SIZE];
} StatusLine;


#endif
