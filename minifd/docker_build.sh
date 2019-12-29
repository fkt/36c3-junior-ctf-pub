#!/bin/bash

if [[ $? = 0 ]]; then
	docker build -t tharina/fd .
else
	echo Build failed
fi
