"""
    A basic psuedo-SQL micro program
"""

from reading import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def read_query(qry_input):
    ''' (str) -> list of strs and lists

    Take the input query and split its tokens into a list, then split
    the list tokens into lists. Return the list of the tokens.

    >>> read_query("select * from movies,oscars where o.title=m.title,\
    m.gross>'2'")
    ['select', ['*'], 'from', ['movies','oscars'], 'where',\
    ['o.title=m.title',"m.gross>'2'"]]
    >>> read_query("select o.title from oscars")
    ['select', ['o.title'], 'from', ['oscars']]
    '''
    # create a query_list by splitting the qry_input at its spaces
    query_list = qry_input.split()
    # split the select and from statements at their commas
    query_list[1] = query_list[1].split(',')
    query_list[3] = query_list[3].split(',')
    # if there is a where statement, split it at the commas
    if(len(query_list) >= 5):
        query_list[5] = query_list[5].split(',')
    # return the query_list
    return query_list


def num_rows(table):
    ''' (table) -> int

    return the number of rows in the table.

    >>> num_rows({'a':['b','c']})
    2
    '''
    # create a list of the keys in the table
    keys = find_table_keys(table)
    # create a variable for the rows setting the value as the length of the
    # first column
    rows = len(table[keys[0]])
    # go through each of the keys in the table
    for key in keys:
        # if the length of one column differs from the past ones then return
        # error code 3
        if(len(table[key]) != rows):
            return 'error 3'
    # return the number of rows
    return rows


def cartesian_product(table1, table2):
    ''' (table, table) -> table

    take two tables and combine them into one.

    >>> cartesian_product({'a':['b','c']}, {'d':['e','f']})
    {'a':['b', 'b', 'c', 'c'], 'd':['e', 'f', 'e', 'f']}
    >>> cartesian_product({'a':[]}, {'b':['c', 'd']})
    {'a':[], 'b'[]}
    '''
    # create and empty dictionary for the result variable
    res = {}
    # find the number of rows in both tables
    table2_rows = num_rows(table2)
    table1_rows = num_rows(table1)
    # create a list of the keys for keys in both tables
    table1_keys = find_table_keys(table1)
    table2_keys = find_table_keys(table2)
    # create empty lists in the result variable for each column in the two
    # tables
    for key in table1_keys:
        res[key] = []
    for key in table2_keys:
        res[key] = []
    # if the length of either table is 0 return the result
    if(len(table1) == 0 or len(table2) == 0):
        return res
    # create two counters, one for the number of keys in table1, and one for
    # the number of rows in each column
    for i in range(len(table1_keys)):
        for i2 in range(len(table1[table1_keys[i]])):
            # add each entry of table1 times the number of rows in table2
            res[table1_keys[i]] += [table1[table1_keys[i]][i2]]*table2_rows
    # create two counters, on for the number of keys in table2, and one for
    # the number of rows in each column
    for i in range(len(table2_keys)):
        for i2 in range(len(table2[table2_keys[i]])):
            # add a copy of table 2 to the result
            res[table2_keys[i]] += [table2[table2_keys[i]][i2]]
        # duplicate this copy by the number of rows in table1
        res[table2_keys[i]] = table2[table2_keys[i]] * table1_rows
    # return the result
    return res


def find_table_keys(table):
    ''' (table) -> list of str

    Take a table and extract its keys returning them in the form of a list.

    >>> find_table_keys({'a':[],'b':[],'c':[]})
    ['a', 'b', 'c']
    >>> find_table_keys({'d':[]})
    ['d']
    '''
    # return the keys in the table in list form
    return list(table.keys())


