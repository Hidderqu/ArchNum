#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define TAILLEDATA 1024


int main(int argc, char const *argv[])
{

	unsigned int program[32];
	for (int i = 0; i < 32; ++i)
	{
		program[i] = 0;
	}

	//BIN Reader
	FILE *file = fopen(argv[1], "r");

	int i = 0;
	while((fscanf(file, "%x", &program[i])) != -1){
		printf("%x\n", program[i++%TAILLEDATA]);
	}

	return 0;
}