rows = 'ABCDEFGHI'
cols = '123456789'
assignments = []


def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
dia1 = [[rows[i]+cols[i] for i in range(len(rows))]]    # First diagonal
dia2 = [[rows[i]+cols[::-1][i] for i in range(len(rows))]]  # Second diagonal
unitlist = row_units + column_units + square_units+ dia1 + dia2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    doubles = [num for num in values.keys() if len(values[num]) == 2]
    twins_hold = []  # hold the naked twin indexes

    for val in doubles:
        vpeers = peers[val]
        for b in vpeers:
            if values[b] == values[val] and (b != val):
                if ([b, val] not in twins_hold) and ([val, b] not in twins_hold):
                    twins_hold.append([b, val])  # List of Lists that hold the twins

    for i in range(len(twins_hold)):
        peers1 = peers[twins_hold[i][0]]
        peers2= peers[twins_hold[i][1]]
        rnum1 = values[twins_hold[i][0]][0]
        rnum2 = values[twins_hold[i][1]][1]
        common_peers = set.intersection(peers1, peers2)
        #  now replace rnum1 and rnum2 from the values in peers
        for val in common_peers:
            if len(values[val]) > 2:
                values[val] = values[val].replace(rnum1, '')
                values[val] = values[val].replace(rnum2, '')

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    dictResult = {}
    totalCount = 0
    for n in range(0, grid.__len__()):
        if (grid[n] == "."):
            dictResult[boxes[n]] = "123456789"
        else:
            dictResult[boxes[n]] = grid[n]

    return dictResult


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """Goes through all boxes and finds single digits results and eliminates them from the peers """
    for (k, v) in values.items():
        if (len(v) == 1):
            for p in peers[k]:
                values[p] = values[p].replace(v, "")

    return values
    pass


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    pass


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    '''creates a tree of possibilities and traverses it using DFS until it finds a solution for the sudoku puzzle.'''
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities

    valkey = "";
    n = 2
    found = False;
    while (n < 10 and found == False):
        for k, v in values.items():
            if (len(v) == n):
                valkey = k;
                found = True
                break;
        n += 1

    #  Now use recursion to find the solution, and if one returns a value (not False), return that answer!
    for val in values[valkey]:
        Values2 = values.copy()
        Values2[valkey] = val
        result = search(Values2)
        if result:
            return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


# gridv= grid_values('2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3')
# display(search(gridv))