def do_from(query):
    ''' (str) -> table

    Return the cartesian product of the tables listed in an inputted SQuEaL
    query

    >>> do_from('select o.title from movies,oscars')
    {'o.category': ['Animated Feature Film', 'Directing', 'Directing',\
    'Best Picture', 'Animated Feature Film', 'Directing', 'Directing',\
    'Best Picture', 'Animated Feature Film', 'Directing', 'Directing',\
    'Best Picture'], 'm.year': ['1997', '1997', '1997', '1997', '2003',\
    '2003', '2003', '2003', '2010', '2010', '2010', '2010'], 'o.year':\
    ['2010', '2003', '1997', '1997', '2010', '2003', '1997', '1997', '2010',\
    '2003', '1997', '1997'], 'o.title': ['Toy Story 3', 'The Lord of the\
    Rings: The Return of the King', 'Titanic', 'Titanic', 'Toy Story 3',\
    'The Lord of the Rings: The Return of the King', 'Titanic', 'Titanic',\
    'Toy Story 3', 'The Lord of the Rings: The Return of the King',\
    'Titanic', 'Titanic'], 'm.title': ['Titanic', 'Titanic', 'Titanic',\
    'Titanic', 'The Lord of the Rings: The Return of the King', 'The Lord\
    of the Rings: The Return of the King', 'The Lord of the Rings: The\
    Return of the King', 'The Lord of the Rings: The Return of the King',\
    'Toy Story 3', 'Toy Story 3', 'Toy Story 3', 'Toy Story 3'], 'm.gross':\
    ['2186.8', '2186.8', '2186.8', '2186.8', '1119.9', '1119.9', '1119.9',\
    '1119.9', '1063.2', '1063.2', '1063.2', '1063.2'], 'm.studio': ['Par.',\
    'Par.', 'Par.', 'Par.', 'NL', 'NL', 'NL', 'NL', 'BV', 'BV', 'BV', 'BV']}
    >>> do_from('select o.title from oscars')
    {'o.category': ['Animated Feature Film', 'Directing', 'Directing', 'Best\
    Picture'], 'o.title': ['Toy Story 3', 'The Lord of the Rings: The Return\
    of the King', 'Titanic', 'Titanic'], 'o.year': ['2010', '2003', '1997',\
    '1997']}
    '''
    # create an empty dictionary variable
    table_list = {}
    # create a list out of the query
    query_list = read_query(query)
    # for each table in the list of table names in the query
    for table_name in query_list[3]:
        # add each table to the table_list dictionary
        table_list[table_name] = read_table(table_name + '.csv')
    # if the number of tables is two or greater
    if(len(query_list[3]) >= 2):
        # set the temporary table equal to the for table in the from clause
        # of the query
        temp_table = table_list[query_list[3][0]]
        # create a counter up to one less that the number of tables in the
        # from clause of the query
        for i in range(len(query_list[3])-1):
            # set the temporary table equal to the cartesian product of the
            # temporary table and the next table in the from clause
            temp_table = cartesian_product(temp_table, table_list[query_list
                                                                  [3][i+1]])
    # if there is only one table set the temporary table equal to it
    else:
        temp_table = table_list[query_list[3][0]]
    # returnt the temporary table
    return temp_table


def read_where(where_list):
    ''' (list of str) -> list of str and int

    Take the list of 'where' statements from a query and classify it as a
    1 (greater than, statement) or a 2 (less than, statement) and then return
    the statements in a list with each being split at its operater and
    beginning with its classification number (1 or 2)

    >>> read_where(["a>b","a='4'"])
    [1, 'a', 'b', 2, 'a', "'4'"]
    '''
    # create an empty list for the list of constraints
    constraints_list = []
    # for each constraint in the where list
    for constraint in where_list:
        # if the constraint is a greater than statement
        if('>' in constraint):
            # add the code '1' and then add the constraint, split at the
            #'greater than' operator
            constraints_list += [1]
            constraints_list += constraint.split('>')
        # if the constraint is an equal to statement
        elif('=' in constraint):
            # add the code '2' and then add the constraint, split at the
            # 'equal to' operator
            constraints_list += [2]
            constraints_list += constraint.split('=')
    # return the list of constraints
    return constraints_list


def do_constraint_1(table, constraints_list, table_keys, i, current_key):
    ''' (table, list of str, list of str, int, str) -> table

    this will occur if 'where' clause is of classification 1; take a table
    remove any rows that do not obey the 'where' clause.

    >>> do_constraint_1({'a':[2], 'b':[7]}, [1, 'a', 'b'], ['a','b'], 0, 'a')
    {'a': [], 'b': []}
    >>> do_constraint_1({'a':[7], 'b':[2]}, [1, 'a', 'b'], ['a','b'], 0, 'a')
    {'a': [7], 'b': [2]}
    '''
    # create an empty result dictionary
    res = {}
    # at each key in the table keys make an empty list in res
    for key in table_keys:
        res[key] = []
    # create a counter up to the length of column
    for i2 in range(len(table[current_key])):
        # if the constraint does not contain a single quote (')
        if(not "'" in constraints_list[i+2]):
            # if the row of the first constraint column is greater than the
            # row of the second constraint column
            if(table[constraints_list[i+1]][i2] > table[constraints_list[i+2]
                                                        ][i2]):
                # add in the entire row for each of the columns
                for i3 in range(len(table_keys)):
                    i3_key = table_keys[i3]
                    res[i3_key] += [table[i3_key][i2]]
        # if the constraint does not contain a single quote
        elif("'" in constraints_list[i+2]):
            # if the row of the first constraint column is greater than the
            # value of the second constraint column
            if(int(table[constraints_list[i+1]][i2]) > float(constraints_list
                                                             [i+2].strip("'")
                                                             )):
                # add in the entire row for each of the columns
                for i3 in range(len(table_keys)):
                    i3_key = table_keys[i3]
                    res[i3_key] += [table[i3_key][i2]]
    # return the result
    return res


