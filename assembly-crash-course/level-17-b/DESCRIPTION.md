We will now be working with control flow manipulation. On each run, the code may be placed at different addresses, so you will need to write instructions that can adapt to their location in memory. In most cases, you will want to set the result in `rax`.

In this level, you will be working with the Instruction Pointer `rip`. Normally, the CPU executes instructions one after another in a straight line. By directly modifying `rip`, you can make the CPU skip over parts of your code or jump to a specific location dynamically.

Recall that there are three types of jumps you might encounter:
* Relative jumps: jump a certain number of bytes forward or backward from the current instruction.
* Absolute jumps: jump to a fixed memory address.
* Indirect jumps: jump to the address stored in a register or memory location.

Here, we are focusing on relative jumps. This means you will tell the CPU to “jump forward a certain number of bytes from where you are currently executing.” This is useful because your code can move in memory and the jump will still reach the correct target.

To implement a relative jump, you will need a few tools:
* `labels`: Instead of calculating addresses manually, you can use labels as placeholders. The assembler will automatically calculate the offset from your jump instruction to the label.
* `nop` (No Operation): A single-byte instruction that does nothing. It is predictable in size and can be used as filler to create an exact distance for your jump.
* `.rept` (Repeat Directive): A directive that tells the assembler to repeat a given instruction multiple times: [GNU Assembler Manual](https://ftp.gnu.org/old-gnu/Manuals/gas-2.9.1/html_chapter/as_7.html) This is perfect for generating a block of `nop` instructions without typing each one individually.

Please perform the following:
* Make the first instruction in your code a `jmp`.
* Make that `jmp` a relative jump of exactly 0x51 bytes from the current instruction.
* Fill the space between the jump and the destination with `nop` instructions using `.rept`.
* At the label where the relative jump lands, set `rax` to 0x1.

When your code runs, the CPU will execute the jump, skip over all the nop instructions, and continue at the instruction that sets `rax`. This will demonstrate how to control the flow of execution using relative jumps.
