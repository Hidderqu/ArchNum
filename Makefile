default: ISS.c
	gcc -Wall ISS.c -o ISS.exe

assemble: Assembler.py ASM.txt
	python3 Assembler.py ASM.txt BIN.txt
	
runBIN: ISS.exe BIN.txt
	./ISS.exe BIN.txt

runASM:
	make assemble
	make runBIN