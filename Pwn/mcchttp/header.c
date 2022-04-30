#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "header.h"

Header* init_header()
{
    Header* header = malloc(sizeof(Header));
    if (header == NULL)
        goto fail;

    header->curr_capacity = 0;
    header->len = HEADER_INIT_SIZE;
    header->table = calloc((size_t)header->len, sizeof(HeaderEntry*));

    if(header->table == NULL)
    {
        puts("Failure to Allocate Memory");
        goto fail;
    }

    return header;

    fail:
        puts(HEADER_FAIL);
        exit(1);
}

void free_header(Header* h)
{
    int i;
    for(i=0; i < h->len; i++)
    {
        if(h->table[i])
        {
            free(h->table[i]->key);
            free(h->table[i]->value);

            h->table[i]->key = NULL;
            h->table[i]->value = NULL;

            free(h->table[i]);
            h->table[i] = NULL;
        }
    }
    free(h->table);
    h->table = NULL;
    free(h);
    h = NULL;
}

unsigned int hash(char* value, int size)
{
    int i;
    int length = strlen(value);
    unsigned int product = 1;
    for(i=0; i<length; i+=2)
    {
        // for odd lengthed strings, the value[i+1] where i==length it should be 0
        product *= (value[i] << 8) | value[i+1];
    }
    
    return product % size;
}

char* header_get(Header* header, char* key)
{
    if (header == NULL)
        goto fail;

    if (key == NULL)
        goto fail;
    
    unsigned int idx = hash(key, header->len);
    HeaderEntry* item = header->table[idx];
    int i = 2;
    while(item != NULL && strcmp(key, item->key))
    {
        idx = (idx + (i * i)) % header->len;
        item = header->table[idx];
        i++;
    }
     
    return item->value;

    fail:
        exit(1);
}

unsigned int header_put(Header* header, char* key, char* value)
{
    if (header == NULL)
        goto fail;

    if (key == NULL)
        goto fail;

    if (value == NULL)
        goto fail;

    if(header->curr_capacity >= header->len)
    {
        printf("Header at full capacity. Ignoring: <%s, %s>\n", key, value);
        return -1;
    }

    header->curr_capacity++;

    HeaderEntry* item = malloc(sizeof(HeaderEntry));
    
    if(item == NULL)
    {
        puts("Failure to Allocate Memory");
        goto fail;
    }

    item->key = malloc(strlen(key )+ 1);
    item->value = malloc(strlen(value) +1);
    strcpy(item->key, key);
    strcpy(item->value, value);

    unsigned int idx = hash(key, header->len);
    int i = 2;
    while(header->table[idx] != NULL)
    {
        idx = (idx + (i * i)) % header->len;
        i++;
    }
    header->table[idx] = item;
    return idx;

    fail:
        exit(1);
}