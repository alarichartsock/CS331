#!/usr/bin/python

import sys

def main():
    if len(sys.argv) > 1:
        """Takes in an input containing two sets of 3 integers separated by commas i.e 2,2,1.
        the list is ordered by chicken, wolves, boat. For example,
        3,3,1 would mean that 3 chickens and 3 wolves were on that side of the river
        and the boat as well. 2,3,0 means 2 chickens, 3 wolves, and no boat is on that side of the river
        In this case the left side is always considered to be the side that starts off with the boat.
        The right side is always the goal state, usually the second set of integers
        """
        
        try:
            inputfile=sys.argv[1]
        except IndexError:
            print("Please provide an input file in the format of python main.py inputfile.txt goalfile.txt searchmode outputfile.txt")
            raise Exception("Error: Please provide an argument ")            

        try:
            goalstate=sys.argv[2]
        except IndexError:
            print("Please provide an input file in the format of python main.py inputfile.txt goalfile.txt searchmode outputfile.txt")
            raise Exception("Error: Please provide a second argument ")

        try:
            mode=sys.argv[3]
        except IndexError:
            print("Please provide an input file in the format of python main.py inputfile.txt goalfile.txt searchmode outputfile.txt")
            raise Exception("Error: Please provide a third argument")

        try:
            outputfile=sys.argv[4]
        except IndexError:
            print("Please provide an input file in the format of python main.py inputfile.txt goalfile.txt searchmode outputfile.txt")
            raise Exception("Error: Please provide a fourth argument")

        try:
            u = open(inputfile, 'r') # turns file input into a list I can work with
            input = u.read().split('\n')
        except FileNotFoundError:
            print("Error: input file not found.")

        try:
            v = open(goalstate, 'r') # turns file input into a list I can work with
            goal = v.read().split('\n')
        except FileNotFoundError:
            print("Error: goal state file not found.")

        input = nestedStringtoInt(input)
        goal = nestedStringtoInt(goal)

        if input[0][2] == 1:
            left = input[0]
            right = input[1]
            final = goal[1]
        elif input[1][2] == 1:
            left = input[1]
            right = input[0]
            final = goal[0]

        head = River(left,right,None,0)

        if mode == "bfs":
            ret = triple(head,final,"bfs", -1)
        elif mode == "dfs":
            ret = triple(head,final,"dfs", -1)
        elif mode == "iddfs":
            ret = triple(head,final,"iddfs", (left[0] + left[1])*2)
        elif mode == "astar":
            ret = astar(head,final)
        else:
            raise Exception("Invalid mode provided. Please provide a valid mode member of [bfs,dfs,iddfs,astar]")

        # print_tree(ret[0])

        out = open(outputfile, "w")  # write mode
        out.write(ret[1])

        # head = expandTree(head,goal[1])

        u.close() # closing input file
        v.close() # closing goal file
        out.close() # closing output file
    else:
        print("Please provide an input file in the format of python main.py inputfile.txt goalfile.txt searchmode outputfile.txt")

def triple(head,goal,kind,limit):
    """Implements bfs/dfs with a first in first out queue"""
    fifo = [head] # initialize the frontier using the initial state of the problem
    explored = [] # initialize the explored set to be empty
    solution = ""
    goalReached = False

    while len(fifo) > 0: # if frontier is empty and we, terminate the loop and return failure
        if kind == "bfs":
            newleaf = fifo.pop(0)
        elif kind == "dfs" or kind == 'iddfs':
            newleaf = fifo.pop()
        else:
            print("Please provide a correct type, 'dfs' or 'bfs'")
        
        # choose leaf node and remove it from the frontier
        if newleaf.rightside == goal: # if the node contains a goal state then return the corresponding solution
            goalReached = True
            print("Goal reached, " + str(newleaf) + "\n")
            print("GOAL DEPTH: " + str(newleaf.depth))
            while newleaf != None:
                solution = str(newleaf) + "\n" + solution
                newleaf = newleaf.parent
            break
        
        if kind == 'iddfs' and newleaf.depth > limit: # If we've gone past the limit, then stop expanding nodes to the frontier
            pass
        else:
            newleaf.expandChildren(explored) # expand the chosen node, adding the resulting nodes to the frontier

        fifo.extend(newleaf.children)
        explored.extend(newleaf.children) # add the nodes to the explored set
        
    if goalReached:
        # print("Found solution: \n" + solution)
        pass
    else:
        print("Failed to find a solution.")

    print(str(len(explored)) + " nodes expanded")

    return (head,solution)

