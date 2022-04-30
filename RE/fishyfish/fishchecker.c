// gcc -o fishchecker -s
// pctf{f1Sh1ng_4_Y4te5_b4t3s_oR_h34venLy_G4t35}


#include <stdlib.h>
#include <stdio.h>



void swap(unsigned char* in, char a, char b) 
{ 
	if(a == b)
		return;
    unsigned char tempa = *in & (128 >> a); // val of in[a]
    unsigned char tempb = *in & (128 >> b); // val of in[b]
    *in = *in ^ (tempa | tempb); // empty bits to swap
    if(tempa)
    	*in = *in | (1 << (7 - b));
    if(tempb)
    	*in = *in | (1 << (7 - a));

}

void shuffle(unsigned char* in){
	for(int i = 7; i > 0; i--){
		int j = rand() % (i + 1);
		swap(in, (char) i, (char) j);
	}
}

int main(){
	char s[45] = {0};
	FILE *in = fopen("FISH_BAIT", "r");
	if(in == NULL){
		puts("No fish bait?");
		fflush(stdout);
		return 0;
	}
	fread(s, 1, 45, in);
	unsigned char a[45] = {0xeb, 0x46, 0xa7, 0x1, 0xc4, 0x5e, 0x88, 0x73, 0x30, 0xa0,
					   0x71, 0xa5, 0x51, 0x5a, 0x75, 0xb9, 0x18, 0xec, 0x76, 0x13,
					   0x9d, 0xee, 0x3, 0xb0, 0xa4, 0xed, 0x91, 0xf7, 0x24, 0xcd,
					   0x6, 0xe0, 0x30, 0x77, 0xe9, 0x17, 0xee, 0xfc, 0xfd, 0xe3,
					   0x3f, 0x67, 0xf8, 0x49, 0x54};
	srand(0xDEFEC8ED);
	//printf("{");
	for(int i = 0; i < sizeof(a); i++){
		shuffle((unsigned char *) &(s[i]));
		if((unsigned char)(s[i] ^ 0x2a) != a[i]){
			puts("Yucc, rotten fish");
			fflush(stdout);
			return 0;
		}
		//printf("0x%2x, ", (unsigned char) s[i] ^ (unsigned char) 0x2a);
	}
	//puts("}");
	puts("Yumm, fresh fish");
	fflush(stdout);

	return 0;
}

