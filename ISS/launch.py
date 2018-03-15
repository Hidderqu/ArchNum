import os
import sys
import time

''' ----------------- Functions ---------------------- '''

def display_title():
	os.system("clear")
	print("\t>>>>>>>>>>>>>>>>>>>> ISS by Quentin HIDDERLEY & Alexandre HOUDEVILLE <<<<<<<<<<<<<<<<<<<\n")
	print("Type 'help' if you feel a bit lost...\n")

def display_help():
	print("\n")
	print("[+] ------ Help Section ------ [+]")
	print("install - Generates necessary files on first launch")
	print("load [FILE.asm] - Loads the assembler program FILE into myProgram.asm (MANDATORY)")
	print("run - Runs the ISS (remember to load a program first)")
	print("init [FILE.inm] - Loads a data initialization file into myInit.inm (optional)")
	print("showprg - Display current assembler program")
	print("showini - Display current initialization file")
	print("quit - Bye!")
	print("\n")
	input("Press Enter to exit the help section\n")

def prompt():
	ans = input(">>> ")
	return ans

''' ----------------- Running Functions ------------------------ '''
def install():
	os.system("make install")

def run():
	os.system("make run")
	input("\nPress Enter to exit")

def load(filePath):
	display_title()
	os.system("cp " + filePath + " ./myProgram.asm")
	time.sleep(3)

def init(filePath):
	display_title()
	os.system("cp " + filePath + " ./myInit.inm")
	time.sleep(3)

def showprg():
	print("\n")
	os.system("more " + "./myProgram.asm")
	input("\nPress Enter to exit")

def showini():
	print("\n")
	os.system("more " + "./myInit.inm")
	input("\nPress Enter to exit")

def quit():
	os.system("clear")
	sys.exit()

''' ------------- Function Dictionnary ----------------'''

index = {
	"help":display_help,
	"install":install,
	"run":run,
	"load":load,
	"init":init,
	"showprg":showprg,
	"showini":showini,
	"exit":quit,
	"q":quit,
	"quit":quit
}


''' -------------- Main ------------- '''

def main():
	while 1:
		display_title()
		ans = prompt()
		ans = ans.split(' ')
		try:
			if len(ans) == 2:
				index[ans[0]](ans [1])
			else:
				index[ans[0]]()
		except Exception as e:
			print("Invalid command " + "'" + ans[0] + "'")
			time.sleep(2)
		

if __name__ == "__main__":
	main()