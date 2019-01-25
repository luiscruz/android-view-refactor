#!/bin/bash

PROJECTS_PATH=$1/*
DESIGNITE_PATH=~/dev/designite/DesigniteJava.jar
OUTPUT_DIR=~/dev/designite/output

for filename in $PROJECTS_PATH; do
  PROJECT_OUTPUT_DIR="$OUTPUT_DIR/${filename##*/}_designite"
  echo $PROJECT_OUTPUT_DIR
  mkdir $PROJECT_OUTPUT_DIR
  java -jar $DESIGNITE_PATH -i "$filename" -o $PROJECT_OUTPUT_DIR
done
