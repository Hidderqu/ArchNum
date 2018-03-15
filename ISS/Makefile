default:
	make IniRun


Recompile: ISS.c
	gcc -Wall ISS.c -o ISS.exe


assemble: Assembler.py ASM.txt
	python3 Assembler.py ASM.txt BIN.txt

initRegs: Initializer.py initASM.txt
	python3 Initializer.py initASM.txt initBIN.txt


IniRun: ISS.exe
	make initRegs
	make assemble
	./ISS.exe BIN.txt initBIN.txt

Run: ISS.exe
	make assemble
	./ISS.exe BIN.txt