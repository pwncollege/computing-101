import pwnlib.asm
import socket
import time
import sys
import os

allow_asm = True
num_instructions = 3

def check_disassembly(disas):
	assert disas[0].mnemonic == "mov" and disas[1].mnemonic == "mov", (
		"Your first two instructions must be 'mov' instructions: one to\n"
		"move a value into rdi, and one to move a value into rax.\n"
	)

	opnds1 = disas[0].op_str.split(", ")
	opnds2 = disas[1].op_str.split(", ")
	regs, vals = zip(opnds1, opnds2)
	assert set(regs) == { 'rax', 'rdi' }, (
		"You must set both the rax register and the rdi register!"
	)

	assert ( ['rax','0x3c'] in [ opnds1, opnds2 ] ), (
		"You must properly set the 'exit' system call number (60 in rax)!"
	)

	operation = disas[2].mnemonic
	assert operation == "syscall", (
		"Your last instruction should be the 'syscall' instruction to invoke\n"
		f"the exit system call, but you used the '{operation}' instruction!"
	)

	return True

def print_prompt():
	print(f"""hacker@{socket.gethostname()}:{
		os.getcwd().replace(os.path.expanduser('~'), '~', 1)
	}$ """, end="", flush=True)

def slow_print(what):
	for c in what:
		print(c, end="", flush=True)
		time.sleep(0.1)
	print("")

def dramatic_command(command, actual_command=None):
	print_prompt()
	slow_print(command)
	exit_code = os.waitstatus_to_exitcode(
		os.system(command if actual_command is None else actual_command)
	)
	time.sleep(0.5)
	return exit_code

def success(raw_binary):
	print("\033[92m", end='') # green
	print("Let's check what your exit code is! It should be 42 to succeed!")
	print("")
	print("Go go go!")
	print("\033[0m") # blank

	filename = "/tmp/your-program"
	os.rename(
		pwnlib.asm.make_elf(raw_binary, extract=False),
		filename
	)

	r = dramatic_command(filename)
	dramatic_command("echo $?", actual_command=f"echo {r}")
	dramatic_command("")

	if r == 42:
		print("\033[92m") # green
		print("Neat! Your program exited cleanly! Let's push on to make things")
		print("more interesting! Take this with you:")

		print("\033[0m", end="") # blank
		#pylint:disable=consider-using-with,unspecified-encoding
		print(open("/flag").read())
	else:
		print('\033[0;31m') # red
		print("Your program exited with the wrong error code. Please make sure")
		print(f"to set 'rdi' to 42 (you exited with '{r}'!")
		print("\033[0m", end="") # blank

