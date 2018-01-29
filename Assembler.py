import sys

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print("Incorrect number of arguments - ABORT")
		sys.exit()
	

	Input = sys.argv[1]
	Output = sys.argv[2]
	ASM = open(Input, 'r')
	BIN = open(Output, 'w')
	l = 0
	labels = {}

	for line in ASM.readlines():

		instr = 0
		
		#Label detection
		if line[-2] == ':':
			label = line.split(':')[0]
			labels[label] = l
			print(labels)


		#STOP detection
		elif line == "STOP":
			instr &= 0 << 31
			BIN.write('0x{:0>8x}\n'.format(instr))
			l += 1

		#Instruction analysis
		else:
			codeop, params = line.split(' ') #["Codeop"], ["R1,R2,R3\n"]
			params = params.split('\n')[0].split(',') #["R1", "R2", "R3"]


			#Encoding 3 arguments operations
			if (codeop in ["ADD", "SUB", "MULT", "DIV", "AND", "OR", "XOR", "SHL", "SHR", "SLT", "SLE", "SEQ", "LOAD", "STORE"]):
				
				if codeop == "ADD":
					instr += 1<< 27
				if codeop == "SUB":
					instr += 2<< 27	
				if codeop == "MULT":
					instr += 3<< 27
				if codeop == "DIV":
					instr += 4<< 27
				if codeop == "AND":
					instr += 5<< 27
				if codeop == "OR":
					instr += 6<< 27
				if codeop == "XOR":
					instr += 7<< 27
				if codeop == "SHL":
					instr += 8<< 27
				if codeop == "SHR":
					instr += 9<< 27
				if codeop == "SLT":
					instr += 10<< 27
				if codeop == "SLE":
					instr += 11<< 27
				if codeop == "SEQ":
					instr += 12<< 27
				if codeop == "LOAD":
					instr += 13<< 27
				if codeop == "STORE":
					instr += 14<< 27


				ra, rb = int(params[0][1:]), int(params[2][1:])
				#print("Source %i, Dest %i" %(ra, rb))
				instr += ra << 22
				instr += rb
				
				if params[1][0] == 'R':
					instr &= ~(1<<21) #imm bit to 0
					o = int(params[1][1:])
					#print("Add Reg %i" %(o))
				else :
					instr |= 1<<21 #imm bit to 1
					o = int(params[1])
					#print("Add immediate value %i" %(o))
				instr += o << 5

			if (codeop == "SCALL"):
				instr += 18<< 27
				instr += int(params[0]) #n parameter

			if (codeop in ["BRAZ", "BRANZ"]):
				
				if codeop == "BRAZ":
					instr += 16<< 27
				if codeop == "BRANZ":
					instr += 17<< 27

				if (params[1] in labels):
					a = labels[params[1]]
					print("Bra(n)z to label %s at address %d" %(params[1], labels[params[1]]))

				else:
					a = int(params[1])
				
				r = int(params[0][1:])
				instr += r << 22
				instr += a

			if (codeop == "JMP"):
				instr += 15<< 27

				#Convert label to address
				if (params[0] in labels):
					instr |= 1<<26 #imm bit to 1
					o = labels[params[0]]
					print("Jump to label %s at address %d" %(params[0], labels[params[0]]))
				elif params[0][0] == 'R':
					instr &= ~(1<<26) #imm bit to 0
					o = int(params[0][1:])
					print("Jump to address stored in register R%d" %(o))
				else :
					instr |= 1<<26 #imm bit to 1
					o = int(params[0])
					print("Jump to address %d" %(o))
				r = int(params[1][1:])
				instr += o << 5
				instr += r


			BIN.write('0x{:0>8x}\n'.format(instr))
			l += 1
