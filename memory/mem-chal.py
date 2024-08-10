import __main__ as checker
import random
import re

import chalconf #pylint:disable=import-error
addr_chain = getattr(chalconf, 'addr_chain', None)
secret_addr = addr_chain[-1]
secret_reg = getattr(chalconf, 'secret_reg', None)
num_instructions = getattr(chalconf, 'num_instructions', 3)

#pylint:disable=global-statement

allow_asm = True
give_flag = True
returncode = None

secret_value = random.randint(15, 255)

assembly_prefix = ""
mapped_pages = set()
for n,_addr in enumerate(addr_chain):
	_page = _addr - _addr%0x1000
	assembly_prefix += "mov r9, 0x0; mov r8, 0xffffffff; mov r10, 0x32; mov rdx, 0x3; mov rsi, 0x1000;"
	assembly_prefix += f"mov rdi, {_page}; mov rax, 9; syscall;\n"
	try:
		assembly_prefix += f"mov qword ptr [{_addr}], {addr_chain[n+1]}\n"
	except IndexError:
		assembly_prefix += f"mov qword ptr [{_addr}], {secret_value}\n"

if secret_reg:
	assembly_prefix += f"mov {secret_reg}, {secret_addr}\n"

if secret_reg and len(addr_chain) == 1:
	check_runtime_prologue = """
Let's check what your exit code is! It should be our secret
value pointed to by {secret_reg} (value {secret_value}) to succeed!
	""".strip()
elif secret_reg:
	check_runtime_prologue = """
Let's check what your exit code is! It should be our secret
value pointed to by a chain of pointers starting at {secret_reg}!
	""".strip()
elif len(addr_chain) == 1:
	check_runtime_prologue = """
Let's check what your exit code is! It should be our secret value
stored at memory address {secret_addr} (value {secret_value}) to succeed!
	""".strip()
else:
	check_runtime_prologue = """
Let's check what your exit code is! It should be our secret
value pointed to by a chain of pointers starting at address {secret_addr}!
	""".strip()

check_runtime_success = """
Neat! Your program exited with the correct error code! You have
performed your first memory read. Great job!
""".strip()

check_runtime_failure = f"""
Your program exited with the wrong error code...
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

	if secret_reg:
		assert re.match(r"qword ptr \[\w+\]", last_rdi_opnd), (
			f"In this level, please dereference the register {secret_reg} to use the\n"
			"memory address stored there."
		)
	else:
		assert last_rdi_opnd != hex(addr_chain[0]), (
			f"You are moving the value {addr_chain[0]} into rdi, not the data stored at the memory\n"
			f"addressed by the address {addr_chain[0]}! Please use the [ADDRESS] syntax to denote\n"
			f"the actual memory address (in this case, ADDRESS should be {addr_chain[0]})."
		)
		assert last_rdi_opnd.startswith("qword ptr ["), (
			"You are not moving a value from memory to rdi. You must use the '[ADDRESS]'\n"
			"syntax to do this. In this case, I've stored the secret value at the\n"
			f"ADDRESS of {addr_chain[0]}."
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

	try:
		print("")
		returncode = checker.dramatic_command(filename)
		checker.dramatic_command("echo $?", actual_command=f"echo {returncode}")
		assert returncode == secret_value
	finally:
		checker.dramatic_command("")
		print("")
