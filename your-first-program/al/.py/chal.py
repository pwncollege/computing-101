allow_asm = True
num_instructions = 1

def check_disassembly(disas):
	operation = disas[0].mnemonic
	assert operation == "mov", (
		f"Your instruction's operation must be 'mov', but yours was {operation}."
	)

	opnd1, opnd2 = disas[0].op_str.split(", ")
	assert opnd1 == "al", (
		"You must move your data to the 'al' register, but you are moving "
		f"to {opnd1}."
	)

	try:
		assert int(opnd2, 0) == 60, (
			"You must move the value 60 into al, whereas you moved "
			f"{int(opnd2, 0)}."
		)
	except ValueError as e:
		if opnd2.startswith("r"):
			raise AssertionError(
				"It looks like you are trying to move values from one register\n"
				"to another, rather than specifying a number to move to al.\n"
				"Try moving 60 to al!"
			) from e
		raise AssertionError(
			"You must move the value 60 into al, whereas you instead specified "
			f"{opnd2}."
		) from e

	return True

def success(raw_binary):
	print("\033[92m", end='') # green
	print("Congratulations, you have written your first program!")
	print("Now let's see what happens when you run it:")
	print("\033[0m") # blank
	print("Segmentation fault")
	print("\033[92m") # green
	print("... uh oh. The program crashed! We'll go into more details about")
	print("what a Segmentation Fault is later, but in this case, the program")
	print("crashed because, after the CPU moved the value 60 into al, it was")
	print("never instructed to stop execution. With no further instructions")
	print("to execute, and no directive to stop, it crashed.")
	print("")
	print("In the next level, we'll learn about how to stop program execution.")
	print("For now, here is your flag for your first (crashing) program!")
	print("\033[0m") # blank
	#pylint:disable=consider-using-with,unspecified-encoding
	print(open("/flag").read())