def iddfs(head,goal):
    pass
      
# Driver's code

def astar(head,goal):
    """Implements astar search with a first priority queue"""

    # Implement as a priority queue
    priority = [(0,head)] # initialize the frontier using the initial state of the problem
    explored = [] # initialize the explored set to be empty
    solution = ""
    goalReached = False

    while len(priority) > 0: # if frontier is empty and we, terminate the loop and return failure
        priority.sort(key=lambda x:x[0],reverse=True)
        newleaf = priority.pop(0)
        leaf = newleaf[1]

        # choose leaf node and remove it from the frontier
        if leaf.rightside == goal: # if the node contains a goal state then return the corresponding solution
            goalReached = True
            print("Goal reached, " + str(leaf) + "\n")
            print("GOAL DEPTH: " + str(leaf.depth))
            while leaf != None:
                solution = str(leaf) + "\n" + solution
                leaf = leaf.parent
            break
        
        leaf.expandChildren(explored) # expand the chosen node, adding the resulting nodes to the frontier

        for i in leaf.children:
            gofn = i.depth
            # hofn = ((goal[0] - i.rightside[0]) + (goal[1] - i.rightside[1]) + i.rightside[2]) * 1.7 # old heuristic
            hofn = ((goal[0] + goal[1]) * 2) - i.depth
            hofn = hofn - (hofn * .02)

            score = gofn + hofn

            priority.append((score,i))

        explored.extend(leaf.children) # add the nodes to the explored set
        
    if goalReached:
        # print("Found solution: \n" + solution)
        pass
    else:
        print("Failed to find a solution.")

    print(str(len(explored)) + " nodes expanded")

    return (head,solution)

def nestedStringtoInt(arr):
    """Turns a nested array of strings into a nested array of integers"""
    for i in range(len(arr)):
        if len(arr[i]) == 0:
            del arr[i]
        else:
            arr[i] = arr[i].split(",")

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] = int(arr[i][j])
    
    return arr

def expandTree(head,goal):
    """Expands the entire tree of possible states iteratively"""

    # List of duplicate nodes not to be replicated
    duplicates = [head]

    # Grandchildren is a list of nodes to be expanded.
    grandchildren = [head]
    finished = False

    while len(grandchildren) > 0 and finished == False:
        newborn = []
        for j in grandchildren:
            if j.rightside == goal:
                finished = True
                break
            j.expandChildren(duplicates)
            newborn.extend(j.children)
            duplicates.extend(j.children)
        grandchildren = newborn
    return head

