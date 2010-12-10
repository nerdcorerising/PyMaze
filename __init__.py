import os, sys
import pygame
import random
from MazeOps import *
from pygame.locals import *

#TODO finish DFS algorithm to create the maze. Right not it just creates a grid
#TODO right now, there is a bug where once it runs out of options on it's current path, it doesn't delete walls properly when it goes back to a previous spot and starts down a different path

class PyMazeMain:
    """PyMaze main class, this handles things like setup
    and the main game loop."""
    
    def __init__(self, size=30, width=800, height=600):
        """Initialize the game"""
        
        """Initialize pygame"""
        pygame.init()
        
        """Set the window size"""
        self.width = width
        self.height = height
        
        self.oldtype = 0
        
        self.size = size;
        
        #Set block width to the width of each cell
        self.blockwidth = self.width // self.size
        #Set block height to the height of each cell
        self.blockheight = self.height // self.size
        
        self.Reinit()
        
        """Create the screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def Reinit(self, gamma=1):
        self.xpos = 0
        self.ypos = 0
        self. mazedrawn = 0
        self.gamma = gamma
        
        """Set the initial speed to the lowest."""
        self.speed = 1
        
        self.maze = []
        self.memory = []
        for i in range(self.size):
            self.maze.append([])
            self.memory.append([])
            for j in range(self.size):
                self.memory[i].append(0)
                if(i % 2 == 1 or j % 2 == 1):
                    self.maze[i].append(1)
                else:
                    self.maze[i].append(0);
        self.DFSMaze()

    def DFSMaze(self):
        """ Creates a Maze using the depth first search algorithm.
        I'm not sure how much I like the results right now."""
        dfs = []
        for i in range(self.size // 2):
            dfs.append([])
            for j in range(self.size // 2):
                dfs[i].append(0)
        
        stack = []
        
        #The walls take up a slot, so we only have half the slots open for paths
        i = random.randrange(self.size // 2)
        j = random.randrange(self.size // 2)
        #This random position is the start position of the robot
        self.startx = i
        self.starty = j
        #Set the position to visited
        dfs[i][j] = 1
        #Push the position onto the stack
        r = random.randrange(4)
        if(r == 0):
            AppendNeighborsLeft(self.size, stack, dfs, (i, j))
        elif(r == 1):
            AppendNeighborsRight(self.size, stack, dfs, (i, j))
        elif(r == 2):
            AppendNeighborsUp(self.size, stack, dfs, (i, j))
        else:
            AppendNeighborsDown(self.size, stack, dfs, (i, j))
        
        while(len(stack) > 0):
                
            r = random.randrange(4)
            if(r == 0):
                AppendNeighborsLeft(self.size, stack, dfs, (i, j))
            elif(r == 1):
                AppendNeighborsRight(self.size, stack, dfs, (i, j))
            elif(r == 2):
                AppendNeighborsUp(self.size, stack, dfs, (i, j))
            else:
                AppendNeighborsDown(self.size, stack, dfs, (i, j))
            
            newi, newj, i, j = stack.pop()
            
            if(newi > i):
                self.maze[i * 2 + 1][j * 2] = 0
            elif(newi < i):
                self.maze[i * 2 - 1][j * 2] = 0
            elif(newj > j):            
                self.maze[i * 2][j * 2 + 1] = 0
            elif(newj < j):
                self.maze[i * 2][j * 2 - 1] = 0
            
            i, j = newi, newj

        #Add the robot
        #i = random.randrange(self.size // 2)
        #j = random.randrange(self.size // 2)
        #self.maze[i * 2][j * 2] = 4
        
        self.xpos = i * 2
        self.xpos = j * 2
        
        del(dfs)
        del(stack)
        
    
    def DrawMaze(self):
        #TODO fill this in, decide on parameters
        
        """Do the Drawing"""               
        self.screen.blit(self.background, (0, 0))
        
        #self.spritegroup.draw(self.screen)
        
        for l in range(0, self.size):
            for m in range(0, self.size):
                if(self.maze[l][m] != 0):
                    r = Rect(l * self.blockwidth, m * self.blockheight, self.blockwidth, self.blockheight)
                    if(self.maze[l][m] == 1):
                        color = (0, 0, 0)
                    elif(self.maze[l][m] == 2):
                        color = (255, 0, 0)
                    elif(self.maze[l][m] == 3):
                        color = (0, 255, 0)
                    elif(self.maze[l][m] == 4):
                        color = (0,0,255)
                    
                    self.screen.fill(color, r)
                
        
        pygame.display.update()
        
    
    def AddWall(self, x, y):
        xpos = x // self.blockwidth
        ypos = y // self.blockheight
        self.maze[xpos][ypos] = 1

    def AddTrap(self, x, y):
        xpos = x // self.blockwidth
        ypos = y // self.blockheight
        self.maze[xpos][ypos] = 2
    
    def AddGoal(self, x, y):
        xpos = x // self.blockwidth
        ypos = y // self.blockheight
        self.maze[xpos][ypos] = 3
    
    def ChangeWall(self, x, y):
        xpos = x // self.blockwidth
        ypos = y // self.blockheight
        val = self.maze[xpos][ypos]
        if(val == 0):
            self.maze[xpos][ypos] = 1
        elif(val == 1):
            self.maze[xpos][ypos] = 0
            
    def ClearLoc(self, x, y):
        xpos = x // self.blockwidth
        ypos = y // self.blockheight
        self.maze[xpos][ypos] = 0
        
    def Restart(self):
        self.maze[self.xpos][self.ypos] = self.oldtype
        
        self.xpos = random.randrange(self.size)
        self.ypos = random.randrange(self.size)
        
        while (self.maze[self.xpos][self.ypos] == 1 or self.maze[self.xpos][self.ypos] == 2
                or self.maze[self.xpos][self.ypos] == 3 ):
            self.xpos = random.randrange(self.size)
            self.ypos = random.randrange(self.size)
        
        self.maze[self.xpos][self.ypos] = 4
        
    def Resize(self, x):
        if(self.size + x > 0):
            self.size = self.size + x
        self.blockwidth = self.width // self.size
        self.blockheight = self.height // self.size
        
    def MainLoop(self):
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 250, 250))
        
        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(500, 30)
        
        
        """Main loop of the game."""
        while 1:
            self.DrawMaze()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if(event.key == K_1):
                        self.speed = 4
                    elif(event.key == K_2):
                        self.speed = 3
                    elif(event.key == K_3):
                        self.speed = 2
                    elif(event.key == K_4):
                        self.speed = 1
                    elif(event.key == K_5):
                        self.speed = 0
                    elif(event.key == K_t):
                        x, y = pygame.mouse.get_pos()
                        self.AddTrap(x, y)
                    elif(event.key == K_g):
                        x, y = pygame.mouse.get_pos()
                        self.AddGoal(x, y)
                    elif(event.key == K_s):
                        if(self.mazedrawn == 0):
                            self.mazedrawn = 1
                        else:
                            self.mazedrawn = 0
                    #elif(event.key == K_d):
                    #    self.DFSMaze()
                    elif(event.key == K_n):
                        self.mazedrawn = 0
                        self.Reinit()
                    elif(event.key == K_EQUALS):
                        self.Resize(10)
                        self.Reinit()
                    elif(event.key == K_MINUS):
                        self.Resize(-10)
                        self.Reinit()
                elif event.type == MOUSEBUTTONDOWN:
                    if(event.button == 1):
                        x,y = pygame.mouse.get_pos()
                        self.ChangeWall(x,y)
                    elif(event.button == 3):
                        x,y = pygame.mouse.get_pos()
                        self.ClearLoc(x, y)
            if(self.mazedrawn):
                oldx, oldy = self.xpos, self.ypos
                self.xpos, self.ypos, self.oldtype = Decision(self.xpos, self.ypos, self.gamma, self.oldtype, self.memory, self.maze)
                if(self.maze[oldx][oldy] == 2 or self.maze[oldx][oldy] == 3):
                    self.memory[oldx][oldy] = reward(self.maze, oldx, oldy)
                    self.Restart()
                    
            pygame.time.wait(self.speed * 20)


    
if __name__ == "__main__":
    MainWindow = PyMazeMain(20, width=800, height=600)
    MainWindow.MainLoop()
