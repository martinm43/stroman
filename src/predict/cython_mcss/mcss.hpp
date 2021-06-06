/*
Header file containing Team custom item, structures for sorting,
function definitions, and type definitions.
*/

#ifndef MCSS_H
#define MCSS_H

#include<armadillo>
#include<iostream>


class Team{
private:

    int _team_id;
    std::string _full_team_name;
    std::string _abbreviation;
    std::string _division;
    std::string _league;
    float _rating; 
    int _total_wins; 
    float _wild_card_odds;
    float _division_odds;
    float _playoff_odds;
    std::vector<double> _htoh;
public:

    Team(int team_id, std::string full_team_name, 
            std::string abbreviation, std::string division, std::string league, 
            float rating,std::vector<double> htoh):
        _team_id(team_id), _full_team_name(full_team_name), 
            _abbreviation(abbreviation), _division(division), 
            _league(league), _rating(rating),_htoh(htoh) {}

    //Sample team definition, blank definition.
    //Team()
    Team(){_team_id=0, _full_team_name="Carp", _abbreviation="HC", _division="Central", _league="NPL", _rating=9001.0, _htoh={0,0,0};}


    int get_team_id() const {return _team_id;}
    std::string get_full_team_name() const {return _full_team_name;}
    std::string get_abbreviation() const {return _abbreviation;}
    std::string get_division() const {return _division;}
    std::string get_league() const {return _league;}
    float get_rating() const {return _rating;}
    int get_total_wins() const {return _total_wins;}
    std::vector<double> get_htoh() const{return _htoh;}

    void set_total_wins(int val) {_total_wins = val;}
    void set_wild_card_odds(float val) {_wild_card_odds = val;}
    void set_division_odds(float val) {_division_odds = val;}
    void set_playoff_odds(float val) {_playoff_odds = val;}
    float get_wild_card_odds() const {return _wild_card_odds;}
    float get_division_odds() const {return _division_odds;}
    float get_playoff_odds() const {return _playoff_odds;}
    void set_htoh(std::vector<double> val) {_htoh = val;}
};

//the following are structures passed to std::sort for sorting custom items.
struct teams_sort
{
    inline bool operator()(const Team& Team1, const Team& Team2)
    {
        if (Team1.get_division() != Team2.get_division())
            return (Team1.get_division() < Team2.get_division());
	else if (Team1.get_total_wins() != Team2.get_total_wins())
	    return (Team1.get_total_wins() > Team2.get_total_wins());
	else              
	    return false;  //CANNOT be return true. Must investigate further.
    } 
};

struct wins_sort
{
    inline bool operator()(const Team& Team1, const Team& Team2)
    {
        if (Team1.get_total_wins() >= Team2.get_total_wins())
            return true;
        else 
            return false;
    } 
};

typedef std::vector<double> stdvec;
typedef std::vector< std::vector<double> > stdvecvec;
typedef std::vector<Team> stdteamvec;


stdvecvec mat_to_std_vec(arma::mat &A);
//Functions being passed to cython must use pass by value, not pass by reference (passed not &passed)
stdvecvec simulations_result_vectorized(stdvecvec B, stdvecvec C, stdteamvec D, int year);





#endif