class River:
    '''Represents a state of the chicken and wolves problem. Also functions as a Node in a tree data structure'''

    def __init__(self,leftside,rightside,parent,depth):
        """Takes leftside and rightside states, 
        containing a list of values representing the state of the game.
        the list is ordered by [chicken, wolves, boat]. For example,
        [3,3,1] would mean that 3 chickens and 3 wolves were on that side of the river
        and the boat as well. [2,3,0] means 2 chickens, 3 wolves, and no boat is on that side of the river"""

        self.leftside = leftside
        self.rightside = rightside

        # Number of steps away from the head node
        self.depth = depth

        self.parent = parent
        self.children = []

    def __eq__(self, object):
        """Overrides equality, returning true if the two river objects are equal."""
        if type(object) == River:
            return (object.leftside == self.leftside) and (object.rightside == self.rightside)
        else:
            return False

    # TODO: Use Inflect library to print off plural/nonplural variables
    def __str__(self):
        """Overrides str, returning a relevant string representation of the River object"""
        return f'Left Bank: {self.leftside[0]} chicken, {self.leftside[1]} wolf, {self.leftside[2]} boat. Right Bank: {self.rightside[0]} chicken, {self.rightside[1]} wolf, {self.rightside[2]} boat'

    def compactedString(self):
        """Like overriding __str__, but with a compacted form for printing off the tree"""
        return f'{self.leftside} {self.rightside}'

    def __hash__(self):
        """Overides hash function for pretty printing purposes"""
        return hash(tuple(self.leftside))

    def __iter__(self):
        """Overrides iterable function for pretty printing purposes"""
        return iter([self.leftside,self.rightside])

    def checkValid(self, leftside=None,rightside=None):
        """Checks to make sure that a state is valid. If there are more wolves than chickens, then it is not valid."""
        if ((leftside == None) and (rightside == None)): # Assigns internal variables if none are provided in the parameter list
            leftside = self.leftside
            rightside = self.rightside
        else:
            pass

        for i in leftside:
            for j in rightside:
                if i<0 or j<0:
                    return False
        

        if ( (leftside[0] < leftside[1] and leftside[0] > 0) or (rightside[0] < rightside[1] and rightside[0] > 0)):
            return False
        else:
            return True

    def moveAnimals(self,animals):
        """Takes an array with two components, number of chickens and number of wolves to move to the other side.
        Automatically determines which side the boat is on and if the move is valid.
        Returns a River with the corrsponding changes. Animals is a list with [chickens, wolves]"""

        newLeft = [None, None, None]
        newRight = [None, None, None]

        if(self.leftside[2] == 1): # If the boat is on the left side of the river, subtract animals from the left side and move to right
            newLeft[0] = self.leftside[0] - animals[0]
            newLeft[1] = self.leftside[1] - animals[1]
            newRight[0] = self.rightside[0] + animals[0]
            newRight[1] = self.rightside[1] + animals[1]

            newRight[2] = 1
            newLeft[2] = 0
        elif(self.rightside[2] == 1): # If the boat is on the right side of the river, subtract animals from the right side and move to left
            newLeft[0] = self.leftside[0] + animals[0]
            newLeft[1] = self.leftside[1] + animals[1]
            newRight[0] = self.rightside[0] - animals[0]
            newRight[1] = self.rightside[1] - animals[1]

            newRight[2] = 0
            newLeft[2] = 1

        if self.checkValid(newLeft,newRight) == True:
            return River(newLeft, newRight, self, self.depth + 1)
        else:
            return False

    def expandChildren(self,duplicates):
        """Expands all valid iterations from the current state, disreguarding duplicates"""
        
        iterations = []

        # Put one chicken in the boat
        iterations.append(self.moveAnimals([1,0]))
        # Put two chickens in the boat
        iterations.append(self.moveAnimals([2,0]))
        # Put one wolf in the boat
        iterations.append(self.moveAnimals([0,1]))
        # Put one wolf and one chicken in the boat
        iterations.append(self.moveAnimals([1,1]))
        # Put two wolves in the boat
        iterations.append(self.moveAnimals([0,2]))

        filtered = []

        for i in iterations:
            duplicate = False
            for j in duplicates:
                if i == j:
                    duplicate = True
            if (i != False) and (duplicate != True):
                filtered.append(i)

        self.children = filtered

"""NOT MY CODE."""
"""CODE ADAPTED FROM https://github.com/clemtoy/pptree/blob/master/pptree/pptree.py"""

def print_tree(current_node, childattr='children', nameattr='name'):
    if hasattr(current_node, nameattr):
        name = lambda node: getattr(node, nameattr)
    else:
        name = lambda node: node.compactedString()

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

main()