#!/bin/bash

read -p "Enter the desired scale value: " SCALE_VALUE

docker-compose up --scale app=$SCALE_VALUE
