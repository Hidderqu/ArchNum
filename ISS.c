#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


int main(int argc, char const *argv[])
{

	int program[32];
	for (int i = 0; i < 32; ++i)
	{
		program[i] = 0;
	}

	//BIN Reader
	int fd = open(argv[1], O_RDONLY);
	char *buff = (char *) malloc(8);


	int i = 0;
	while(read(fd, buff, 8) != 0){
		//printf("Read %s\n", buff);
		int n = strtol(buff, NULL, 16);
		program[i++%32] = n;
	}


	/*
	for (int i = 0; i < 32; ++i)
	{
		printf("%d\n", program[i]);
	}
	*/

	return 0;
}