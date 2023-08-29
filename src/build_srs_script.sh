#!/bin/sh
g++ srs.cpp -o SRSCalc -lsqlite3 -I /usr/local/include/eigen3 -O3 #macOS version.
g++ srs.cpp -o SRSCalc -lsqlite3 -I /usr/include/eigen3 -O3 #Linux version.
