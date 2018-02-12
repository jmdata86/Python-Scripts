
## Problem:  Need to download 1 year's worth of data from MicrosoftSQL server.
# Solution:  Use Bulk Copy Program (BCP).

## Problem: Bulk Copy Program commands cannot reference an external .sql file
#  Solution: Use Python script to read .sql and submit a BCP command with the query inline.

## Problem: Data is too big for 1 file.
#  Solution: Have Python script iterate over a set of dates, replacing the dates in the query with dates to extract 1 month of data at a timeout

## Problem: BCP doesn't create properly partitioned .csv files.
#  Solution: Use a custom multi-character delimiter so that data with long strings of variable lengths and unsanitized contents can be properly parsed

import os
import pandas as pd


# create data frame containing date intervals we want to extract
dates = pd.DataFrame([
        ["2017-01-01", "2017-02-01","201701"]
        ,["2017-02-01", "2017-03-01","201702"]
        ,["2017-03-01", "2017-04-01","201703"]
        ,["2017-04-01", "2017-05-01","201704"]
        ,["2017-05-01", "2017-06-01","201705"]
        ,["2017-06-01", "2017-07-01","201706"]
        ,["2017-07-01", "2017-08-01","201707"]
        ,["2017-08-01", "2017-09-01","201708"]
        ,["2017-09-01", "2017-10-01","201709"]
        ,["2017-10-01", "2017-11-01","201710"]
        ,["2017-11-01", "2017-12-01","201711"]
        ,["2017-12-01", "2018-01-01","201712"]], columns=['begin', 'end', 'filename'])

# sql file path
sqlpath = "\\\\labsg\\users\\jmartin18\\SCM Orders\\Code and Queries\\SCMpharma v.05.sql"
# path to dump extracted files
datapath = '"C:\\Users\\jmartin18\\Documents\\Query Results\\bcp\\scm_pharm{}.txt"'

# import .sql as string
with open(sqlpath,'r') as mysqlfile:
    sqltxt=mysqlfile.read()

# replace the start and end dates from .sql with curly braces so string.format can insert the dates we want
sqltxt = sqltxt.replace("2017-01-01", "{}")
sqltxt = sqltxt.replace("2017-02-01", "{}")

print("waiting 3 seconds then starting...")
os.system("timeout 3")

for x in range(0,12):
    
    #prep command
    #
    
    command = 'bcp.exe "' + sqltxt.format(dates.begin[x], dates.end[x]) + '" queryout ' + datapath.format(dates.filename[x]) + " -tJMcl! -rJMrw! -T -c -S CYKPANADBSQL & timeout 10"
    
    print(command)
    
    # The BCP command wants to see whitespace and not \n\t in the string its passed as the sql query.
    # Note that the "--" to comment the rest of a line works in BCP if you can somehow get a newline into the command prompt.  However \n doesn't actually work, I've only been able to do this by copy and pasting into the command line.
    # So if the sql file has "--" based comments, removing \n and \t will make the-- comments break the query, so all comments in the source .sql file must be explicitly closed via /* and */
    command2 = command.replace("\n", " ")
    command2 = command2.replace("\t", " ")
    
	# submit the constructed BCP command.  BCP will now execute, connecting to the server using Windows authentication, running the query.
	# BCP will write the file to the specified path, python doens't need to handle this.
    os.system(command2)
    
    print("{}.txt complete. \n waiting 5 seconds to start next iteration...".format(dates.filename[x]))
    os.system("timeout 5")


print("done")

# to run type  %run "SCM Pharm BCP Script.py"  in the IPython console
