As seen by your program, computer memory is a huge place where data is housed.
Like houses on a street, every part of memory has a numeric _address_, and like houses on a street, these numbers are (mostly) sequential.
Modern computers have enormous amounts of memory, and the view of memory of a typical modern program actually has large gaps (think: a playground that takes up some amount of house numbers, but no one lives there!).
But these are all details: the point is, computers store data, mostly sequentially, in memory.

In this level, we will practice accessing data stored in memory.
How might we do this?
Recall that to move a value into a register, we did something like:

```assembly
mov dil, 42
```

After this, the value of `dil` is `42`.
Cool.
Well, we can use the same instruction to access memory!
There is another format of the command that, instead, uses the second parameter as an address to access memory!
It is:

```assembly
mov dil, [42]
```

When the CPU executes this instruction, it of course understands that the `42` is an _address_, not a raw value.
If you think of the instruction as a person telling the CPU what to do, and we stick with our "houses on a street" analogie, then instead of just handing the CPU data, the instruction/person _points at a house on the street_.
The CPU will then go to that address, ring its doorbell, open its front door, drag the data that's in there out, and put it into `dil`.
Thus, the `42` in this context is the _memory address_ and serves as a _pointer_ to the data stored at that memory address.

Let's put this into practice!
I've stored a secret number at memory address `100`.
You must retrieve this secret number and use it as the exit code for your program.
To do this, you must read it into `dil`, whose value, if you recall, is the first parameter to `exit` and is used as the exit code.
Good luck!
