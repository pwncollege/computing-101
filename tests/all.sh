#!/bin/bash

cd $(dirname ${BASH_SOURCE[0]})/../

RESULT="SUCCESS"
for TEST in tests/solves/*
do
	echo "[t] Running $TEST"
	FAST=1 "$TEST" || RESULT="FAIL"
done

yes "$RESULT" | head -n10
