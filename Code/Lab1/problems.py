from node import Node
import copy

class FifteensNode(Node):
    """Extends the Node class to solve the 15 puzzle.

    Parameters
    ----------
    parent : Node, optional
        The parent node. It is optional only if the input_str is provided. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this puzzle it is the number of moves to reach this node from the initial configuration.
        It is optional only if the input_str is provided. Default is 0.

    board : list of lists
        The two-dimensional list that describes the state. It is a 4x4 array of values 0, ..., 15.
        It is optional only if the input_str is provided. Default is None.

    input_str : str
        The input string to be parsed to create the board.
        The argument 'board' will be ignored, if input_str is provided.
        Example: input_str = '1 2 3 4\n5 6 7 8\n9 10 0 11\n13 14 15 12' # 0 represents the empty cell

    Examples
    ----------
    Initialization with an input string (Only the first/root construction call should be formatted like this):
    >>> n = FifteensNode(input_str=initial_state_str)
    >>> print(n)
      5  1  4  8
      7     2 11
      9  3 14 10
      6 13 15 12

    Generating a child node (All the child construction calls should be formatted like this) ::
    >>> n = FifteensNode(parent=p, g=p.g+c, board=updated_board)
    >>> print(n)
      5  1  4  8
      7  2    11
      9  3 14 10
      6 13 15 12

    """

    def __init__(self, parent=None, g=0, board=None, input_str=None):
        # NOTE: You shouldn't modify the constructor
        if input_str:
            self.board = []
            for i, line in enumerate(filter(None, input_str.splitlines())):
                self.board.append([int(n) for n in line.split()])
        else:
            self.board = board

        super(FifteensNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by trying all 4 possible moves of the empty cell.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """

        # TODO: add your code here
        # You should use self.board to produce children. Don't forget to create a new board for each child
        # e.g you can use copy.deepcopy function from the standard library.

        # generate the childrenlist to return
        children_node_list = []

        # find the position of emptycell
        emptycell_row = -1
        emptycell_col = -1
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    emptycell_row = i
                    emptycell_col = j

        # exchange the position of emptycell and its neighbour
        # Loop through possible column shifts: -1 and 1
        for col_diff in [-1, 1]:
            # Check if the new column index is within bounds (0 to 3)
            if 0 <= emptycell_col + col_diff <= 3:
                child = copy.deepcopy(self.board)
                neighbour = child[emptycell_row][emptycell_col + col_diff]
                child[emptycell_row][emptycell_col] = neighbour
                child[emptycell_row][emptycell_col + col_diff] = 0
                child_g = self.g + 1
                childnode = FifteensNode(self, child_g, child)
                children_node_list.append(childnode)

        # Loop through possible row shifts: -1 and 1
        for row_diff in [-1, 1]:
            # Check if the new row index is within bounds (0 to 3)
            if 0 <= emptycell_row + row_diff <= 3:
                child = copy.deepcopy(self.board)
                neighbour = child[emptycell_row + row_diff][emptycell_col]
                child[emptycell_row][emptycell_col] = neighbour
                child[emptycell_row + row_diff][emptycell_col] = 0
                child_g = self.g + 1
                childnode = FifteensNode(self, child_g, child)
                children_node_list.append(childnode)

        return children_node_list


    def is_goal(self):
        """Decides whether this search state is the final state of the puzzle.

        Returns
        -------
            is_goal : bool
                True if this search state is the goal state, False otherwise.
        """

        # TODO: add your code here
        # You should use self.board to decide.

        base = 1
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != base:
                    return False
                base = base + 1
                if base == 16:
                    return True
        return True

    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of moves
        required to reach the goal state from this node.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """

        # TODO: add your code here
        # You may want to use self.board here.

        heuristic_value = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != 0:
                    # calculate the goal coordinate of the specific value
                    goal_row = self.board[i][j] // 4.1
                    goal_col = 3 - ((goal_row + 1) * 4 - self.board[i][j])
                    heuristic_value += abs(goal_row - i) + abs(goal_col - j)
        return heuristic_value


    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple([n for row in self.board for n in row])

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = []  # String builder
        for row in self.board:
            for i in row:
                sb.append(' ')
                if i == 0:
                    sb.append('  ')
                else:
                    if i < 10:
                        sb.append(' ')
                    sb.append(str(i))
            sb.append('\n')
        return ''.join(sb)


class SuperqueensNode(Node):
    """Extends the Node class to solve the Superqueens problem.

    Parameters
    ----------
    parent : Node, optional
        The parent node. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this problem it is the number of pairs of superqueens that can attack each other in this state configuration.
        Default is 1.

    queen_positions : list of pairs
        The list that stores the x and y positions of the queens in this state configuration.
        Example: [(q1_y,q1_x),(q2_y,q2_x)]. Note that the upper left corner is the origin and y increases downward
        Default is the empty list [].
        ------> x
        |
        |
        v
        y

    n : int
        The size of the board (n x n)

    Examples
    ----------
    Initialization with a board size (Only the first/root construction call should be formatted like this):
    >>> n = SuperqueensNode(n=4)
    >>> print(n)
         .  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    Generating a child node (All the child construction calls should be formatted like this):
    >>> n = SuperqueensNode(parent=p, g=p.g+c, queen_positions=updated_queen_positions, n=p.n)
    >>> print(n)
         Q  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    """

    def __init__(self, parent=None, g=0, queen_positions=[], n=1):
        # NOTE: You shouldn't modify the constructor
        self.queen_positions = queen_positions
        self.n = n
        super(SuperqueensNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by adding a new queen.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """
        # TODO: add your code here
        # You should use self.queen_positions and self.n to produce children.
        # Don't forget to create a new queen_positions list for each child.
        # You can use copy.deepcopy function from the standard library.

        # the next being place queen's x (from 0 to n-1)
        position_x = len(self.queen_positions)
        forbidden_y = set()
        all_y = set()
        for tuple in self.queen_positions:
            forbidden_y.add(tuple[0])
            forbidden_y.add(tuple[0] + position_x - tuple[1])
            forbidden_y.add(tuple[0] - position_x - tuple[1])
        for i in range(self.n):
            all_y.add(i)
        # do the difference of two sets to find the y can be placed
        possible_y = all_y - forbidden_y

        # put all possible child node into list
        child_node_list = []
        for position_y in possible_y:
            child_queen_positions = copy.deepcopy(self.queen_positions)
            child_queen_positions.append((position_y, position_x))
            child_g = self.g + 1
            child_node = SuperqueensNode(self, child_g, child_queen_positions, self.n)
            child_node_list.append(child_node)

        return child_node_list

    def is_goal(self):
        """Decides whether all the queens are placed on the board.

        Returns
        -------
            is_goal : bool
                True if all the queens are placed on the board, False otherwise.
        """
        # You should use self.queen_positions and self.n to decide.
        # TODO: add your code here

        if len(self.queen_positions) == self.n:
            position_y = set()
            for tuple in self.queen_positions:
                position_y.add(tuple[0])
            if len(position_y) == self.n:
                return True
        return False


    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of conflicts required to reach the final state.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """
        # If you want to design a heuristic for this problem, you should use self.queen_positions and self.n.
        # TODO: add your code here (optional)
        return 0

    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple(self.queen_positions)

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = [[' . '] * self.n for i in range(self.n)]  # String builder
        for i, j in self.queen_positions:
            sb[i][j] = ' Q '
        return '\n'.join([''.join(row) for row in sb])
