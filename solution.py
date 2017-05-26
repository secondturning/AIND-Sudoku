assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [ ['A1','B2','C3','D4','E5','F6','G7','H8','I9'], ['A9','B8','C7','D6','E5','F4','G3','H2','I1'] ]
unitlist = row_units + col_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit_group in unitlist:
        processed_values = []
        for unit in unit_group:
            if len(values[unit]) == 2:
                if values[unit] not in processed_values:
                    peer_unit_with_same_value = next((peer for peer in unit_group if peer != unit and values[peer] == values[unit]),None)
                    if peer_unit_with_same_value:
                        processed_values.append(values[unit])
                        for digit in values[unit]:
                            for check_unit in unit_group:
                                if (len(values[check_unit]) > 1) and (check_unit != peer_unit_with_same_value) and (check_unit != unit):
                                    assign_value(values, check_unit, values[check_unit].replace(digit,''))

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
    dict = {}
    for idx, box in enumerate(boxes):
        dict[box] = grid[idx] if grid[idx] != '.' else '123456789'
    return dict        

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for box in values:
        if len(values[box]) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(values[box],''))

def only_choice(values):
    for unit_group in unitlist:
        counts = {}
        for unit in unit_group:
            for digit in list(values[unit]):
                if digit in counts.keys():
                    counts[digit] = counts[digit] + 1
                else:
                    counts[digit] = 1
        for key in counts:
            if counts[key] == 1:
                for unit in unit_group:
                    if len(values[unit]) > 1:
                        if key in values[unit]:
                            assign_value(values, unit, key)
                            # values[unit] = key    

def no_of_solved_boxes(values):
    return len([box for box in boxes if len(values[box]) == 1])

def reduce_puzzle(values):
    stop_reducing = False
    while not stop_reducing:
        sovled_boxes = no_of_solved_boxes(values)
        eliminate(values)
        only_choice(values)
        new_solved_boxes = no_of_solved_boxes(values)
        stop_reducing = new_solved_boxes == sovled_boxes
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

def search(values):
    result = reduce_puzzle(values)
    if result is False:
        return False
    if no_of_solved_boxes(values) == 81:
        return values
    min_length = 9
    min_length_box = None
    for box in boxes:
        if len(values[box]) > 1 and len(values[box]) < min_length:
            min_length = len(values[box])
            min_length_box = box
    if min_length_box:
        for digit in values[min_length_box]:
            new_values = values.copy()
            new_values[min_length_box] = digit
            attempt = search(new_values)
            if attempt:
                return attempt

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
