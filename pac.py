from functools import cmp_to_key
import numpy as np
import math
from operator import itemgetter
from queue import PriorityQueue
def update(line_maze, col, p):
    st = list(line_maze)
    st[col] = p
    return ''.join(st)
import os
def game(actions, maz, pacmanPos):
    os.system('cls')
    for m in maz:
        print(m)
    input()
    for i in actions:
        os.system('cls')
        maz[pacmanPos[0]] = update(maz[pacmanPos[0]], pacmanPos[1], ' ')
        if i == 'N':
            maz[pacmanPos[0]-1] = update(maz[pacmanPos[0]-1], pacmanPos[1], 'P')
            pacmanPos = (pacmanPos[0]-1, pacmanPos[1])
        elif i == 'S':
            maz[pacmanPos[0]+1] = update(maz[pacmanPos[0]+1], pacmanPos[1], 'P')
            pacmanPos = (pacmanPos[0]+1, pacmanPos[1])
        elif i == 'E':
            maz[pacmanPos[0]] = update(maz[pacmanPos[0]], pacmanPos[1]+1, 'P')
            pacmanPos = (pacmanPos[0], pacmanPos[1]+1)
        elif i == 'W':
            maz[pacmanPos[0]] = update(maz[pacmanPos[0]], pacmanPos[1]-1, 'P')
            pacmanPos = (pacmanPos[0], pacmanPos[1]-1)
        for j in maz:
            print(j)
        input()
    
def order_goals(goals, pacman_loc):
    o = []
    for goal in goals:
        dist = math.dist(goal, pacman_loc)
        o.append((goal, dist))
    o = sorted(o, key=itemgetter(1))
    o = np.array(o)[:,0]
    return o



def dfs(pacmanPos, goals, grid)  -> list:
    goal_position = order_goals(goals, pacmanPos)
    paths = []
    for goal_pos in goal_position:
        print(goal_pos)
        goal_pos = goal_pos[0]
        frontier = [pacmanPos]
        explored = set()
        parent = {pacmanPos: None}
        flag = False
        while frontier:
            pacmanPos = frontier.pop()
            explored.add(pacmanPos)
            if pacmanPos==goal_pos:
                path = []
                while pacmanPos is not None:
                    path.append(pacmanPos)
                    pacmanPos = parent[pacmanPos]
                path.reverse()
                paths.extend(direction(path))
                flag = True
                pacmanPos = path[-1]
                grid[pacmanPos[0]] = update(grid[pacmanPos[0]], pacmanPos[1], " ")
                break
            successors = successor_func(grid, pacmanPos, goal_pos)
            for successor in successors:
                if successor not in explored:
                    parent[successor] = pacmanPos 
                    frontier.append(successor)
        if flag==False:
            paths.append(None)
    return paths

def successor_func(maze, pac_pos, goal_pos):
    def sortbyCond_ar_dc(a, b):
        if (a[0] != b[0]):
            return (a[0] - b[0])
        else:
            return b[1] - a[1]
    def sortbyCond_dr_ac(a, b):
        if (a[0] != b[0]):
            return b[0] - a[0]
        else:
            return b[1] - a[1]
    row = pac_pos[0]
    column = pac_pos[1]
    numRows = len(maze)
    numCols = len(maze[0])
    successors = []
    for newPos in [(row, column + 1), (row + 1, column), (row, column - 1), (row - 1, column)]:
        if newPos[0] < numRows and newPos[1] < numCols and maze[newPos[0]][newPos[1]] != '%':
            successors.append(newPos)
    if goal_pos[0] >= row and goal_pos[1] <= column:
        successors.sort(key = cmp_to_key(sortbyCond_ar_dc))
    elif goal_pos[0] >= row and goal_pos[1] >= column:
        successors.sort(key = cmp_to_key(sortbyCond_dr_ac), reverse=True)
    elif goal_pos[0] <= row and goal_pos[1] <= column:
        successors.sort(key = cmp_to_key(sortbyCond_dr_ac))
    else:
        successors.sort(key = cmp_to_key(sortbyCond_ar_dc), reverse=True)
    
    print("goal: ", goal_pos)
    print("suc: ", successors)
    input()
    return successors
