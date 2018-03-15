default:
	make run -s

recompile: ISS.c
	gcc -Wall ISS.c -o ISS.exe

blankMem:
	touch myInit.inm

blankProg:
	touch myProgram.asm



initRegs: Initializer.py myInit.inm
	python3 Initializer.py myInit.inm myInit.bin

assemble: Assembler.py myProgram.asm
	python3 Assembler.py myProgram.asm myProgram.bin


install:
	make recompile -s
	make blankProg -s
	make blankMem -s


run: ISS.exe
	@make initRegs -s
	@make assemble -s
	@./ISS.exe myProgram.bin myInit.bin