#!/bin/bash -x

cd $(dirname ${BASH_SOURCE[0]})/../

FAILED=()
for TEST in tests/solves/*
do
	echo "[t] Running $TEST"
	FAST=1 "$TEST" || FAILED+=($TEST)
done

if [ "${#FAILED[@]}" -ne 0 ]
then
	echo FAILED: "${FAILED[@]}"
	yes "FAIL"
else
	yes "SUCCESS"
fi | head -n10
