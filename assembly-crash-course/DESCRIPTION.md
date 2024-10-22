Now that you have the hang of very basic assembly, let's dive in and explore a few different instructions and some additional concepts!
The Assembly Crash Course is a romp through a lot of different things you can do in assembly, and will prepare you for the adventures to come!

To interact with any level you will send raw bytes over stdin to this program.
To efficiently solve these problems, first run it to see the challenge instructions.
Then craft, assemble, and pipe your bytes to this program.

For instance, if you write your assembly code in the file `asm.S`, you can assemble that to an object file:
```plaintext
as -o asm.o asm.S
```

Note that if you want to use Intel syntax for x86 (which, of course, you do), you'll need to add the following to the start of `asm.S`:
```plaintext
.intel_syntax noprefix
```

Then, you can copy the `.text` section (your code) to the file `asm.bin`:
```plaintext
objcopy -O binary --only-section=.text asm.o asm.bin
```

And finally, send that to the challenge:
```plaintext
cat ./asm.bin | /challenge/run
```

You can even run this as one command:
```plaintext
as -o asm.o asm.S && objcopy -O binary --only-section=.text ./asm.o ./asm.bin && cat ./asm.bin | /challenge/run
```
