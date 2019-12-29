#!/bin/bash
docker run "$@" --rm -p "0.0.0.0:22222:22222" --name "stack" -it "tharina/stack"
