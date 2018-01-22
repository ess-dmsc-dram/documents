#!/bin/bash
set -e

# -------------------------------------------------------------
# -------------------------------------------------------------
# Set environment variables in bashrc
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
base_path=$(pwd)
prefix_path=${base_path}/dependencies/usr

# We need to set environment variables for libunwind and some python packages
echo 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}'"${prefix_path}/lib64" >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}'"${prefix_path}/lib" >> ~/.bashrc
echo 'export PYTHONPATH=${PYTHONPATH:+${PYTHONPATH}:}'"${prefix_path}/lib/python2.7/site-packages" >> ~/.bashrc
echo 'export PYTHONPATH=${PYTHONPATH:+${PYTHONPATH}:}'"${prefix_path}/lib64/python2.7/site-packages" >> ~/.bashrc

echo "*******************************************************************"
echo "Everything has been set up. To run a sript you have to first do  source .bashrc in your home directory to load the environment variables."
