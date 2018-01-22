#!/bin/bash
set -e

# -------------------------------------------------------------
# -------------------------------------------------------------
# CMake
# -------------------------------------------------------------
# -------------------------------------------------------------
base_path=$(pwd)
cmake_path=${base_path}/dependencies/CMake/bin
prefix_path=${base_path}/dependencies/usr
source_path=${base_path}/src/mantid
build_path=${base_path}/build
boost_lib_path=${prefix_path}/lib
tcmalloc_include_path=${prefix_path}/include/gperftools
tcmalloc_lib_path=${prefix_path}/lib64/libtcmalloc.so


cd ${build_path}
#/ This is a work around for a broken eigen download
mkdir -p eigen-download/eigen-prefix/src

cd eigen-download/eigen-prefix/src
wget https://bitbucket.org/eigen/eigen/get/3.2.10.tar.gz
cd ../../..
${cmake_path}/cmake -DCMAKE_BUILD_TYPE=Release -DMPI_EXPERIMENTAL=ON -DENABLE_MANTIDPLOT=OFF -DCMAKE_PREFIX_PATH="${prefix_path}" -DTCMALLOC_INCLUDE_DIR="${tcmalloc_include_path}" -DTCMALLOC_LIB="${tcmalloc_lib_path}"  ${source_path}

