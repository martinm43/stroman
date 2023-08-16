#include <cmath>
#include <iostream>
#include <sqlite3.h>
#include <vector>
#include <Eigen/Dense>

//ORM
struct Game {
    int id;
    int home_team_id;
    int home_team_runs;
    int away_team_id;
    int away_team_runs;
    int year;
    double epochtime;
};

int selectDataCallback(void* data, int argc, char** argv, char** /*azColName*/) {
    std::vector<Game>* games = static_cast<std::vector<Game>*>(data);

    Game game;
    game.id = std::stoi(argv[0]);
    game.home_team_id = std::stoi(argv[1]);
    game.home_team_runs = std::stoi(argv[2]);
    game.away_team_id = std::stoi(argv[3]);
    game.away_team_runs = std::stoi(argv[4]);
    game.year = std::stoi(argv[5]);
    game.epochtime = std::stod(argv[6]);
    games->push_back(game);

    return 0;
}

int main() {
    sqlite3* db;
    char* errorMsg = nullptr;

    // Open a connection to the database
    int rc = sqlite3_open("mlb_data.sqlite", &db);
    if (rc != SQLITE_OK) {
        std::cout << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return rc;
    }

    // Query the table
    const char* selectDataQuery = "SELECT id, home_team_id, home_team_runs, away_team_id, away_team_runs,"
    " year , epochtime FROM Games where year = 2022"; 
    std::vector<Game> games;
    rc = sqlite3_exec(db, selectDataQuery, selectDataCallback, &games, &errorMsg);
    if (rc != SQLITE_OK) {
        std::cout << "SQL error: " << errorMsg << std::endl;
        sqlite3_free(errorMsg);
        sqlite3_close(db);
        return rc;
    }

    // Close the database connection
    sqlite3_close(db);

    // Process the data
    int processing_year = games[0].year;



    int max_MOV = 100;
    int win_floor = 0;
    int numTeams = 30;

    std::vector<std::vector<double> > M(numTeams, std::vector<double>(games.size(), 0.0));
    std::vector<double> S(games.size(),0.0);

    for (unsigned long col=0;col<games.size();col++) {
  
        int gameNum = col;
        double home, away, homescore, awayscore;
        home = games[col].home_team_id;
        away = games[col].away_team_id;
        homescore = games[col].home_team_runs;
        awayscore = games[col].away_team_runs;

        // In the csv data, teams are numbered starting at 1
        // So we let home-team advantage be 'team 0' in our matrix
        M[int(home) - 1][col] = 1.0;
        M[int(away) - 1][col] = -1.0;

        int diff_score = static_cast<int>(homescore) - static_cast<int>(awayscore);
        if (diff_score > max_MOV) {
            diff_score = static_cast<int>(max_MOV);
        } else if (diff_score < -max_MOV) {
            diff_score = static_cast<int>(-max_MOV);
        }

        // Granting a bonus based on "actually winning the game".
        // This is intended to account for teams that can "win games when it counts".
        // A crude adjustment for teams with significantly different talent levels from other teams.
        if (diff_score > 0) {  // bonuses for a win
            diff_score = std::max(static_cast<int>(win_floor), diff_score);
        } else {  // demerits for a loss
            diff_score = std::min(static_cast<int>(-win_floor), diff_score);
        }

        S[col] = diff_score;
    }

    // Now, if our theoretical model is correct, we should be able to find a performance-factor vector W such that W*M == S
    // In the real world, we will never find a perfect match, so what we are looking for instead is W, which results in S'
    // such that the least-mean-squares difference between S and S' is minimized.

    //Eigen::MatrixXd M(30, 1400); // Convert 2D vector to Eigen matrix
    //Eigen::VectorXd S(1400);     // Convert 1D vector to Eigen vector
    Eigen::MatrixXd Mmatrix(numTeams, games.size()); // Convert 2D vector to Eigen matrix
    Eigen::VectorXd Svector(games.size());     // Convert 1D vector to Eigen vector

    // Fill Eigen matrix and vector with data
    for (int i = 0; i < 30; ++i) {
        for (int j = 0; j < 1400; ++j) {
            Mmatrix(i, j) = M[i][j];
        }
    }
    for (int j = 0; j < 1400; ++j) {
        Svector(j) = S[j];
    }

    Eigen::MatrixXd MmatrixT = Mmatrix.transpose();
    Eigen::RowVectorXd SvectorT = Svector.transpose();
    

    std::cout << "M is " << Mmatrix.rows() << " by " << Mmatrix.cols() << std::endl;
    std::cout << "MT is " << MmatrixT.rows() << " by " << MmatrixT.cols() << std::endl;
    std::cout << "S is " << Svector.rows() << " by " << Svector.cols() << std::endl;
    std::cout << "ST is " << SvectorT.rows() << " by " << SvectorT.cols() << std::endl;


    // Solve using least squares
    Eigen::VectorXd x = MmatrixT.jacobiSvd(Eigen::ComputeThinU | Eigen::ComputeThinV).solve(Svector);


    


    std::vector<double> init_W(numTeams, 0.0);

    std::vector<double> W = init_W;
    double homeAdvantage = W[0];

    std::cout << "Solution x: " << x.transpose() << std::endl;

    std::cout<<"Completion. "<<std::endl;

    return 0;
}

