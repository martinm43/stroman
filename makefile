CC=g++
CFLAGS=-O3 -I.
DEPS = armadillo sqlite3

averagemake: mcss_average.cpp
	g++ -o mcss_average mcss_average.cpp -lsqlite3 -larmadillo -I.
