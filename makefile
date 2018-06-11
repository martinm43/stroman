CC=g++
CFLAGS=-O3 -I.
DEPS = armadillo sqlite3

averagemake: mcss.cpp
	g++ -o mcss mcss.cpp -lsqlite3 -larmadillo -I.
