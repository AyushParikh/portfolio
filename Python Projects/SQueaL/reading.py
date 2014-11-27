# Functions for reading tables and databases


import glob

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.


# Write the read_table and read_database functions below

def read_table(file_name):
    ''' (str) -> table

    open the file 'file_name' and read it changing it from a text format to a
    table, which is a dictionary with its keys being the column names and the
    data being a list of all the data in the columns below
    
    >>> read_table("movies.csv")
    {'m.year': ['1997', '2003', '2010'], 'm.title': ['Titanic', 'The Lord of\
 the Rings: The Return of the King', 'Toy Story 3'], 'm.gross': ['2186.8',\
 '1119.9', '1063.2'], 'm.studio': ['Par.', 'NL', 'BV']}
    >>> read_table("oscars.csv")
    {'o.category': ['Animated Feature Film', 'Directing', 'Directing',\
 'Best Picture'], 'o.year': ['2010', '2003', '1997', '1997'], 'o.title':\
 ['Toy Story 3', 'The Lord of the Rings: The Return of the King',\
 'Titanic', 'Titanic']}
    '''
    # import the list of all .csv files into the directory and create a
    # result variable
    file_list =  glob.glob('*.csv')
    res = {}
    # go through each file in the file_list
    if file_name in file_list:
        # open the file and convert it's lines into a list, close the file
        file = open(file_name, 'r')
        line_list = file.readlines()
        file.close()
        # create a counter up to the number of lines in the file
        for i in range(len(line_list)):
            # strip each line of its newline '\n' and split it into a list at
            # the commas
            line_list[i] = line_list[i].strip('\n')
            line_list[i] = line_list[i].split(',')
            # create a second counter up to the number of items in the newly
            # split line
            for i2 in range(len(line_list[i])):
                # strip each item of its spaces at the beginning and end
                line_list[i][i2] = line_list[i][i2].strip(' ')
        # go through the names of the column
        for i in line_list[0]:
            # create an empty list for each column name
            res[i] = []
        # create a counter from 1 to length of the line_list
        for i in range(1,len(line_list)):
            # create a second counter up to the length of line_list[i]
            for i2 in range(len(line_list[i])):
                # for the column, add each element down the column to it
                res[line_list[0][i2]] += [line_list[i][i2]]
        # return the table
        return(res)



def read_database():
    ''' () -> database
    
    read all the tables in the directory and put them into the format of a
    database where the keys are table names and the data are the tables
    themselves
    
    >>> read_database()
    {'movies':{'m.studio': ['Par.', 'NL', 'BV'], 'm.gross': ['2186.8',\
    '1119.9', '1063.2'], 'm.title': ['Titanic', 'The Lord of the Rings: The\
    Return of the King', 'Toy Story 3'], 'm.year': ['1997', '2003', '2010']},\
    'oscars':{'o.category': ['Animated Feature Film', 'Directing',\
    'Directing', 'Best Picture'], 'o.year': ['2010', '2003', '1997', '1997'],\
    'o.title': ['Toy Story 3', 'The Lord of the Rings: The Return of the\
    King', 'Titanic', 'Titanic']}}
    '''
    # create an empty result variable and a list of files in the directory
    res = {}
    file_list =  glob.glob('*.csv')
    # go through each file in the list
    for file in file_list:
        # read the table
        table = read_table(file)
        # create a variable for the filename without the .csv at the end
        filename = file[:len(file)-4]
        # add to the database the table using the filename as the key
        res[filename] = table
    # return the database
    return res