import __main__ as checker
import random
import re

#pylint:disable=global-statement

allow_asm = True
give_flag = True
returncode = None
secret_value = random.choice(list(set(range(15, 250))-{100}))
assembly_prefix = f"""
    mov r9, 0x0
    mov r8, 0xffffffff
    mov r10, 0x32
    mov rdx, 0x3
    mov rsi, 0x1000
    mov rdi, 0
    mov rax, 9
    syscall
	mov byte ptr [100], {secret_value}
"""
num_instructions = 3

check_runtime_prologue = """
\033[92mLet's check what your exit code is! It should be our secret
value stored at memory address 100 (value {secret_value}) to succeed!

Go go go!
\033[0m
""".strip()

check_runtime_success = """
\033[92m
Neat! Your program exited with the correct error code! You have
performed your first memory read. Great job!

\033[0m
""".strip()

check_runtime_failure = """
\033[0;31m
Your program exited with the wrong error code. Please make sure
to move the memory at address 100 into 'dil'.
""".strip()

def check_disassembly(disas):
	assert disas[0].mnemonic == "mov" and disas[1].mnemonic == "mov", (
		"Your first two instructions must be 'mov' instructions: one to\n"
		"move a value from memory into dil, and one to move a value into al.\n"
	)

	opnds1 = disas[0].op_str.split(", ")
	opnds2 = disas[1].op_str.split(", ")
	regs, _ = zip(opnds1, opnds2)
	assert set(regs) == { 'al', 'dil' }, (
		"You must set both the al register and the dil register!"
	)

	assert ( ['al','0x3c'] in [ opnds1, opnds2 ] ), (
		"You must properly set the 'exit' system call number (60 in al)!"
	)

	dil_opnd = opnds1[1] if opnds2[0] == 'al' else opnds2[1]

	assert dil_opnd != "0x64", (
		"You are moving the value 100 into dil, not the data stored at the memory\n"
		"addressed by the address 100! Please use the [ADDRESS] syntax to denote\n"
		"the actual memory address (in this case, ADDRESS should be 100)."
	)
	assert dil_opnd.startswith("byte ptr ["), (
		"You are not moving a value from memory to dil. You must use the '[ADDRESS]'\n"
		"syntax to do this. In this case, I've stored the secret value at the\n"
		"ADDRESS of 100."
	)
	assert re.match(r"byte ptr \[\w+\]", dil_opnd), (
		"In this level, please use the address 100 directly for the memory address.\n"
		"We will learn more advanced ways of addressing memory later."
	)


	operation = disas[2].mnemonic
	assert operation == "syscall", (
		"Your last instruction should be the 'syscall' instruction to invoke\n"
		f"the exit system call, but you used the '{operation}' instruction!"
	)

	return True

def check_runtime(filename):
	global returncode
	returncode = checker.dramatic_command(filename)
	checker.dramatic_command("echo $?", actual_command=f"echo {returncode}")
	checker.dramatic_command("")
	assert returncode == secret_value
