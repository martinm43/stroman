# Stroman

A Python/C++ program to calculate basic statistics about baseball seasons and to determine the playoff 
picture at any given time since 1977.

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

Only thing requiring building is the Cython C++ simulation module, using ext_build.sh.
- Note: issues have been encountered with compilation when using GCC 11

## <u>To Do</u>
- Complete readme with brief descriptions of files
- Apply the corrections made in the prediction_table file to team names to the info_table file
- Get the plotting file to work


