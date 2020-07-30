# Stroman

A C++ program to simulate a baseball season. Very much a work in progress. Yes, it's named after the very cool ex-Jays pitcher. 

## <u>**Dependencies**</u>

**Windows**

*Sqlite:* sqlite.c and sqlite.h, which can be obtained from the "amalgamation source code" located at https://www.sqlite.org/download.html. Place these two files in the same folder as the .sln.

*Armadillo:* Obtained from http://arma.sourceforge.net/download.html. Extract and place on your computer in a convenient folder (e.g. C:/armadillo). And do the following:

- Add armadillo directory under `Property Manager --> C/C++ --> General --> Additional Include Directories`, add semicolon after existing entries, followed by `C:\armadillo\include;%(AdditionalIncludeDirectories)`

- Navigate to `Property Manager --> Linker --> General --> Additional Library Directories`, add semicolon after existing entries, followed by `C:\armadillo\examples\lib_win64;%(AdditionalLibraryDirectories)`
- Navigate to `Property Manager --> Linker --> Input --> Additional Dependencies`, add semicolon after existing entries, followed by `blas_win64_MT.lib;lapack_win64_MT.lib;%(AdditionalDependencies)`

(credit to kedarps of StackOverflow for the linking instructions)

**Linux**

`sudo apt install libarmadillo-dev libsqlite3-dev` 

## **<u>Build Instructions</u>**

**Windows, Visual Studio:** Select Release and x64 configuration and "Rebuild Solution"

**Linux:**  `make`

(mlb_data.sqlite must be in the same folder as the executable)

## <u>To Do</u>

Improve model; figure out how to import data from MLB stats api; complete this section



