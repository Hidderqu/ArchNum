import sys

if __name__ == "__main__":
	
	Input = sys.argv[1]
	Output = sys.argv[2]
	ASM = open(Input, 'r')
	BIN = open(Output, 'w')

	for line in ASM.readlines():
		codeop, params = line.split(' ')
		params = params.split('\n')[0].split(',')

		# Encoding ADD
		instr = 0
		if codeop == "ADD":
			instr += 2<< 27
			
			
			ra, rb = int(params[0][1]), int(params[2][1])
			instr += ra << 22
			instr += rb
			
			if params[1][0] == 'R':
				instr &= ~(1<<21)
				o = int(params[1][1])
			else :
				instr |= 1<<21
				o = int(params[1][0])
			instr += o << 5
			
		BIN.write((hex(instr)))
		BIN.write('\n')




