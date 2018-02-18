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
	codes = {
		'ADD':1, 'SUB':2, 'MULT':3,
		'DIV':4, 'AND':5, 'OR':6,
		'XOR':7, 'SHL':8, 'SHR':9,
		'SLT':10, 'SLE':11, 'SEQ':12,
		'LOAD':13, 'STORE':14, 'JMP':15,
		'BRAZ':16, 'BRANZ':17, 'SCALL':18,
		'STOP':0
		}

	instrASM = ASM.readlines()


	#Label recording
	for line in instrASM:

		#Ignore blank lines
		if line == "\n":
			pass

		elif line[-2] == ':':
			label = line.split(':')[0]
			labels[label] = l
		else:
			l += 1
		
	print("Labels:", labels)



	
	#Instruction encoding
	for line in instrASM:

		instr = 0
		
		#Ignore blank lines
		if line == "\n":
			pass

		#Ingore labels
		elif line[-2] == ':':
			pass

		#STOP detection
		elif line == "STOP":
			print("Encoding STOP")
			instr = 0
			BIN.write('0x{:0>8x}\n'.format(instr))

		#Instruction analysis
		else:
			print("Encoding", line)
			codeop, params = line.split(' ') #["Codeop"], ["R1,R2,R3\n"]
			params = params.split('\n')[0].split(',') #["R1", "R2", "R3"]

			instr += codes[codeop] << 27


			#Encoding 3 arguments operations
			if (codeop in ["ADD", "SUB", "MULT", "DIV", "AND", "OR", "XOR", "SHL", "SHR", "SLT", "SLE", "SEQ", "LOAD", "STORE"]):
				
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


			
			#Encoding single argument operation
			if (codeop == "SCALL"):
				instr += int(params[0]) #n parameter

			


			#Encoding Bra(n)z type ops
			if (codeop in ["BRAZ", "BRANZ"]):
				
				#Convert label to address
				if (params[1] in labels):
					a = labels[params[1]]
					#print("Encoding Bra(n)z to label %s at address %d" %(params[1], labels[params[1]]))

				else:
					a = int(params[1])
				
				r = int(params[0][1:])
				instr += r << 22
				instr += a




			'''Encoding Jump type operation'''
			if (codeop == "JMP"):

				'''Convert label to address'''
				if (params[0] in labels):
					instr |= 1<<26 #imm bit to 1
					o = labels[params[0]]
					#print("Encoding Jump to label %s at address %d" %(params[0], labels[params[0]]))
				elif params[0][0] == 'R':
					instr &= ~(1<<26) #imm bit to 0
					o = int(params[0][1:])
					#print("Encoding Jump to address stored in register R%d" %(o))
				else :
					instr |= 1<<26 #imm bit to 1
					o = int(params[0])
					#print("Encoding Jump to address %d" %(o))
				r = int(params[1][1:])
				instr += o << 5
				instr += r




			BIN.write('0x{:0>8x}\n'.format(instr)) #Write encoded data
