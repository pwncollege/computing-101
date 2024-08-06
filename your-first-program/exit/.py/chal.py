import pwnlib.asm
import socket
import time
import sys
import os

allow_asm = True
num_instructions = 2

def check_disassembly(disas):
	operation = disas[0].mnemonic
	assert operation == "mov", (
		"Your first instruction's operation must be 'mov', "
		f"but yours was {operation}."
	)

	opnd1, opnd2 = disas[0].op_str.split(", ")
	assert opnd1 == "rax", (
		"You must move your system call index to the 'rax' register, "
		f"but you are moving to {opnd1}."
	)

	try:
		assert int(opnd2, 0) == 60, (
			"You must move the syscall index of exit (60) into rax, "
			f"whereas you moved {int(opnd2, 0)}."
		)
	except ValueError as e:
		if opnd2.startswith("r"):
			raise AssertionError(
				"It looks like you are trying to move values from one register\n"
				"to another, rather than specifying a number to move to rax.\n"
				"Try moving 60 to rax!"
			) from e
		raise AssertionError(
			"You must move the syscall index of exit (60) into rax, whereas\n"
			f"you instead specified {opnd2}."
		) from e

	operation = disas[1].mnemonic
	assert operation == "syscall", (
		"Your second instruction should be the 'syscall' instruction to invoke\n"
		f"the exit system call, but you used the '{operation}' instruction!"
	)

	return True

def success(raw_binary):
	print("\033[92m", end='') # green
	print("Okay, now you have written your first COMPLETE program!")
	print("All it'll do is exit, but it'll do so cleanly, and we can")
	print("build from there!")
	print("")
	print("Let's see what happens when you run it:")
	print("\033[0m") # blank

	filename = "/tmp/your-program"
	os.rename(
		pwnlib.asm.make_elf(raw_binary, extract=False),
		filename
	)
	print(f"""hacker@{socket.gethostname()}:{
		os.getcwd().replace(os.path.expanduser('~'), '~', 1)
	}$ """, end="")
	for c in filename:
		print(c, end="")
		time.sleep(0.1)
		sys.stdout.flush()
	print("")
	time.sleep(0.5)
	print(f"""hacker@{socket.gethostname()}:{
		os.getcwd().replace(os.path.expanduser('~'), '~', 1)
	}$ """)
	time.sleep(0.5)

	print("\033[92m") # green
	print("Neat! Your program exited cleanly! Let's push on to make things")
	print("more interesting! Take this with you:")
	print("\033[0m") # blank
	#pylint:disable=consider-using-with,unspecified-encoding
	print(open("/flag").read())
