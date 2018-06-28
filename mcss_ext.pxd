# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#
#

from libcpp.vector cimport vector
from libcpp.string cimport string

# c++ interface to cython
cdef extern from "mcss.h":

    cdef cppclass Team:

        Team(int,string,string,string,string,float) except +

        int get_team_id()
        string get_mlbgames_name()
        string get_abbreviation()
        string get_division()
        string get_league()
        float get_rating()
        int get_total_wins()


        void set_total_wins(int val)
        void set_wild_card_odds(float val)
        void set_division_odds(float val)
        void set_playoff_odds(float val)
        float get_wild_card_odds()
        float get_division_odds()
        float get_playoff_odds()

    vector[vector[double]] simulations_result_vectorized(vector[vector[double]],vector[vector[double]])

cdef class PyTeam:
    cdef Team *thisptr # hold a C++ instance of a team object

    def __cinit__(self,int id, string mlbgames_name, string...)
        self.thisptr = new Team(...)

    def __dealloc__(self):
        del self.thisptr

    def get_team_id(self):
        return self.thisptr.get_team_id()

    #other defs as above
    def get_mlbgames_name(self):
        return self.thisptr.get_mlbgames_name()
    def get_abbreviation(self):
        return self.thisptr.get_abbreviation()
    def get_division(self):
        return self.thisptr.get_division()
    def get_league(self):
        return self.thisptr.get_league()
    def get_rating(self):
        return self.thisptr.get_rating()
    def get_total_wins(self):
        return self.thisptr.get_total_wins()


        self.thisptr.set_total_wins(int val)
        self.thisptr.set_wild_card_odds(float val)
        self.thisptr.set_division_odds(float val)
        self.thisptr.set_playoff_odds(float val)
        self.thisptr.get_wild_card_odds()
        self.thisptr.get_division_odds()
        self.thisptr.get_playoff_odds()
