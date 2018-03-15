#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <sys/time.h>
#include<math.h>
#define TAILLE 30
#define NUM_REGS 32
#define TAILLEDATA 1024
#define TAILLE_MAX 1000

#define OFFSET_BITS 4 //(int)pow(2,2)
#define SET_BITS 64 //(int)pow(2,6)
#define TAG_BITS 2

int regs[ NUM_REGS ];
int unsigned program[TAILLEDATA];
int data[TAILLE];


typedef struct addr_sliced {
	int set;
	int tag;
	int offset;
} addr_sliced;


typedef struct line {
	int set;
	int valid;
	int tag;
	int bloc[OFFSET_BITS];
} line;


typedef struct Cache {
	line memoire[SET_BITS];
} Cache;

Cache ini_cache()
{	
	Cache cache_data;
	int i;
	int j;
	for (i=0 ;i<SET_BITS; i++)
	{
		cache_data.memoire[i].set = i;
		cache_data.memoire[i].valid = 0;
		cache_data.memoire[i].tag = 0;
		for (j=0 ; j<OFFSET_BITS ; j++)
		{
			cache_data.memoire[i].bloc[j] = 0;
		}
	}
	return cache_data;
}



Cache cache_data;

addr_sliced slice_addr(int addr)
{
	addr_sliced new_addr;
	new_addr.tag     = (addr & 0x300) >> 8;
	new_addr.set     = (addr & 0xFC ) >>  2;
	new_addr.offset  = (addr & 0x3 );
	return new_addr;
}






void write_to_cache(addr_sliced addr)
{
	line myline;
	myline.valid = 1;
	myline.tag = addr.tag;
	myline.set = addr.set;
	int i;
	int adresse = 0;
	adresse = (addr.tag << 9) + (addr.set << 2);
	for (i=0;i<OFFSET_BITS;i++)
	{
		myline.bloc[i] = data[adresse + i];
	}
	cache_data.memoire[addr.set] = myline;
}




void is_in_cache(addr_sliced addr)
{
	if (cache_data.memoire[addr.set].valid == 1 && addr.tag == cache_data.memoire[addr.set].tag)
	{
	printf("Cache hit\n");
	}
	else
	{
	write_to_cache(addr); 
	printf("Cache miss\n");
	}
}


int get_from_cache(int addr)
{	
	int info;
	addr_sliced new_addr = slice_addr(addr);
	is_in_cache(new_addr);
	info = (cache_data.memoire[new_addr.set]).bloc[new_addr.offset];
	return info;
}



void init(int argc, char const *argv[])
{
	int i;
	for (i = 0; i < TAILLEDATA; ++i)
	{
		program[i] = 0;
	}

	//BIN Reader
	FILE *file = fopen(argv[1], "r");

	i = 0;
	while((fscanf(file, "%x", &program[i])) != -1){
		i++;
		//printf("%x\n", program[i++%TAILLEDATA]);
}
	fclose(file);


	i = 0;
                            
}




/* program counter */
int pc = 0;

/* fetch the next word from the program */
int fetch()
	{
	  return program[ pc++ ];
	}

/* instruction fields */
int instrNum = 0;
int reg1     = 0;
int reg2     = 0;
int reg3     = 0;
int imm      = 0;
int imm_JMP  = 0;
int o_JMP  = 0;
int R_JMP  = 0;
int R_BRAZ  = 0;
int a_BRAZ  = 0;
int n  = 0;
/* decode a word */
void decode( int instr )
	{
	 instrNum = (instr & 0xF8000000) >> 27;
	 reg1     = (instr & 0x7C00000 ) >>  22;
	 reg2     = (instr & 0x1FFFE0 ) >>  5;
	 reg3     = (instr & 0x1F   );
	 imm      = (instr & 0x200000 ) >> 21;

	 imm_JMP  = (instr & 0x4000000 ) >> 26;
	 o_JMP    = (instr & 0x3FFFFE0 ) >> 5;
         R_JMP    = (instr & 0x1F );
         R_BRAZ   = (instr & 0x7C00000 ) >> 22;
         a_BRAZ   = (instr & 0x3FFFFF );
         n        = (instr & 0x7FFFFFF );

	// printf("instrNum : %d reg1 : %d\n", instrNum, reg1);
	}