# def order_ucs(frontiers, goal_pos):
#     def sortbyCond_ar_dc(a, b):
#         if (a[0] != b[0]):
#             return (a[0] - b[0])
#         else:
#             return b[1] - a[1]
#     def sortbyCond_dr_ac(a, b):
#         if (a[0] != b[0]):
#             return b[0] - a[0]
#         else:
#             return b[1] - a[1]
#     row = pac_pos[0]
#     column = pac_pos[1]
#     if goal_pos[0] >= row and goal_pos[1] <= column:
#         frontiers.sort(key = cmp_to_key(sortbyCond_ar_dc))
#     elif goal_pos[0] >= row and goal_pos[1] >= column:
#         frontiers.sort(key = cmp_to_key(sortbyCond_dr_ac), reverse=True)
#     elif goal_pos[0] <= row and goal_pos[1] <= column:
#         frontiers.sort(key = cmp_to_key(sortbyCond_dr_ac))
#     else:
#         frontiers.sort(key = cmp_to_key(sortbyCond_ar_dc), reverse=True)
#     return frontiers


def direction(path):
    direction = []
    for i in range(len(path)-1):
        check = list(np.array(path[i]) - np.array(path[i+1]))
        if check[0] == 0 and check[1] > 0:
            direction.append('W')
        elif check[0] == 0 and check[1] < 0:
            direction.append('E')
        elif check[0] > 0 and check[1] == 0:
            direction.append('N')
        else:
            direction.append('S')
    direction.append('Stop')
    return direction




def update(line_maze, col, p):
    st = list(line_maze)
    st[col] = p
    return ''.join(st)


def bfs(pacmanPos, goals, grid) -> list:
    goal_position = order_goals(goals, pacmanPos)
    paths = []
    for goal_pos in goal_position:
        frontier = [pacmanPos]
        explored = set()
        parent = {pacmanPos: None}
        flag = False
        while frontier:
            pacmanPos = frontier.pop()
            explored.add(pacmanPos)
            if pacmanPos==goal_pos:
                path = []
                while pacmanPos is not None:
                    path.append(pacmanPos)
                    pacmanPos = parent[pacmanPos]
                path.reverse()
                paths.extend(direction(path))
                flag = True
                pacmanPos = path[-1]
                # grid[pacmanPos[0]] = update(grid[pacmanPos[0]], pacmanPos[1], " ")
                break
            successors = successor_func(grid, pacmanPos, goal_pos)
            unvisited_succ = []
            for successor in successors:
                if successor not in explored:
                    parent[successor] = pacmanPos 
                    unvisited_succ.append(successor)
            frontier = unvisited_succ + frontier
        if flag==False:
            paths.append(None)
    print(paths)
    input()
    return paths

def get_loc(maze):
    pacman = None
    goal = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]=="P":
                pacman = (i ,j)
            elif maze[i][j]==".":
                goal.append((i, j))
    return pacman, goal



def ucs(pacmanPos, goals, grid):
    goal_position = order_goals(goals, pacmanPos)
    paths = []
    for goal_pos in goal_position:
        frontier = PriorityQueue()
        frontier.put((0, pacmanPos, []))
        explored = set()
        flag = False
        while not frontier.empty():
            cost, pacmanPos, path = frontier.get()
            if pacmanPos == goal_pos:
                paths.extend(direction(path + [pacmanPos]))
                pacmanPos = goal_pos
                flag = True
                break
            explored.add(pacmanPos)
            successors = successor_func(grid, pacmanPos, goal_pos)
            for neighbor in successors:
                if neighbor not in explored:
                    updated_cost = cost + 1
                    frontier.put((updated_cost, neighbor, path + [pacmanPos]))
        if not flag:
            paths.extend(None)
    return paths












    

if __name__ == "__main__":        
    maze = []
    with open('maze.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            maze.append(line)
    maz = maze.copy()
    pacman, goal = get_loc(maze)
    # print(ucs(pacman, goal, maze))
    print(game(ucs(pacman, goal, maze), maz, pacman))

# maz = maze.copy()
# pacmanPos = (3, 11)
# goal_position = [(8,1)]
# # actions = direction(bfs(pacmanPos, goal_position, maze))
# print(bfs(pacmanPos, goal_position, maze))
# exit(1)



     

