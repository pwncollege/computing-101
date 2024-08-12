So now you can dereference pointers in memory like a pro!
But pointers don't always point directly at the data you need.
Sometimes, for example, a pointer might point to a collection of data (say, an entire book), and you'll need to reference partway into this collection for the specific data you need.

For example, if your pointer (say, `rdi`) points to a sentence in memory, and you want the 10th letter of that sentence, you could do:

```assembly
mov rax, [rdi+10]
```

Wow, super simple!
In memory terms, we call these "letter" slots _bytes_.
The above example is accessing memory 10 bytes after the memory address pointed to by `rax`.
In memory terms, we call this 10 byte difference an _offset_, so in this example, there is an offset of 10 from the address pointed to by `rdi`.

Let's practice this concept.
As before, we will initialize `rax` (note: not `rdi` unlike the example!) to point at the secret value, but not _directly_ at it.
This time, the secret value will have an offset of 8 bytes from where `rax` points.
Go find it!
