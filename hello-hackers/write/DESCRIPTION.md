Let's learn to write text!

Unsurprisingly, your program writes text to the screen by invoking a system call.
Specifically, this is the `write` system call, and its syscall number is `1`.
However, the write system call also needs to specify, via its parameters, _what_ data to write and _where_ to write it to.

You may remember, from the [../../linux-luminarium/piping](Practicing Piping) module of the [../../linux-luminarium](Linux Luminarium) dojo, the concept of _File Descriptors_ (FDs).
As a reminder, each process starts out with three FDs:

- **FD 0:** Standard *Input* is the channel through which the process takes input. For example, your shell uses Standard Input to read the commands that you input.
- **FD 1:** Standard *Output* is the channel through which processes output normal data, such as the flag when it is printed to you in previous challenges or the output of utilities such as `ls`.
- **FD 2:** Standard *Error* is the channel through which processes output error details. For example, if you mistype a command, the shell will output, over standard error, that this command does not exist.

It turns out that, in your `write` system call, this is how you specify _where_ to write the data to!
The first (and only) parameter to your `exit` system call was your exit code (`mov rdi, 42`), and the first (but, in this case, not only!) parameter to `write` is the file descriptor.
If you want to write to standard output, you would set `rdi` to 1.
If you want to write to standard error, you would set `rdi` to 2.
Super simple!

This leaves us with _what_ to write.
Now, you could imagine a world where we specify what to write through yet another register parameter to the `write` system call.
But these registers don't fit a ton of data, and to write out a long story like this challenge description, you'd need to invoke the `write` system call multiple times.
Relatively speaking, this has a lot of performance cost --- the CPU needs to switch from executing the instructions of your program to executing the instructions of Linux itself, do a bunch of housekeeping computation, interact with your hardware to get the actual pixels to show up on your screen, and then switch back.
This is slow, and so we try to minimize the number of times we invoke system calls.

Of course, the solution to this is to write multiple characters at the same time.
The `write` system call does this by taking _two_ parameters for the "what": a _where_ (in memory) to start writing from and a _how many_ characters to write.
These parameters are passed as the second and third parameter to `write`.
In the kinda-C syntax that we learned from `strace`, this would be:

```c
write(file_descriptor, memory_address, number_of_characters_to_write)
```

For a more concrete example, if you wanted to write 10 characters from memory address 133700 to standard output (file descriptor 1), this would be:

```c
write(1, 133700, 10);
```

Wow, that's simple!
Now, how do we actually specify these parameters?

1. We'll pass the first parameter of a system call, as we reviewed above, in the `rdi` register.
2. We'll pass the second parameter via the `rsi` register.
   That's just another general purpose register, and the agreed-upon convention in Linux is that it's used as the second parameter to a system call.
3. We'll pass the third parameter via the `rdx` register.
   This is the most confusing part of this entire module: `rdi` (the register holding the first parameter) has such a similar name to `rdx` that it's really easy to mix up and, unfortunately, the naming is this way for historic reasons and is here to stay.
   Oh well...
   It's just something we have to be careful about.
   Maybe a mnemonic like "`rdi` is the **i**nitial parameter while `rdx` is the **x**tra parameter"?

And, of course, the `write` syscall index into `rax` itself: `1`.
Other than the `rdi` vs `rdx` confusion, this is really easy!
Just think of it as having to keep track of different friends with similar names, and you'll be fine.

Now, you know how to point a register at a memory address (from the [../memory](Memory) module!), and yo know how to set the system call number, and how to set the rest of the registers.
So, this should be cake!

Similar to before, we wrote a secret value into memory at address `133700`.
Call `write` to that value onto standard out, and we'll give you the flag!
