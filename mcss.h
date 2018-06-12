#ifndef MCSS_H
#define MCSS_H

#include<iostream>

double SRS_regress(double rating_away, double rating_home);
double uniformRandom();

double uniformRandom() {
  return ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
}

class Game{
private:

   int _away_team_id;
   int _away_runs;
   int _home_team_id;
   int _home_runs;

public:
   Game(int away_team_id, int away_runs, int home_team_id, int home_runs): 
     _away_team_id(away_team_id), _away_runs(away_runs), _home_team_id(home_team_id), _home_runs(home_runs) {}

   int get_away_team_id() const {return _away_team_id;}
   int get_away_runs() const {return _away_runs;}
   int get_home_team_id() const {return _home_team_id;}
   int get_home_runs() const {return _home_runs;}
};

class Team{
private:

    int _team_id;
    std::string _mlbgames_name;
    std::string _abbreviation;
    std::string _division;
    std::string _league;
    float _rating;
    int _total_wins;

public:

    Team(int team_id, std::string mlbgames_name, 
            std::string abbreviation, std::string division, std::string league, 
            float rating):
        _team_id(team_id), _mlbgames_name(mlbgames_name), 
            _abbreviation(abbreviation), _division(division), 
            _league(league), _rating(rating) {}

    int get_team_id() const {return _team_id;}
    std::string get_mlbgames_name() const {return _mlbgames_name;}
    std::string get_abbreviation() const {return _abbreviation;}
    std::string get_division() const {return _division;}
    std::string get_league() const {return _league;}
    float get_rating() const {return _rating;}

    void set_total_wins(int val) {_total_wins = val;}
    int get_total_wins() const {return _total_wins;}
};

double SRS_regress(double rating_away, double rating_home)
{
    float m=0.0;
    float b=-0.15; 
    return (double) 1.0/(1.0 + exp(-1*(m*(rating_home-rating_away)+b)));
}

struct teams_sort
{
    inline bool operator()(const Team& Team1, const Team& Team2)
    {
        if (Team1.get_division() == Team2.get_division())
            if (Team1.get_total_wins() > Team2.get_total_wins())
                return true;
            else
                return false;
        else if (Team1.get_division() < Team2.get_division())
            return true;
        else
            return false;
    } 
};

struct wins_sort
{
    inline bool operator()(const Team& Team1, const Team& Team2)
    {
        if (Team1.get_total_wins() > Team2.get_total_wins())
            return true;
        else 
            return false;
    } 
};

#endif
