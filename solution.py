
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units1 = []
diagonal_units2 = []
for i in range(0,len(rows)):
        diagonal_units1 = diagonal_units1+(cross(rows[i],cols[i]))
for i in range(0,len(rows)):
        diagonal_units2 = diagonal_units2+(cross(rows[i],cols[len(rows)-1-i]))
diagonal_units = [diagonal_units1,diagonal_units2]
unitlist = row_units + column_units + square_units 

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diagonal_units
print(unitlist)

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def naked_twins(values):
    out = values.copy()
    for i in out:
        for j in peers[i]:
            if(out[i] == out[j]):
                if(len(out[i])==2):
                   for k in intersection(peers[i], peers[j]):
                       for w in out[i]:
                            out[k]=out[k].replace(w,"")
    return out
                   

def eliminate_aux(dict_):
    for i in peers:
        if(len(dict_[i])==1):
            pass
        else:
            for j in peers[i]:
                if (len(dict_[j])==1):
                    dict_[i]=dict_[i].replace(dict_[j],"")
    return dict_

def eliminate2(dict_):
    dict_aux = dict_.copy()
    dict_ = eliminate_aux(dict_)
    while(dict_aux != dict_):
        dict_aux = dict_.copy()
        dict_ = eliminate_aux(dict_)
    return dict_


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice_aux(dict_):
    for i in '123456789':
        for j in units:
            if i in dict_[j]:
                for k in units[j]:
                    if(len(dict_[j])==1):
                        break
                    for w in k:
                        if(i in dict_[w]):
                            if(w!=j):
                                break
                        if w == k[8]:
                            dict_[j] = i
    return dict_

def only_choice(dict_):
    dict_aux = dict_.copy()
    dict_ = only_choice_aux(dict_)
    while(dict_aux != dict_):
        dict_aux = dict_.copy()
        dict_ = only_choice_aux(dict_)
    return dict_

print('space')


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    n = 10
    values = reduce_puzzle(values)
    if(values == False): 
        return False
    aux = ''
    # Choose one of the unfilled squares with the fewest possibilities
    for i in boxes:
        if(len(values[i])!= 1 and len(values[i])<n):
            aux = i
            n = len(values[i])
    if(aux ==''):
        return values
    for i in values[aux]:
        dict_aux = values.copy()
        dict_aux[aux] = i
        possible_solution = search(dict_aux)
        if(possible_solution !=False):
            possible_solution = reduce_puzzle(possible_solution)
            return possible_solution
    return False


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
