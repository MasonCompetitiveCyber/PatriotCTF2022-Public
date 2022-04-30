#include <stdlib.h>
#include <stdio.h>

#include "header.h"

int header_test()
{
    Header* h = init_header();

    int res1, res2 ,res3;

    header_put(h, "Connection", "Keep-Alive");
    header_put(h, "Content-Length", "283");
    header_put(h, "Pragma", "no-cache");

    res1 = !strcmp("Keep-Alive", header_get(h, "Connection"));
    res2 = !strcmp("283", header_get(h, "Content-Length"));
    res3 = !strcmp("no-cache", header_get(h, "Pragma"));

    return res1 | res2 | res3;
}


int main()
{
    puts("TESTS:");

    puts("header_test");
    if(header_test())
        puts("Pass");
    else
        puts("Failed");
}