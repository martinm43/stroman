#!/bin/bash

# Check if the operating system is macOS
if [[ $(uname) == "Darwin" ]]; then
    echo "Compiling on macOS"
    # Add macOS-specific commands here
    g++ srs.cpp -o SRSCalc -lsqlite3 -I /usr/local/include/eigen3 -O3 #macOS version.
fi


# Check if the operating system is Termux
if [[ -n "$PREFIX" ]]; then
    echo "Compiling on Termux"
    # Add Linux/Unix-specific commands here
    g++ srs.cpp -o SRSCalc -lsqlite3 -I $PREFIX/include/eigen3 -O3 #Linux version.
elif [[ $(uname) == "Linux" || $(uname) == "GNU" ]]; then
    echo "Compiling on Linux/Unix"
    # Add Linux/Unix-specific commands here
    g++ srs.cpp -o SRSCalc -lsqlite3 -I /usr/include/eigen3 -O3 #Linux version.
fi


