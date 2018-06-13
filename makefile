CC=g++
CFLAGS=-O3 -I.
DEPS = armadillo sqlite3

main-make: mcss.cpp
	g++ -o mcss mcss.cpp -lsqlite3 -larmadillo -I. -O3

debug-make: mcss.cpp
	g++ -o mcss mcss.cpp -lsqlite3 -larmadillo -I. -g

average-make:
	g++ -o mcss_average mcss_average.cpp -lsqlite3 -larmadillo -I. -O3

average-debug-make:
	g++ -o mcss_average mcss_average.cpp -lsqlite3 -larmadillo -I. -g

