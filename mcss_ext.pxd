# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#
#

from libcpp.vector cimport vector
from libcpp.string cimport string

# c++ interface to cython
cdef extern from "mcss.h":
    vector[vector[double]] simulations_result_vectorized(vector[vector[double]],vector[vector[double]])

cdef cppclass Team:

    Team(int,string,string,string,strin

    int get_team_id() const {return _team_id;}
    std::string get_mlbgames_name() const {return _mlbgames_name;}
    std::string get_abbreviation() const {return _abbreviation;}
    std::string get_division() const {return _division;}
    std::string get_league() const {return _league;}
    float get_rating() const {return _rating;}
    int get_total_wins() const {return _total_wins;}


    void set_total_wins(int val) {_total_wins = val;}
    void set_wild_card_odds(float val) {_wild_card_odds = val;}
    void set_division_odds(float val) {_division_odds = val;}
    void set_playoff_odds(float val) {_playoff_odds = val;}
    float get_wild_card_odds() const {return _wild_card_odds;}
    float get_division_odds() const {return _division_odds;}
    float get_playoff_odds() const {return _playoff_odds;}