def do_constraint_2(table, constraints_list, table_keys, i, current_key):
    ''' (table, list of str, list of str, int, str) -> table

    this will occur if 'where' clause is of classification 2; take a table
    remove any rows that do not obey the 'where' clause.

    >>> do_constraint_2({'a':['c'], 'b':['c']}, [1, 'a', 'b'], ['a','b'], 0,\
    'a')
    {'a': ['c'], 'b': ['c']}
    >>> do_constraint_2({'a':['d'], 'b':['f']}, [1, 'b', "f"], ['a','b'], 0,\
    'a')
    {'a': ['d'], 'b': ['f']}
    '''
    # create an empty result dictionary
    res = {}
    # at each key in the table keys make an empty list in res
    for key in table_keys:
        res[key] = []
    # create a counter up to the length of the column
    for i2 in range(len(table[current_key])):
        # if the constraint does not contain a single quote (')
        if(not "'" in constraints_list[i+2]):
            # if the row of the first constraint column is equal to the
            # row of the second constrain column
            if(table[constraints_list[i+1]][i2] == table[constraints_list
                                                         [i+2]][i2]):
                # add in the entire row for each column
                for i3 in range(len(table_keys)):
                    i3_key = table_keys[i3]
                    res[i3_key] += [table[i3_key][i2]]
        # if the constraint does not contain a single quote
        elif("'" in constraints_list[i+2]):
            # if the row of the first constrant column is equal to the value
            # of the second constraint column
            if((table[constraints_list[i+1]][i2]) == (constraints_list[i+2].
                                                      strip("'"))):
                # add in the entire row for each of the columns
                for i3 in range(len(table_keys)):
                    i3_key = table_keys[i3]
                    res[i3_key] += [table[i3_key][i2]]
    # return the result
    return res


def do_where(where_list, table):
    ''' (list of str/int, table) -> table

    take a list of 'where' clauses and a table and return the table removing
    all rows that do not obey the 'where' clauses.

    >>> do_where(['a=d'], {'a':['b', 'c'],'d':['b', 'f']})
    {'a':['b'], 'd':['b']}
    '''
    # create a list of the constraints and table keys
    constraints_list = read_where(where_list)
    table_keys = find_table_keys(table)
    # create a counter from 0 up to the number of constraints jumping by
    # three each time
    for i in range(0, len(constraints_list), 3):
        # create a constraint variable tracking the constraint currently
        # being looked at
        constraint = constraints_list[i]
        # create a variable for the current columns for the constraint
        key = constraints_list[i+1]
        # if the constraint code is 1 set the result equal to the result of
        # do_constraint_1
        if(constraint == 1):
            res = do_constraint_1(table, constraints_list, table_keys, i, key)
        # if the ocnstraint code is 2 set the result equal to the result of
        # do_constrain_2
        elif(constraint == 2):
            res = do_constraint_2(table, constraints_list, table_keys, i, key)
    # return the result
    return res


def do_select(query_list, temp_table):
    ''' (list of str, table) -> table

    Take the list form of the query and a table and remove all columns that
    are not in the select token of the query.

    >>> do_select(['select', ['a'], 'from', ['abtable']], {'a':[1,2,3,4],\
    'b':[5,6,7,8]})
    {'a':[1,2,3,4]}
    '''
    # create an empty dictionary for a result variable
    res = {}
    # create a list of the table keys
    table_keys = find_table_keys(temp_table)
    # if the select token of the query list is '*' then set the result
    # variable equal to the temporary table
    if(query_list[1][0] == "*"):
        res = temp_table
    else:
        # for each column in the table
        for key in table_keys:
            # if the column is in the list of selected columns in the query
            if(key in query_list[1]):
                # add the column to the result variable
                res[key] = temp_table[key]
    # return the result
    return res


