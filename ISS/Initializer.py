import sys

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print("Incorrect number of arguments - ABORT")
		sys.exit()
	

	Input = sys.argv[1]
	Output = sys.argv[2]
	ASM = open(Input, 'r')
	BIN = open(Output, 'w')

	instrASM = ASM.readlines()

	for line in instrASM:

		#Ignore blank lines
		if line == "\n":
			pass
		else:
			mem, val = line.split(':')
			instr = 0
			instr += 1 << 27 #ADD instruction
			instr += 1 #Destination register
			instr |= 1<<21 #Imm bit to 1
			instr += int(val) << 5 #Value to give to register

			BIN.write('0x{:0>8x}\n'.format(instr)) #ADD R0,val,R1

			instr = 0
			instr += 14 << 27 #STORE instruction
			instr += 1 #Source register
			instr |= 1<<21 #Imm bit to 1
			instr += int(mem) << 5 #Memory address

			BIN.write('0x{:0>8x}\n'.format(instr)) #STORE R0,mem,R1

			#print("Initialized memory space {} with value {}".format(mem, val))

	instr = 0
	instr += 1 << 27 #ADD instruction
	instr += 1 #Destination register
	instr |= 1<<21 #Imm bit to 1
	instr += 0 << 5 #Value to give to register

	BIN.write('0x{:0>8x}\n'.format(instr)) #ADD R0,0,R1 (R1 back to 0)
	BIN.write('0x{:0>8x}\n'.format(0)) #ADD R0,0,R1 (R1 back to 0)

	print("Generated a memory initialization binary")