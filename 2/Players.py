'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

from os import terminal_size
import threading
import itertools
import time
import sys

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

    """Not my code, taken from https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
    Does not implement any critical functionalities to the assignment, just a loading bar for convenience. 
    """
    def animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.waiting == False:
                break
            sys.stdout.write('\rloading.. ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.flush()
        print('\rDone!       ')
    """End of not my code"""


    # From here down, all the code in this file was written by me (Alaric Hartsock)

    """
    Determines the move from the 
    """
    def get_move(self, board):

        # self.waiting = True
        # t = threading.Thread(target=self.animate)
        # t.start()

        if self.head == None:
            self.head = Node(board, self.symbol, self.oppSym)
            self.expandTree(self.head)
            self.miniMax(self.head)
        else:
            pass
            
        if self.head.board == board: # If our head is pointed at the current board state, then pass.
            pass
        else: # Else update the head to be pointed at the current board state
            for i in self.head.children:
                if i.board == board:
                    self.head = i
            if self.head.parent.board == board:
                self.head = self.head.parent
            elif self.head.board != board:
                print("DEBUG: Regenerating tree unnecessarily. To improve performance, debug")
                self.head = Node(board, self.symbol, self.oppSym)
                self.expandTree(self.head)
                self.miniMax(self.head)

        # while self.head != None:
        #     print(str(self.head))
        #     print("minmax: " + str(self.head.minimax_value))
        #     print("utility: " + str(self.head.terminal_value))
        #     try:
        #         self.head = self.head.children.pop()
        #     except IndexError as e:
        #         print("Reached end of tree")
        #         self.head = None

        # Determine next best move for robot

        bestchild = self.findBestChild(self.head.children[0],self.head.children)

        col = bestchild.move[0]
        row = bestchild.move[1]

        while col == None and row == None:
            bestchild = self.findBestChild(bestchild.children[0],bestchild.children)

            col = bestchild.move[0]
            row = bestchild.move[1]

        self.head = bestchild

        # self.waiting = False

        # t.join()
        return  (col, row)

    def findBestChild(self,bestchild,children):


        for child in children:
            if (child.terminal_node == True and bestchild.terminal_node == True):
                if (child.terminal_value >= bestchild.terminal_value):
                    bestchild = child
                else:
                    pass
            elif (child.terminal_node == True and bestchild.terminal_node == False):
                if child.terminal_value >= bestchild.minimax_value:
                    bestchild = child
                else:
                    pass
            elif (child.terminal_node == False and bestchild.terminal_node == True):
                if child.minimax_value >= bestchild.terminal_value:
                    bestchild = child
                else: 
                    pass
            else: # Child and bestchild are both nonterminal nodes
                if child.minimax_value >= bestchild.minimax_value:
                    bestchild = child
        
        return bestchild

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

        self.move = None # Move required to get to this state from the parent state

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
    Sets the child, appending it to the children class and automatically setting the parent as equal to the current node
    """
    def set_child(self,move):
        child = Node(move[0], self.oppsym, self.symbol)
        child.move = move[1]
        child.parent = self

        self.children.append(child)

        if len(self.children) > 0:
            self.terminal_node = False

    """
    Automatically generates children for current node (not entire tree). Uses the set_child method. 
    """
    def birth_babies(self):
        for i in self.get_succ(self.board,self.symbol,self.oppsym):
            self.set_child(i)

    """
    Finds all legal board states after this current board state and returns them in a list.
    """
    def get_succ(self,board,symbol,oppsym):
        moves = []

        if board.has_legal_moves_remaining(symbol):
            for i in range (0, board.cols):
                for j in range (0, board.rows):
                    if board.is_cell_empty(i, j) and board.is_legal_move(i, j, symbol):
                        newBoard = board.cloneOBoard()
                        newBoard.play_move(i,j,symbol)
                        moves.append([newBoard,(i,j)])
        else: # In this case, current player has no legal moves but the opponent does. So the opponent can go twice or rarely, more in some cases
            if board.has_legal_moves_remaining(oppsym):
                newBoard = board.cloneOBoard()
                moves.append([newBoard,(None,None)])

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