Did you prefer to access memory at `133700` or at `123400`?
Your answer might say something about your personality, but it's not super relevent from a technical perspective.
In fact, in most cases, you don't deal with actual memory addresses when writing programs at all!

How is this possible?
Well, typically, memory addresses are stored in registers, and we use the values in the registers to point to data in memory!
Consider this snippet:

```assembly
mov rdi, [rax]
```

How interesting!
Here, we are accessing memory, but instead of specifying a fixed address like `133700`, we're using the value stored in `rax` as the memory address.
By containing the memory address, `rax` is a _pointer_ that _points to_ the data we want to access!
When we use `rax` in lieu of directly specifying the address that it stores to access the memory address that it references, we call this _dereferencing_ the pointer.
In the above example, we _dereference_ `rax` to load the data it points to into `rdi`.
Neat!

In this challenge, we've initialized `rax` to contain the address of the secret data we've stored in memory.
Dereference `rax` to the secret data into `rdi` and use it as the exit code of the program to get the flag!
