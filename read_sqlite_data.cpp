#include <sqlite3.h>
#include <iostream>

int main() {
    sqlite3* db;
    int result = sqlite3_open("example.db", &db);

    if (result != SQLITE_OK) {
        std::cerr << "Failed to open database: " << sqlite3_errmsg(db) << std::endl;
        return 1;
    }

    // Execute a simple query
    const char* query = "SELECT * FROM my_table";
    sqlite3_stmt* stmt;
    result = sqlite3_prepare_v2(db, query, -1, &stmt, nullptr);

    if (result != SQLITE_OK) {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    // Fetch the results
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        // Access columns by their index
        int column1 = sqlite3_column_int(stmt, 0);
        const char* column2 = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));

        // Process the retrieved data
        std::cout << "Column 1: " << column1 << ", Column 2: " << column2 << std::endl;
    }

    // Clean up resources
    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return 0;
}
