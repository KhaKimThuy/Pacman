maze = []
with open("maze.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '')
        maze.append(line)

pacman = None
goal = []

for i in range(len(maze)):
    for j in range(len(maze[i])):
        o = 0+i
        if maze[i][j]=="P":
            pacman = (i ,j)
        elif maze[i][j]==".":
            goal.append((i, j))
print(pacman)
print(goal)



