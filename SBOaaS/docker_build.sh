#!/bin/bash

if [[ $? = 0 ]]; then
	docker build -t tharina/stack .
else
	echo Build failed
fi
