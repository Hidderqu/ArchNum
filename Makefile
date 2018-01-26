default: ISS.c
	gcc -Wall ISS.c -o ISS.exe

assemble: Assembler.py ASM.txt
	more ASM.txt
	python3 Assembler.py ASM.txt BIN.txt
	more BIN.txt
	
runBIN: ISS.exe BIN.txt
	./ISS.exe BIN.txt

runASM:
	more ASM.txt
	make assemble
	make runBIN