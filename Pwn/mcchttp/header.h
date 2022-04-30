
#ifndef HEADER_H
#define HEADER_H

#define HEADER_INIT_SIZE 32
#define HEADER_FAIL "Failed to create Header"

#define FIELD_SEP ":"

typedef struct HeaderEntry
{
    char* key;
    char* value;
} HeaderEntry;

/*
 * Header is a sized hash table
 */
typedef struct Header
{
    HeaderEntry** table;
    int curr_capacity;
    int len;
} Header;

Header* init_header();
char* header_get(Header*, char*);
unsigned int header_put(Header*, char*, char*);
unsigned int hash(char*, int);
void free_header(Header*);

#endif