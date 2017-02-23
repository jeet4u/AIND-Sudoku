# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In contraint propagation certains contrained are determined for the variables relating to the prolem at hand and these contrains are
    repededly applied in an attept to find the solution. For the Naked twins the constraint is that when two boxes and the same two digit number
    than none of the other peers of those boxes can have those two number. This Contraint applied by finding all the boxes with similar two digits
    and than finding their common peers and elimination those digits from the peers.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The contraint, that both diagonals must have unique 9 digits, is made a part of the solution by appending diagonals to the list of units.
    This makes eliminate, only choice and naked twin strategies run by effectively propagating and including the diagonal containts which solves the Sudoku.

