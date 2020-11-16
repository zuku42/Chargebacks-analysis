# Chargebacks analysis

This is a solution for a recruitment task for a company that manages online
payments. The aim of the task was to identify main sources of chargebacks
filed by the customers and propose actions aimed at reducing the chargebacks
rate to a given limit based on the results of the analysis. In order to
achieve that, it was necessary to use data from two sources: a database and
an Excel spreadsheet. The details of the task can be found in the "task.pdf"
file. 

Based on the reported chargebacks stored in the "Processing Report.xlsx" file
as well as the data about cards, transactions, and customers contained in the
"db.sqlite" database, an analysis of the main sources of chargebacks was 
performed and its most important findings reported in a PowerPoint 
presentation. Both sources of data, that is the Excel file and the sqlite 
database, were linked with each other as required.

# Prerequities

- Python 3
- Python libraries: pandas, numpy, scipy, sqlite3, matplotlib

# Contents

In the "Chargebacks analysis" package you will find five python scripts 
(__init__.py excluded). "cb_match.py" is responsible for updating the database
with information contained in the "Processing Report.xlsx" file. It provides 
the solution to task 1 and for the rest of the code to generate expected 
results it is necessary that this script is ran first. This script uses 
methods of the DatabaseQueries class contained in the "db_class.py" module. 
This class was built to encapsulate the code responsible for communication 
with the database. Although all methods of this class were developed for this 
particular application, it can serve a wider purpose and can be easily 
extended to accommodate for other SQL queries if necessary.

"prepare_data.py" is a script that uses methods of the DatabaseQueries class
to gather necessary information for the rest of analysis. All the data it 
produces is exported to three csv files.

The analsyis of data prepared by the "prepare_data.py" script can be conducted
with the "analyse.py" module. It reads the previously created csv files to 
process them and generate values that will be later used to draw conclusions
about main sources of chargebacks. Although it is not necessary to run this
script directly (it is later imported into "plot.py" as a module), it will
print out a short report when executed this way.

Finally, there is "plot.py" script that uses matplotlib library to generate 
four figures visualising the data generated in "analyse.py".

Apart from the python scripts, you will notice that this package contains
three folders. "figures" contains plots generated by the "plot.py" script.
They will be overwritten upon executing this script again. "files" contains 
the files provided as inputs for this task ("db.sqlite",
"Processing Report.xlsx") in their original form. Other Excel and csv files
that will be generated as a result of running this program will be also saved
in this directory. "aux_scripts" contains auxilary python scripts: 
"file_paths.py" with paths to files used in the program assigned to constants,
"sql_queries.py" with commands in SQL used in the DatabaseQueries class, and 
"vector_decorator.py" that contains a class definition responsible for
altering the original behaviour of numpy.vectorize function.

# Installation

For the program to yield expected results, scripts should be ran in the
following order: cb_match.py -> prepare_data.py -> plot.py.

Alternatively, if you are not interested in generating plots but would like to
compute all the values and read a short report that summerizes them, you can
execute the scripts in the following order: cb_match.py -> prepare_data.py ->
-> analyse.py.

To run a python program you will need to navigate to the directory containing
all the scripts using your command line and type: python <name of the script>.
You must not move any of the files in this directory, unless you make
appropriate alterations to the import statements and path names.

# Limitations

Note that the order of countries in figure 2 you will generate with the 
"plot.py" script may differ from that in the PowerPoint presentation, as the
number of chargebacks filed by customers from certain countries is the same
and the order of those countries will be generated randomly. It does not
change the interpretation of the graph.