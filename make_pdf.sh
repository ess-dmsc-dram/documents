#!/bin/sh

cd build

# Run cmake if Makefile not found, i.e., on first invokation
if ! [ -e Makefile ]
then
  cmake ..
fi

make
