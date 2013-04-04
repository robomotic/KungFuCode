#!/bin/sh
find . -name '*.pyc' -delete
dir='logs/'
find "$dir" -maxdepth 1 -type f -delete
dir='.db/'
find "$dir" -maxdepth 1 -type f -delete
