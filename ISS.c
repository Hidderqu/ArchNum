#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#define TAILLE 30
#define NUM_REGS 32
#define TAILLEDATA 1024
#define TAILLE_MAX 1000


int regs[ NUM_REGS ];
int unsigned program[TAILLEDATA];
int data[TAILLE];


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
		printf("%x\n", program[i++%TAILLEDATA]);
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
/* evaluate the last decoded instruction */
void eval()
{
	int rea;
	char tab[10];
	switch( instrNum )
	  {
	    case 1:
	      /* add */
	      printf( "add r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] + regs[ reg2 ];
		printf("registre 3 : %d \n", regs[3]);
	      break;
	    case 2:
	      /* sub */
	      printf( "sub r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] - regs[ reg2 ];
	      break;
	    case 3:
	      /* mult */
	      printf( "mult r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] * regs[ reg2 ];
	      break;
	    case 4:
	      /* div */
	      printf( "div r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] / regs[ reg2 ];
	      break;
	    case 5:
	      /* and */
	      printf( "and r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] & regs[ reg2 ];
	      break;
	    case 6:
	      /* or */
	      printf( "or r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] | regs[ reg2 ];
	      break;
	    case 7:
	      /* xor */
	      printf( "xor r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg2 ] ^ regs[ reg1 ];
	      break;
	    case 8:
	      /* shl */
	      printf( "shl r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] << regs[ reg2 ];
	      break;
	    case 9:
	      /* shr */
	      printf( "shr r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] >> regs[ reg2 ];
	      break;
	    case 10:
	      /* slt */
	      printf( "slt r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] < regs[ reg2 ];
	      break;
	    case 11:
	      /* sle */
	      printf( "sle r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = regs[ reg1 ] <= regs[ reg2 ];
	      break;
	    case 12:
	      /* seq */
	      printf( "seq r%d r%d r%d\n", reg1, reg2, reg3 );
	      regs[ reg3 ] = (regs[ reg2 ] == regs[ reg1 ]);
	      break;
	    case 13:
	      /* load */
	      printf( "load r%d #%d\n", reg1, imm );
	      regs[ reg1 ] = imm;
	      break;
	    case 14:
	      /* store */
	      printf( "store r%d r%d r%d\n", reg1, reg2, reg3 );
	      break;
	    case 15:
	      /* jmp */
	      printf( "jmp o%d R%d\n", o_JMP, R_JMP );
	      
	      break;
	    case 16:
	      /* braz */
	      printf( "braz R%d a%d \n", R_BRAZ, a_BRAZ );

	      break;
	    case 17:
	      /* branz */
	      printf( "branz r%d r%d \n", R_BRAZ, a_BRAZ );

	      break;
	    case 18:
	      /* scall */

	      printf( "scall(n) n%d \n", n );

	      if (n == 0)
			{
			printf("Entrer une valeur : ");
			
			rea = strtol(fgets(tab,sizeof tab, stdin),NULL,10); //probleme lecture

printf(" rea : %d \n", rea);
			
		      regs[1] = rea;
			}
	      else if (n == 1)
			{
			printf( "affichage resultat : %d \n", regs[1] );
			}
	      break;
	    case 0:
	      /* stop */
	      printf( "stop\n" );
	      running = 0;
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
		showRegs();
		int instr = fetch();
		decode( instr );
		eval();
		}
	showRegs();
}

int main( int argc, const char * argv[] )
{ 
  init(argc, argv);
  run();
  return 0;
}
