#!/bin/bash 
PYPRISMPATH=$(pwd -P)
PYPRISMPATH=${PYPRISMPATH%/env}
echo '--> Prepending the PYTHONPATH:' ${PYPRISMPATH}
export PYTHONPATH=${PYPRISMPATH}:${PYTHONPATH}

# Possible solution for windows
# set PATH=%PATH%;C:\xampp\php
