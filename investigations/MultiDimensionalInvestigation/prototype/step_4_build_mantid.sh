#!/bin/bash
set -e

# -------------------------------------------------------------
# -------------------------------------------------------------
# Build Mantid
# -------------------------------------------------------------
# -------------------------------------------------------------
cd ./build
number_of_processors=$(nproc)
make -j ${number_of_processors}
