import __main__ as checker
import random
import re

from chalconf import secret_addr, secret_reg
#pylint:disable=global-statement

allow_asm = True
give_flag = True
returncode = None
secret_value = random.randint(15, 255)
page_addr = secret_addr - secret_addr%0x1000
num_instructions = 3

assembly_prefix = f"""
    mov r9, 0x0
    mov r8, 0xffffffff
    mov r10, 0x32
    mov rdx, 0x3
    mov rsi, 0x1000
    mov rdi, {page_addr}
    mov rax, 9
    syscall
	mov byte ptr [{secret_addr}], {secret_value}
"""
if secret_reg:
	assembly_prefix += f"mov {secret_reg}, {secret_addr}\n"

if secret_reg:
	check_runtime_prologue = """
\033[92mLet's check what your exit code is! It should be our secret
value pointed to by {secret_reg} (value {secret_value}) to succeed!

Go go go!
\033[0m
	""".strip()
else:
	check_runtime_prologue = """
\033[92mLet's check what your exit code is! It should be our secret
value stored at memory address {secret_addr} (value {secret_value}) to succeed!

Go go go!
\033[0m
	""".strip()

check_runtime_success = """
\033[92m
Neat! Your program exited with the correct error code! You have
performed your first memory read. Great job!

\033[0m
""".strip()

if secret_reg:
	check_runtime_failure = f"""
\033[0;31m
Your program exited with the wrong error code. Please make sure
to move the memory pointed to by {secret_reg} into 'rdi'.
	""".strip()
else:
	check_runtime_failure = f"""
\033[0;31m
Your program exited with the wrong error code. Please make sure
to move the memory at address {secret_addr} into 'rdi'.
	""".strip()

def check_disassembly(disas):
	assert disas[0].mnemonic == "mov" and disas[1].mnemonic == "mov", (
		"Your first two instructions must be 'mov' instructions: one to\n"
		"move a value from memory into rdi, and one to move a value into rax.\n"
	)

	opnds1 = disas[0].op_str.split(", ")
	opnds2 = disas[1].op_str.split(", ")
	regs, srcs = zip(opnds1, opnds2)
	assert set(regs) == { 'rax', 'rdi' }, (
		"You must set both the rax register and the rdi register!"
	)

	assert ( ['rax','0x3c'] in [ opnds1, opnds2 ] ), (
		"You must properly set the 'exit' system call number (60 in rax)!"
	)

	rdi_opnd = opnds1[1] if opnds2[0] == 'rax' else opnds2[1]

	assert (not secret_reg) or not (regs[0] == secret_reg and secret_reg not in srcs[0]), (
		f"Uh oh! It looks like you're overwriting the value in {regs[0]} in your\n"
		"first instruction. Once you overwrite this value, you will lose the secret\n"
		"address that we initialized it with! Dereference it first before overwriting\n"
		"it.\n"

	)

	assert rdi_opnd != hex(secret_addr), (
		f"You are moving the value {secret_addr} into rdi, not the data stored at the memory\n"
		f"addressed by the address {secret_addr}! Please use the [ADDRESS] syntax to denote\n"
		f"the actual memory address (in this case, ADDRESS should be {secret_addr})."
	)
	assert rdi_opnd.startswith("qword ptr ["), (
		"You are not moving a value from memory to rdi. You must use the '[ADDRESS]'\n"
		"syntax to do this. In this case, I've stored the secret value at the\n"
		f"ADDRESS of {secret_addr}."
	)
	if secret_reg:
		assert re.match(r"qword ptr \[\w+\]", rdi_opnd), (
			f"In this level, please dereference the register {secret_reg} to use the\n"
			"memory address stored there."
		)
	else:
		assert re.match(r"qword ptr \[\w+\]", rdi_opnd), (
			f"In this level, please use the address {secret_addr} directly for the memory address.\n"
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
	#pylint:disable=c-extension-no-member
	returncode = checker.dramatic_command(filename)
	checker.dramatic_command("echo $?", actual_command=f"echo {returncode}")
	checker.dramatic_command("")
	assert returncode == secret_value