def test_failure(query):
    ''' (str) -> int

    try to catch some common mistakes that are made. Hopefully most
    failures will be caught by this and the user will be able to fix the
    issues themselves.

    >>> test_failure("select yo from oscas")
    1
    >>> test_failure("asdfadsf")
    5
    '''
    # if there is no select or from token in the query return error code 5
    if((not "select" in query) or (not "from" in query)):
        return 5
    # create a database and a list of the tables in the database
    database = read_database()
    database_keys = find_table_keys(database)
    # create a list of the query and an empty list varible for the table keys
    query_list = read_query(query)
    table_keys = []
    # for each table in the from clause of the query
    for table in query_list[3]:
        # if the table is not in the database return error code 1
        if(not table in database_keys):
            return 1
        # if the num_rows returns the error 3 code return error code 3
        # create a variable for the current table in its table form (not just
        # the name)
        table_in_form = database[table]
        if(num_rows(table_in_form) == 'error 3'):
            return 3
        # add in all of the columns from each table in the query
        for column in database[table]:
            table_keys += find_table_keys(database[table])
    # for each column in the query
    for column in query_list[1]:
        # if the query uses the special '*' ignore it
        if(column == '*'):
            pass
        # if the column does not exist any of the tables in the query, return
        # error code 2
        elif(not column in table_keys):
            return 2
    # if there is no columns or tables in the query return error code 4
    if(len(query_list[1]) == 0 or len(query_list[3]) == 0):
        return 4


def run_program(query):
    ''' (str) -> str/table

    run the entire query performing all steps of the program. REQ: the query
    must be in the correct form

    >>> run_program('select o.title,m.title from oscars,movies')
    {'o.title': ['Toy Story 3', 'Toy Story 3', 'Toy Story 3', 'The Lord of\
    the Rings: The Return of the King', 'The Lord of the Rings: The Return\
    of the King', 'The Lord of the Rings: The Return of the King', 'Titanic'\
    , 'Titanic', 'Titanic', 'Titanic', 'Titanic', 'Titanic'], 'm.title': ['\
    Titanic', 'The Lord of the Rings: The Return of the King', 'Toy Story 3\
    ', 'Titanic', 'The Lord of the Rings: The Return of the King', 'Toy Sto\
    ry 3', 'Titanic', 'The Lord of the Rings: The Return of the King', 'Toy\
    Story 3', 'Titanic', 'The Lord of the Rings: The Return of the King', 'T\
    oy Story 3']}
    >>> run_program('select * from movies')
    {'m.title': ['Titanic', 'The Lord of the Rings: The Return of the King',\
    'Toy Story 3'], 'm.gross': ['2186.8', '1119.9', '1063.2'], 'm.studio': [\
    'Par.', 'NL', 'BV'], 'm.year': ['1997', '2003', '2010']}
    '''
    # create a variable testing if any failure codes occur
    failure_code = test_failure(query)
    # if a code does occur return the corresponding error
    if(failure_code == 1):
        return "The table does not exist in the database."
    elif(failure_code == 2):
        return "A column entered is not in any of the tables."
    elif(failure_code == 3):
        return "A table within the query has columns or different lengths."
    elif(failure_code == 4):
        return "The query does not have a column or table"
    elif(failure_code == 5):
        return "The query does not have the mandatory select/from token"
    # create a query list
    query_list = read_query(query)
    # set the result variable to the result of do_from on the query
    res = do_from(query)
    # if the query includes a where statement
    if(len(query_list) >= 5):
        # create a where list variable
        where_list = query_list[5]
        # set the result variable equal to the result of do_where
        res = do_where(where_list, res)
    # set the result variable equal to the result of do_select
    res = do_select(query_list, res)
    # return the result
    return res

# helper function for outputting tables


def print_csv(table):
    '''(table) -> NoneType

    Print a representation of table.

    '''
    columns = list(table.keys())
    print(','.join(columns))
    rows = num_rows(table)
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(table[column][i])
        print(','.join(cur_column))


if(__name__ == "__main__"):
    # set the query so that it will satisfy the while loop
    query = " "
    # while the query does not equal "DONE" or nothing
    while(query != "DONE" and query != ""):
        # set the query equal to the query inputted by the user
        query = input("Enter a SQuEaL query, type 'DONE' to exit:")
        # if the does not equal "DONE" or is empty then print the result of
        # running the program on the inputted query
        if(query != "DONE" and query != ""):
            print_csv(run_program(query))
