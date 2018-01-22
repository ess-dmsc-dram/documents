#!/bin/bash

set -e

# -------------------------------------------------------------
# -------------------------------------------------------------
# 1. Get Mantid
# -------------------------------------------------------------
# -------------------------------------------------------------
mkdir src
mkdir build
mkdir dependencies

# Clone Mantid
cd src
git clone https://github.com/mantidproject/mantid.git

