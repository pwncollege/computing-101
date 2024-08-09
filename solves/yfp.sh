#!/bin/bash -e

cd $(dirname ${BASH_SOURCE[0]})/../

your-first-program/rax/check <<< "mov rax, 60" | grep "pwn.college{"
your-first-program/exit/check <<< "mov rax, 60; syscall" | grep "pwn.college{"
your-first-program/exit-code/check <<< "mov rdi, 42; mov rax, 60; syscall" | grep "pwn.college{"
