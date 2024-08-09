#!/bin/bash -e

cd $(dirname ${BASH_SOURCE[0]})/../

your-first-program/al/check <<< "mov al, 60" | grep "pwn.college{"
your-first-program/exit/check <<< "mov al, 60; syscall" | grep "pwn.college{"
your-first-program/exit-code/check <<< "mov dil, 42; mov al, 60; syscall" | grep "pwn.college{"
