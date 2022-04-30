#include <stdlib.h>
#include <stdio.h>

//gcc -o flowing flowing.c
//pctf{Wh3rEf0R3_Art_Th0u_0v3rFlOw}

void main(){
    char inputNum[9];
    int seed;
    char inBytes[65535];
    char flag[34];
    //int hops[] = {50796, 30457, 14434, 55025, 31170, 47786, 24190, 9827, 32329, 10788, 40649, 28567, 16878, 53733, 52042, 65218, 37300, 3570, 64766, 28531, 5078, 56962, 46543, 24089, 65171, 17493, 33791, 26604, 44545, 49052, 22635, 37376, 55570};

    FILE *infile = fopen("inbytes", "r");
    fread(inBytes, 1, 65535, infile);
    fclose(infile);

    printf("Input number in hex with no leading 0x (max num ffffffff): ");
    puts("\n");
    fgets(inputNum, 9, stdin);
    seed = (int) strtol(inputNum, NULL, 16);
    seed = abs(seed) % 65535;
    for(int i = 0; i < 33; i++){
        flag[i] = inBytes[seed];
        seed = (abs(seed * flag[i] * (0xb33f * -1))) % 65535;
    }
    flag[33] = '\0';
    printf("Here is your flag: %s", flag);
}