import pwnlib.asm

allow_asm = True

def check_raw_binary(raw_binary):
	try:
		disas_lines = pwnlib.asm.disasm(raw_binary).split("\n")
	except pwnlib.exception.PwnlibException as e:
		raise AssertionError(
			"Your assembly failed to disassemble...\n"
			"One possibility for this is that you sent an extra newline.\n"
			"The specific error:\n" + str(e)
		) from e

	assert len(disas_lines) == 1, (
		"This challenge expects a single instruction, but you provided\n"
		f"{len(disas_lines)} instructions."
	)

	operation, operands = disas_lines[0].split(" "*4, 2)[-2:]
	assert operation == "mov", (
		f"Your instruction's operation must be 'mov', but yours was {operation}."
	)

	assert operands.startswith("rax"), (
		"You must move your data to the 'rax' register, but you are moving "
		f"to {operands.split()[0]}."
	)

	try:
		operand_two = operands.split()[-1]
		assert int(operand_two, 0) == 60, (
			"You must move the value 60 into rax, whereas you moved "
			f"{int(operand_two, 0)}."
		)
	except ValueError as e:
		if operand_two.startswith("r"):
			raise AssertionError(
				"It looks like you are trying to move values from one register\n"
				"to another, rather than specifying a number to move to rax.\n"
				"Try moving 60 to rax!"
			) from e
		raise AssertionError(
			"You must move the value 60 into rax, whereas you instead specified "
			f"{int(operand_two, 0)}."
		) from e

	return True

def success():
	print("\033[92m", end='') # green
	print("Congratulations, you have written your first program!")
	print("Now let's see what happens when you run it:")
	print("\033[0m") # blank
	print("Segmentation fault")
	print("\033[92m") # green
	print("... uh oh. The program crashed! We'll go into more details about")
	print("what a Segmentation Fault is later, but in this case, the program")
	print("crashed because, after the CPU moved the value 60 into rax, it was")
	print("never instructed to stop execution. With no further instructions")
	print("to execute, and no directive to stop, it crashed.")
	print("")
	print("In the next level, we'll learn about how to stop program execution.")
	print("For now, here is your flag for your first (crashing) program!")
	print("\033[0m") # blank
	#pylint:disable=consider-using-with,unspecified-encoding
	print(open("/flag").read())
