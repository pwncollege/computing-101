import __main__ as checker
import random
import re

import chalconf #pylint:disable=import-error
secret_addr = getattr(chalconf, 'secret_addr', None)
known_addr = getattr(chalconf, 'known_addr', None)
secret_reg = getattr(chalconf, 'secret_reg', None)
num_instructions = getattr(chalconf, 'num_instructions', 3)

#pylint:disable=global-statement

allow_asm = True
give_flag = True
returncode = None

secret_value = random.randint(15, 255)

assembly_prefix = f"""
    mov r9, 0x0
    mov r8, 0xffffffff
    mov r10, 0x32
    mov rdx, 0x3
    mov rsi, 0x1000
    mov rdi, {secret_addr-secret_addr%0x1000}
    mov rax, 9
    syscall
	mov byte ptr [{secret_addr}], {secret_value}
"""
if secret_reg:
	assembly_prefix += f"mov {secret_reg}, {secret_addr}\n"
if known_addr:
	assembly_prefix += f"""
    	mov r9, 0x0
    	mov r8, 0xffffffff
    	mov r10, 0x32
    	mov rdx, 0x3
    	mov rsi, 0x1000
    	mov rdi, {known_addr-known_addr%0x1000}
    	mov rax, 9
    	syscall
		mov qword ptr [{known_addr}], {secret_addr}\n
	"""

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
to move the value at memory address {secret_addr} into 'rdi'.
	""".strip()

def check_disassembly(disas):
	if num_instructions == 3:
		assert disas[0].mnemonic == "mov" and disas[1].mnemonic == "mov", (
			"Your first two instructions must be 'mov' instructions: one to\n"
			"move a value from memory into rdi, and one to move a value into rax.\n"
		)

	mov_operands = [ d.op_str.split(", ") for d in disas if d.mnemonic == 'mov' ]

	regs, _ = zip(*mov_operands)
	assert set(regs) == { 'rax', 'rdi' }, (
		"You must set both the rax register and the rdi register!"
	)

	assert ( ['rax','0x3c'] in mov_operands ), (
		"You must properly set the 'exit' system call number (60 in rax)!"
	)

	last_rdi_opnd = [ mo[1] for mo in mov_operands if mo[0] == 'rdi' ][-1]

	assert mov_operands.index(['rax','0x3c']) == max(
		i for i,m in enumerate(mov_operands) if m[0] == 'rax'
	), (
		"Uh oh! It looks like you're overwriting exit's syscall index (in rax) after\n"
		"setting it. If you overwrite it, then your eventual syscall instruction will\n"
		"trigger the wrong system call!"
	)

	if secret_reg:
		try:
			idx_deref = max(i for i,m in enumerate(mov_operands) if secret_reg in m[1] and "[" in m[1])
		except ValueError as e:
			raise AssertionError(
				"It looks like you never dereference the register with the secret\n"
				f"address ({secret_reg})! You need to dereference it to read the\n"
				"required exit code!"
			) from e

		try:
			earliest_overwrite = min(i for i,m in enumerate(mov_operands) if m[0] == secret_reg)
			assert earliest_overwrite >= idx_deref, (
				f"Uh oh! It looks like you're overwriting the address in {secret_reg} before\n"
				"dereferncing it. Once you overwrite this value, you will lose the secret\n"
				"address that we initialized it with! Dereference it first before overwriting\n"
				"it.\n"
			)
		except ValueError:
			pass

	assert last_rdi_opnd != hex(secret_addr), (
		f"You are moving the value {secret_addr} into rdi, not the data stored at the memory\n"
		f"addressed by the address {secret_addr}! Please use the [ADDRESS] syntax to denote\n"
		f"the actual memory address (in this case, ADDRESS should be {secret_addr})."
	)
	assert last_rdi_opnd.startswith("qword ptr ["), (
		"You are not moving a value from memory to rdi. You must use the '[ADDRESS]'\n"
		"syntax to do this. In this case, I've stored the secret value at the\n"
		f"ADDRESS of {secret_addr}."
	)
	if secret_reg:
		assert re.match(r"qword ptr \[\w+\]", last_rdi_opnd), (
			f"In this level, please dereference the register {secret_reg} to use the\n"
			"memory address stored there."
		)
	else:
		assert re.match(r"qword ptr \[\w+\]", last_rdi_opnd), (
			f"In this level, please use the address {secret_addr} directly for the memory address.\n"
			"We will learn more advanced ways of addressing memory later."
		)


	operation = disas[-1].mnemonic
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
