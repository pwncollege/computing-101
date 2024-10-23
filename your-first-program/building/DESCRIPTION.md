So you've written your first program?
But until now, we've handled the actual building of it into an executable that your CPU can actually run.
In this challenge, _you_ will build it!

To build an executable binary, you need to:

1. Write your assembly in a file (often with a `.S` or `.s` syntax. We'll use `asm.s` in this example).
2. Assemble your binary into an executable _object file_ (using the `as` command).
3. Link one or more executable object files into a final executable binary (using the `ld` command)!

Let's take this step by step:

**Writing assembly.**  
The assembly file contains, well, your assembly code.
For the previous level, this might be:

```console
hacker@dojo:~$ cat asm.s
mov rdi, 42
mov rax, 60
syscall
hacker@dojo:~$
```

But it needs to contain _just a tad more info_.
We mentioned that we're using the _Intel_ assembly syntax in this course, and we'll need to let the assembler know that.
You do this by prepending a directive to the beginning of your assembly code, as such:

```
hacker@dojo:~$ cat asm.s
.intel_syntax noprefix
mov rdi, 42
mov rax, 60
syscall
hacker@dojo:~$
```

`.intel_syntax noprefix` tells the assembler that you will be using Intel assembly syntax, and specifically the variant of it where you don't have to add extra prefixes to every instruction.
We'll talk about these later, but for now, we'll let the assembler figure it out!

**Assembling object files!**  
Next, we'll assemble the code.
This is done using the **as**sembler, `as`, as so:

```
hacker@dojo:~$ ls
asm.s
hacker@dojo:~$ cat asm.s
.intel_syntax noprefix
mov rdi, 42
mov rax, 60
syscall
hacker@dojo:~$ as -o asm.o asm.s
hacker@dojo:~$ ls
asm.s   asm.o
hacker@dojo:~$
```

Here, the `as` tool reads in `asm.s`, assembles it into binary code, and outputs an _object file_ called `asm.o`.
This object file has actual assembled binary code, but it is not yet ready to be run.
First, we need to _link_ it.

**Linking executables.**  
In a typical development workflow, source code is compiled and assembly is assembled to object files, and there are typically many of these (generally, each source code file in a program compiles into its own object file).
These are then _linked_ together into a single executable.
Even if there is only one file, we still need to link it, to prepare the final executable.
This is done with the `ld` (stemming from the term "**l**ink e**d**itor") command, as so:

```console
hacker@dojo:~$ ls
asm.s   asm.o
hacker@dojo:~$ ld -o exe asm.o
hacker@dojo:~$ ls
asm.s   asm.o   exe
hacker@dojo:~$
```

This creates an `exe` file that we can then run!
Here it is:

```console
hacker@dojo:~$ ./exe
hacker@dojo:~$ echo $?
42
hacker@dojo:~$
```

Neat!
Now you can build programs.
In this challenge, go ahead and run through these steps yourself.
Build your executable, and pass it to `/challenge/check` for the flag!
