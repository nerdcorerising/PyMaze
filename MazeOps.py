'''
Created on Dec 5, 2010

@author: Dave
'''

def FindUnused(dfs, size):
    for i in range(size):
        for j in range(size):
            if(dfs[i][j] == 0):
                return (i,j)
    return (-1,-1)

def AppendNeighborsRight(size, stack, dfs, pos):
    x, y = pos
    if((x + 1) <  size // 2 and dfs[x + 1][y] == 0):
        stack.append((x + 1, y, x, y))
        dfs[x + 1][y] = 1
    if((x - 1) >= 0 and dfs[x - 1][y] == 0):
        stack.append((x - 1, y, x, y))
        dfs[x - 1][y] = 1
    if((y + 1) <  size // 2 and dfs[x][y + 1] == 0):
        stack.append((x, y + 1, x, y))
        dfs[x][y + 1] = 1
    if((y - 1) >= 0 and dfs[x][y - 1] == 0):
        stack.append((x, y - 1, x, y))
        dfs[x][y - 1] = 1

def AppendNeighborsLeft(size, stack, dfs, pos):
    x, y = pos
    if((x - 1) >= 0 and dfs[x - 1][y] == 0):
        stack.append((x - 1, y, x, y))
        dfs[x - 1][y] = 1
    if((y + 1) <  size // 2 and dfs[x][y + 1] == 0):
        stack.append((x, y + 1, x, y))
        dfs[x][y + 1] = 1
    if((y - 1) >= 0 and dfs[x][y - 1] == 0):
        stack.append((x, y - 1, x, y))
        dfs[x][y - 1] = 1
    if((x + 1) <  size // 2 and dfs[x + 1][y] == 0):
        stack.append((x + 1, y, x, y))
        dfs[x + 1][y] = 1

def AppendNeighborsDown(size, stack, dfs, pos):
    x, y = pos
    if((y + 1) <  size // 2 and dfs[x][y + 1] == 0):
        stack.append((x, y + 1, x, y))
        dfs[x][y + 1] = 1
    if((y - 1) >= 0 and dfs[x][y - 1] == 0):
        stack.append((x, y - 1, x, y))
        dfs[x][y - 1] = 1
    if((x + 1) <  size // 2 and dfs[x + 1][y] == 0):
        stack.append((x + 1, y, x, y))
        dfs[x + 1][y] = 1
    if((x - 1) >= 0 and dfs[x - 1][y] == 0):
        stack.append((x - 1, y, x, y))
        dfs[x - 1][y] = 1
        
def AppendNeighborsUp(size, stack, dfs, pos):
    x, y = pos
    if((y - 1) >= 0 and dfs[x][y - 1] == 0):
        stack.append((x, y - 1, x, y))
        dfs[x][y - 1] = 1
    if((x + 1) <  size // 2 and dfs[x + 1][y] == 0):
        stack.append((x + 1, y, x, y))
        dfs[x + 1][y] = 1
    if((x - 1) >= 0 and dfs[x - 1][y] == 0):
        stack.append((x - 1, y, x, y))
        dfs[x - 1][y] = 1
    if((y + 1) < size // 2 and dfs[x][y + 1] == 0):
        stack.append((x, y + 1, x, y))
        dfs[x][y + 1] = 1
               
def reward(maze, xpos, ypos):
    if(maze[xpos][ypos] == 3):
        return 1
    elif(maze[xpos][ypos] == 2):
        return -1
    else:
        return -0.1
    

def Decision(xpos, ypos, gamma, oldtype, memory, maze):
    """Makes a decision based on the current state of 
    the maze and the memory."""
    #TODO fill in
    positions = []
    
    if(xpos + 1 < len(maze) and maze[xpos + 1][ypos] != 1):
        positions.append((xpos + 1, ypos))
    if(xpos - 1 >= 0 and maze[xpos - 1][ypos] != 1):
        positions.append((xpos - 1, ypos))
    if(ypos + 1 < len(maze[xpos]) and maze[xpos][ypos + 1] != 1):
        positions.append((xpos, ypos + 1))
    if(0 <= ypos - 1 and maze[xpos][ypos - 1] != 1):
        positions.append((xpos, ypos - 1))
        
    xmax, ymax = (xpos, ypos)
    utilmax = -10000
    
    for (x,y) in positions:
        if(memory[x][y] > utilmax):
            utilmax = memory[x][y]
            xmax, ymax = (x,y)
            
    memory[xpos][ypos] = reward(maze, xpos, ypos) + gamma * (utilmax)
    maze[xpos][ypos] = oldtype
    oldtype = maze[xmax][ymax]
    maze[xmax][ymax] = 4
    
    del positions
    
    return xmax, ymax, oldtype