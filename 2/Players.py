'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

from os import terminal_size


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()

class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)

class MinimaxPlayer(Player):

    """
    Initializes Minimax player
    """
    def __init__(self, symbol):
        Player.__init__(self, symbol);
        self.head = None
        if symbol == 'X':
            self.symbol = 'X'
            self.oppSym = 'O'
        else:
            self.symbol = 'O'
            self.oppSym = 'X'

    # From here down, all the code in this file was written by me (Alaric Hartsock)

    """
    Determines the move from the 
    """
    def get_move(self, board):
        if self.head == None:
            self.head = Node(board, self.symbol, self.oppSym)
            self.expandTree(self.head)
            self.miniMax(self.head)
            print_tree(self.head)
        else:
            pass
            

        # while self.head != None:
        #     print(str(self.head))
        #     print(str(self.head.minimax_value))
        #     try:
        #         self.head = self.head.children.pop()
        #     except IndexError as e:
        #         print("Reached end of tree")
        #         self.head = None

        # Determine next best move for robot
        # col = 2
        # row = 0

        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)

    """
    Implements the minimax functionality and pseudocode
    """
    def miniMax(self,head):

        def maxValue(node):
            if node.terminal_node:
                return node.terminal_value
            v = -16 # -16 is the lowest score possible on a 4x4 othello board
            for child in node.children:
                v = max(v,minValue(child))
            node.minimax_value = v
            return v

        def minValue(node):
            if node.terminal_node:
                return node.terminal_value
            v = 16 # -16 is the highest score possible on a 4x4 othello board
            for child in node.children:
                v = min(v,maxValue(child))
            node.minimax_value = v
            return v

        if head.symbol == "O":
            maxValue(head)
        elif head.symbol == "X":
            minValue(head)
            

    """
    Recursively expands tree by birthing the babies of each node. 
    The recursion for a specific branch stops if a node doesn't have any children, meaning we've reached the terminal state of a game. 
    """
    def expandTree(self, head):
        head.birth_babies()

        for child in head.children:
            self.expandTree(child)
        
        if len(head.children) == 0:
            return head

class Node():

    def __init__(self,board,symbol,oppsym):
        self.board = board # Holds the board value of the node

        self.symbol = symbol # Symbol of the Node
        self.oppsym = oppsym # Symbol of the Node's adversary. If the node is an X, then the oppsym is O

        self.children = [] # List of children which the node has

        self.parent = None # Unset value which corresponds to its node parent parent
        self.value = None # Unset value which corresponds to its minimax value

        self.terminal_node = True # Node with no children, i.e its value is determined by the utility function rather than minmax. 
        self.terminal_value = self.utility_func(self)
        self.minimax_value = None

    def __iter__(self):
        """Overrides iterable function for pretty printing purposes"""
        return iter(self.children)

    """
    Counts the score for both symbols, returns symscore - oppsymscore is maximizing sybol and oppsymscore - symscore if minimizing symbol
    """
    def utility_func(self, node):
        symscore = 0
        oppsymscore = 0

        for i in range (0, node.board.cols):
            for j in range (0, node.board.rows):
                if self.board.grid[i][j] == node.symbol:
                    symscore +=1
                elif self.board.grid[i][j] == node.oppsym:
                    oppsymscore += 1
        
        if node.symbol == "O":
            score = symscore - oppsymscore
        elif node.symbol == "X":
            score = oppsymscore - symscore
        
        return score


    """
    Overrides Python's str method, this function will automatically be called when we call str(Nodeobject)
    """
    def __str__(self):
        return str(self.board)

    """
    
    """
    def __len__(self):
        return len(self.children)

    """
    Sets the child, appending it to the children class and automatically setting the parent as equal to the current node
    """
    def set_child(self,board):
        child = Node(board, self.oppsym, self.symbol)
        child.parent = self

        self.children.append(child)

        if len(self.children) > 0:
            self.terminal_node = False

    """
    Automatically generates children for current node (not entire tree). Uses the set_child method. 
    """
    def birth_babies(self):
        for i in self.get_succ(self.board,self.symbol):
            self.set_child(i)

    """
    Finds all legal board states after this current board state and returns them in a list.
    """
    def get_succ(self,board,symbol):
        moves = []

        if board.has_legal_moves_remaining(symbol):

            for i in range (0, board.cols):
                for j in range (0, board.rows):
                    if board.is_cell_empty(i, j) and board.is_legal_move(i, j, symbol):
                        newBoard = board.cloneOBoard()
                        newBoard.play_move(i,j,symbol)
                        moves.append(newBoard)
        return moves

"""NOT MY CODE."""
"""CODE ADAPTED FROM https://github.com/clemtoy/pptree/blob/master/pptree/pptree.py"""

def print_tree(current_node, childattr='children', nameattr='name'):
    if hasattr(current_node, nameattr):
        name = lambda node: getattr(node, nameattr)
    else:
        name = lambda node: " " + str(node.terminal_value) + " " if(node.terminal_node) else " " + str(node.minimax_value) + " "

    children = lambda node: getattr(node, childattr)
    nb_children = lambda node: sum(nb_children(child) for child in children(node)) + 1

    def balanced_branches(current_node):
        size_branch = {child: nb_children(child) for child in children(current_node)}

        """ Creation of balanced lists for "a" branch and "b" branch. """
        a = sorted(children(current_node), key=lambda node: nb_children(node))
        b = []
        while a and sum(size_branch[node] for node in b) < sum(size_branch[node] for node in a):
            b.append(a.pop())

        return a, b

    print_tree_horizontally(current_node, balanced_branches, name)
    print("\n")

def print_tree_horizontally(current_node, balanced_branches, name_getter, indent='', last='updown'):

    up, down = balanced_branches(current_node)

    """ Printing of "up" branch. """
    for child in up:     
        next_last = 'up' if up.index(child) == 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', ' ' * len(name_getter(current_node)))
        print_tree_horizontally(child, balanced_branches, name_getter, next_indent, next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print('{0}{1}{2}{3}'.format(indent, start_shape, name_getter(current_node), end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', ' ' * len(name_getter(current_node)))
        print_tree_horizontally(child, balanced_branches, name_getter, next_indent, next_last)

"""CODE ADAPTED FROM https://github.com/clemtoy/pptree/blob/master/pptree/pptree.py"""
"""NOT MY CODE. END"""