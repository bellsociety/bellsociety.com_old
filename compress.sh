#!/usr/bin/env bash

FILES=./*.jpg
for f in $FILES
do
  echo "Processing $f"
  convert "$f" -resize "512^>" "$f"
done