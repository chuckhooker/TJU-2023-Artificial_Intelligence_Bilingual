"""Implementation of the A* algorithm.

This file contains a skeleton implementation of the A* algorithm. It is a single
method that accepts the root node and runs the A* algorithm
using that node's methods to generate children, evaluate heuristics, etc.
This way, plugging in root nodes of different types, we can run this A* to
solve different problems.

"""


def Astar(root):
    """Runs the A* algorithm given the root node. The class of the root node
    defines the problem that's being solved. The algorithm either returns the solution
    as a path from the start node to the goal node or returns None if there's no solution.

    Parameters
    ----------
    root: Node
        The start node of the problem to be solved.

    Returns
    -------
        path: list of Nodes or None
            The solution, a path from the initial node to the goal node.
            If there is no solution it should return None
    """

    # TODO: add your code here
    # Some helper pseudo-code:
    # 1. Create an empty fringe and add your root node (you can use lists, sets, heaps, ... )
    # 2. While the container is not empty:
    # 3.      Pop the best? node (Use the attribute `node.f` in comparison)
    # 4.      If that's a goal node, return node.get_path()
    # 5.      Otherwise, add the children of the node to the fringe
    # 6. Return None
    #
    # Some notes:
    # You can access the state of a node by `node.state`. (You may also want to store evaluated states)
    # You should consider the states evaluated and the ones in the fringe to avoid repeated calculation in 5. above.
    # You can compare two node states by node1.state == node2.state

    nodes = [root]
    evaluated_states = set()

    while nodes:
        # find the node with the minimum f
        min_f_node = min(nodes, key=lambda node: node.f)

        # for the exception that the root is the goal
        if min_f_node.is_goal():
            return min_f_node.get_path()

        # remove the parent node and add its state into evaluated_states
        nodes.remove(min_f_node)
        evaluated_states.add(min_f_node.state)

        # generate children node of the min_f_node and add it into nodes(whose state is not in evaluated_states)
        child_node_list = min_f_node.generate_children()
        new_nodes = []
        for node in child_node_list:
            if node.state not in evaluated_states:
                new_nodes.append(node)

        nodes.extend(new_nodes)

    return None