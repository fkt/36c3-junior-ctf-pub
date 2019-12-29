#!/bin/bash
docker run "$@" --rm -p "0.0.0.0:22223:22223" --name "fd" -it "tharina/fd"
