
#include <stdio.h>

#define HIDE_LETTER(a)   (a) + 0x50
#define UNHIDE_STRING(str)  do { char * ptr = str ; while (*ptr) *ptr++ -= 0x50; } while(0)
#define HIDE_STRING(str)  do {char * ptr = str ; while (*ptr) *ptr++ += 0x50;} while(0)

int main()
{


    // store the "secret password" as mangled byte array in binary
        char flag[] = { HIDE_LETTER('P') , HIDE_LETTER('C') , HIDE_LETTER('T') , HIDE_LETTER('F') , HIDE_LETTER('{') 
        , HIDE_LETTER('8') , HIDE_LETTER('y') , HIDE_LETTER('p') , HIDE_LETTER('4') , HIDE_LETTER('5'),
                HIDE_LETTER('5') ,HIDE_LETTER('_') ,HIDE_LETTER('h') ,HIDE_LETTER('4') ,HIDE_LETTER('2'), HIDE_LETTER('d'),
                HIDE_LETTER('_'), HIDE_LETTER('c'), HIDE_LETTER('0'), HIDE_LETTER('d'), HIDE_LETTER('3'), HIDE_LETTER('d'),
                HIDE_LETTER('_'),HIDE_LETTER('v'),HIDE_LETTER('4'),HIDE_LETTER('1'),HIDE_LETTER('u'),HIDE_LETTER('3'),HIDE_LETTER('5'),HIDE_LETTER('}'),'\0' }; 


    int health = 1000;
    int stupidHumanOpinion;
    int exit;

    printf("I am the mighty Robo-Tron9000. If my health is less or equal to zero, I will die and give you the flag. \n");
    printf("Why don\'t you go ahead and tell me what my health should be?\n");
    scanf("%d",&stupidHumanOpinion);
    if (health < 1) 
    {

       printf("BLARGH!!!\n");
       printf("Fine, you earned it; here\'s your flag: \n");

       UNHIDE_STRING(flag);  // unmangle the string in-place
       printf("%s\n", flag);
       HIDE_STRING(flag);  //mangle back
    }
    else 
    {
        printf("HA! I DONT CARE!!!\n");
        printf("MY HEALTH IS: %d AND IT IS STAYING THAT WAY!\n",health);
    }
    printf("Press enter to exit");
    scanf("%c",&exit);
    scanf("%c",&exit);
    

    return 0;
}




    

    

