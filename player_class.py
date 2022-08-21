import pygame
import math
from settings import *
import os, psutil
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.coordinate=[]
        self.coordinate1=[]
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1
        self.target = None
        self.shortest = []
        self.state = None
        self.index = 0
        self.next = pos
        self.nodes = 0

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.app.screen, YELLOW, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.app.cell_width//2-2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20*x, HEIGHT - 15), 7)

        # Drawing the grid pos rect
        #pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins = []
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction
        if self.grid_pos in self.app.coins :
            self.eat_coin()

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)


    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True  
        

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        direction = vec(xdir, ydir)
        
        return direction

    def find_next_cell_in_path(self, target):
        if self.grid_pos == target :
            return target
        if self.grid_pos == self.next :
            # self.index += 1
            next_cell = self.shortest[self.index + 1]
            for i in self.app.enemies :
                if (i.grid_pos -self.grid_pos).length() <= 2 :
                    e_direction = i.get_direction()
                    if self.shortest[self.index + 1] == i.grid_pos + e_direction or self.shortest[self.index + 1] == i.grid_pos :
                        if self.grid_pos[1] == i.grid_pos[1] :
                            self.index -= 1
                            next_cell =self.shortest[self.index]
                        elif self.grid_pos[1] != i.grid_pos[1]:
                            self.index -= 1
                            next_cell = self.grid_pos
                            break
                        else:
                            next_cell = self.shortest[self.index +1 ]
                            break
            if next_cell == self.shortest[self.index + 1] :
                self.index += 1
            self.next = next_cell
            return next_cell
        else :
            
            return self.shortest[self.index]
    
############################### BREARTH FIRST SEARCH #################################
    
    def BFS(self, start, target):
        for next_cell in self.coordinate1:
                pygame.draw.rect(self.app.background, BLACK, (next_cell[0]*self.cell_width, next_cell[1]*self.cell_height,
                                                                  self.cell_width, self.cell_height)) 
        grid = [[' ' for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = '0'
                      
        queue = [start]
        path = []
        visited = [start]
        
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            if current == target:
                break #den đây là giống nhau
            else:
                neighbours = [[1, 0], [0, 1], [-1, 0],[0, -1]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid): #neu (x,y) như the nao do
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] == ' ' :
                                    self.coordinate.append([next_cell[0],next_cell[1]])
                                    visited.append(next_cell)
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
                                    self.nodes += 1
                                    #print(next_cell)
         #den đây là giống                           
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        self.state = "astar"
        for next_cell in self.coordinate:
                pygame.draw.rect(self.app.background, GREY, (next_cell[0]*self.cell_width, next_cell[1]*self.cell_height,
                                                                  self.cell_width, self.cell_height))                                                            
                                                                
        return shortest



############################### ASTAR SEARCH ###########################################
    def ASTAR(self, start, target):
        for next_cell in self.coordinate:
                pygame.draw.rect(self.app.background, BLACK, (next_cell[0]*self.cell_width, next_cell[1]*self.cell_height,
                                                                  self.cell_width, self.cell_height))   
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1

        queue = [start]
        path = []
        queue1=[start]
        visited = [start]
        
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            
            if current == target:
                break
            else:
                neighbours_check = [[1, 0], [0, 1], [-1, 0],[0, -1]]
                #neighbours = []
                i=0
                for i in range(len(neighbours_check)):
                    if neighbours_check[i][0]+current[0] >= 0 and neighbours_check[i][0] + current[0] < len(grid[0]):
                        if neighbours_check[i][1]+current[1] >= 0 and neighbours_check[i][1] + current[1] < len(grid):
                            next_cell_check = [neighbours_check[i][0] + current[0], neighbours_check[i][1] + current[1]]
                            if next_cell_check not in visited:
                                if grid[next_cell_check[1]][next_cell_check[0]] != 1:
                                    if math.sqrt(abs(next_cell_check[0]-target[0])**2 + abs(next_cell_check[1]-target[1])**2) <= math.sqrt(abs(current[0]-target[0])**2 + abs(current[1]-target[1])**2):
                                        #neighbours.append( neighbours_check[i])
                                        visited.append(next_cell_check)
                                        
                                        self.coordinate1.append([next_cell_check[0],next_cell_check[1]])
                                        queue.append(next_cell_check)
                                        path.append({"Current": current, "Next": next_cell_check})
                                        self.nodes += 1
                                    if math.sqrt(abs(next_cell_check[0]-target[0])**2 + abs(next_cell_check[1]-target[1])**2) > math.sqrt(abs(current[0]-target[0])**2 + abs(current[1]-target[1])**2):
                                        if len(queue)==0:
                                            
                                            visited.append(next_cell_check)
                                            self.coordinate1.append([next_cell_check[0],next_cell_check[1]])
                                            queue.append(next_cell_check)
                                            path.append({"Current": current, "Next": next_cell_check})
                                            self.nodes += 1
                                            
                                        else:
                                            path.append({"Current": current, "Next": next_cell_check})  
                                            queue1.insert(0,next_cell_check)
                                if grid[next_cell_check[1]][next_cell_check[0]] != 1:
                                    i+=1   
                            if next_cell_check in visited:
                                i+=1                 
                if (i==3 and (len(queue)==0)):
                    queue.append(queue1[0])
                    path.append({"Current": current, "Next": queue1[0]})
                    queue1.remove(queue1[0])
                    self.nodes += 1

        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        self.state = "bfs"
        for next_cell in self.coordinate1:
                pygame.draw.rect(self.app.background, GREY, (next_cell[0]*self.cell_width, next_cell[1]*self.cell_height,
                                                                  self.cell_width, self.cell_height))   
        return shortest
    '''def depthFirstSearch(self, start, target ):
        grid = [[' ' for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = '0'
                      
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours_dfss = [[1, 0], [0, 1], [-1, 0],[0, -1]]
                for neighbours in neighbours_dfss:






        # create a Stack to keep track of nodes we are going to explore
        #myStack = util.Stack()

        #done = set()  #to keep track or explored nodes

        #startPoint = problem.startingState()

        #we will push in tuples (coordinates, pass) in the stack
        #myStack.push((startPoint, []))'''

