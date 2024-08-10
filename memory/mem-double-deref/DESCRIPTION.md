In the last few levels, you have:

- Used an address that we told you (in one level, `133700`, and in another, `123400`) to load a secret value from memory.
- Used an address that we put into `rax` for you to load a secret value from memory.
- Used an address that we told you (in the last level, `567800`) to load _the address_ of a secret value from memory into a register, then used that register as a pointer to retrieve the secret value from memory!

Let's put those last two together.
In this level, we stored our `SECRET_VALUE` in memory at the address `SECRET_LOCATION_1`, then stored `SECRET_LOCATION_1` in memory at the address `SECRET_LOCATION_2`.
Then, we put `SECRET_ADDRESS_2` into `rax`!
You will need to perform two memory reads: one dereferencing `rax` to read `SECRET_LOCATION_1` from the location that `rax` is pointing to (which is `SECRET_LOCATION_2`), and the second one dereferencing whatever register now holds `SECRET_LOCATION_1` to read `SECRET_VALUE` into `rdi`, so you can use it as the exit code!

That sounds like a lot, but you've done basically all of this already.
Go put it together!