/* the VM runs until this flag becomes 0 */
int running = 1;
/* evaluate the number of instructions done up to the end */
int performance = 0;
/* Temps initial defini ici pour eviter de compter le temps des scall */
clock_t debut;
/* evaluate the last decoded instruction */
void eval()
{
	int rea;
	char tab[10];
	switch( instrNum )
	  {
	    case 1:
	      /* add */

	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] + reg2;
		//printf( "add : r%d reçoit r%d + %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] + regs[ reg2 ];
		//printf( "add : r%d reçoit r%d + r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 2:
	      /* sub */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] - reg2;
		//printf( "sub : r%d reçoit r%d - %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] - regs[ reg2 ];
		//printf( "sub : r%d reçoit r%d - r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 3:
	      /* mult */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] * reg2;
		//printf( "mult : r%d reçoit r%d * %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] * regs[ reg2 ];
		//printf( "mult : r%d reçoit r%d * r%d\n", reg3, reg1, reg2 );
		}
	      performance += 2;
	      break;

	    case 4:
	      /* div */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] / reg2;
		//printf( "div : r%d reçoit r%d / %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] / regs[ reg2 ];
		//printf( "div : r%d reçoit r%d / r%d\n", reg3, reg1, reg2 );
		}
	      performance += 2;
	      break;

	    case 5:
	      /* and */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] & reg2;
		//printf( "and : r%d reçoit r%d & %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] & regs[ reg2 ];
		//printf( "and : r%d reçoit r%d & r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 6:
	      /* or */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] | reg2;
		//printf( "or : r%d reçoit r%d | %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] | regs[ reg2 ];
		//printf( "or : r%d reçoit r%d | r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 7:
	      /* xor */
	      
	      if (imm)
		{
		regs[ reg3 ] = reg2 ^ regs[ reg1 ];
		//printf( "xor : r%d reçoit r%d ^ %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg2 ] ^ regs[ reg1 ];
		//printf( "xor : r%d reçoit r%d ^ r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 8:
	      /* shl */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] << reg2;
		//printf( "shl : r%d reçoit r%d << %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] << regs[ reg2 ];
		//printf( "shl : r%d reçoit r%d << r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 9:
	      /* shr */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] >> reg2;
		//printf( "shr : r%d reçoit r%d >> %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] >> regs[ reg2 ];
		//printf( "shr : r%d reçoit r%d >> r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 10:
	      /* slt */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] < reg2;
		//printf( "slt : r%d reçoit r%d < %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] < regs[ reg2 ];
		//printf( "slt : r%d reçoit r%d < r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 11:
	      /* sle */
	      
	      if (imm)
		{
		regs[ reg3 ] = regs[ reg1 ] <= reg2;
		//printf( "sle : r%d reçoit r%d <= %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = regs[ reg1 ] <= regs[ reg2 ];
		//printf( "sle : r%d reçoit r%d <= r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 12:
	      /* seq */
	      
	      if (imm)
		{
		regs[ reg3 ] = (reg2 == regs[ reg1 ]);
		//printf( "seq : r%d reçoit r%d == %d\n", reg3, reg1, reg2 );
		}
	      else
		{
	        regs[ reg3 ] = (regs[ reg2 ] == regs[ reg1 ]);
		//printf( "seq : r%d reçoit r%d == r%d\n", reg3, reg1, reg2 );
		}
	      performance++;
	      break;

	    case 13:
	      /* load */
	      
	      if (imm)
		{
		regs[ reg3 ] = get_from_cache(regs[ reg1 ] + reg2);
		//regs[ reg3 ] = data[ regs[ reg1 ] + reg2 ];
		//printf( "load : r%d reçoit le contenu de l'adresse r%d + %d\n", reg3, reg1, reg2);
		}
	      else
		{
		regs[ reg3 ] = get_from_cache(regs[ reg1 ] + regs[ reg2 ]);
		//regs[ reg3 ] = data[ regs[ reg1 ] + regs[ reg2 ] ];
		//printf( "load : r%d reçoit le contenu de l'adresse r%d + r%d\n", reg3, reg1, reg2);
		}
	      performance++;
	      break;

	    case 14:
	      /* store */

	      if (imm)
		{
		data[ regs[ reg1 ] + reg2 ] = regs[ reg3 ];
		//printf( "store : le contenu de r%d est ecrit a l'adresse r%d + %d\n", reg3, reg1, reg2);
		}
	      else
		{
		data[ regs[ reg1 ] + regs [ reg2 ] ] = regs[ reg3 ];
		//printf( "store : le contenu de r%d est ecrit a l'adresse r%d + r%d\n", reg3, reg1, reg2);
		}
	      performance++;
	      break;

	    case 15:
	      /* jmp */
	      if (imm_JMP)
		{
		regs[ R_JMP ] = pc++;
		pc = o_JMP;
		//printf( "jmp : saute a l'adresse %d et stocke l'adresse de l'instruction suivant le jmp dans r%d\n", o_JMP, R_JMP );
		}
	      else
		{
		regs[ R_JMP ] = pc++;
		pc = regs[ o_JMP ];
		//printf( "jmp : saute a l'adresse r%d et stocke l'adresse de l'instruction suivant le jmp dans r%d\n", o_JMP, R_JMP );
		}
	      performance += 2;
	      break;


	    case 16:
	      /* braz */

	      if (regs[R_BRAZ] == 0)
		{
		pc = a_BRAZ;
		}
	      //printf( "braz : saute a l'adresse %d si r%d == 0 \n", a_BRAZ, R_BRAZ );
	      performance += 2;
	      break;

	    case 17:
	      /* branz */

	      if (regs[R_BRAZ] != 0)
		{
		pc = a_BRAZ;
		}
	      //printf( "branz : saute a l'adresse %d si r%d != 0 \n", a_BRAZ, R_BRAZ );	      
	      performance += 2;
	      break;

	    case 18:
	      /* scall */

	      //printf( "scall(n) n%d \n", n );

	      if (n == 0)
			{
			printf("Entrez une valeur : ");
			
			rea = strtol(fgets(tab,sizeof tab, stdin),NULL,10);
			
		        regs[1] = rea;
			debut = clock();
			}
	      else if (n == 1)
			{
			printf( "Affichage : %d \n", regs[1] );
			}
	      performance++;
	      break;

	    case 0:
	      /* stop */
	      printf( "End of program\n" );
	      running = 0;
	      performance++;
	      break;

  }
}

/* display all registers as 4-digit hexadecimal words */
void showRegs()
{
	int i;
	printf( "regs = " );
	for( i=0; i<NUM_REGS; i++ ){
		printf( "%04X ", regs[ i ] );
		printf( "\n" );
	}
}

void run()
{
	while( running )
		{
		//showRegs();
		int instr = fetch();
		decode( instr );
		eval();
		}
	//showRegs();
}

int main( int argc, const char * argv[] )
{ 
  cache_data = ini_cache();
  clock_t fin;
  debut = clock();
  init(argc, argv);
  run();
  fin = clock();
  double total_time = (double)(fin - debut)/CLOCKS_PER_SEC;
  double ops_per_sec = (double)performance/total_time;

  printf("Le programme effectue %d operations en %lf secondes soit une fréquence de %lf MHz\n", performance, total_time, ops_per_sec/10E6);
  return 0;
}
