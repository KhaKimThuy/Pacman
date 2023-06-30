from functools import cmp_to_key
import os


class SingleFoodSearchProblem:
    def __init__(self, maze_file):
        self.state = self.read_maze(maze_file)
        self.init_state, self.goal_state = self.ini()
        self.node = self.init_state
        self.solution = []

    def successor_func(self, curr_node):

        def sortbyCond_ar_dc(a, b): # ascending row - descending column
            if (a[0] != b[0]):
                return (a[0] - b[0])
            else:
                return b[1] - a[1] # Trường hợp cùng hàng thì so sánh cột
            
        def sortbyCond_dr_ac(a, b): # descending row - ascending column
            if (a[0] != b[0]):
                return b[0] - a[0]
            else:
                return b[1] - a[1] # Trường hợp cùng hàng thì so sánh cột
            
        # node = [hànd, cột]
        row = curr_node[0]
        column = curr_node[1]

        # Số hàng của map
        numRows = len(self.state)

        # Số cột của map
        numCols = len(self.state[0])

        successors = []

        # Xét 4 hướng vị
        for newPos in [(row, column + 1), (row + 1, column), (row, column - 1), (row - 1, column)]:
            
            # Kiểm tra vị trí hợp lệ của pacman
            if newPos[0] < numRows and newPos[1] < numCols and self.state[newPos[0]][newPos[1]] != '%':
                successors.append(newPos)

        # Theo ý tưởng của hàm
        # self.goal_state
        if self.goal_state[0][0] >= row and self.goal_state[0][1] <= column:
            successors.sort(key = cmp_to_key(sortbyCond_ar_dc))
        elif self.goal_state[0][0] >= row and self.goal_state[0][1] >= column:
            successors.sort(key = cmp_to_key(sortbyCond_dr_ac), reverse=True)
        elif self.goal_state[0][0] <= row and self.goal_state[0][1] <= column:
            successors.sort(key = cmp_to_key(sortbyCond_dr_ac))
        else:
            successors.sort(key = cmp_to_key(sortbyCond_ar_dc), reverse=True)

        return successors

        
    
    def goal_test_func(self, food):
        return food == self.goal_state
    
    def path_cost_func(self):
        return len(self.solution) - 1
    
    def read_maze(self, maze_file):
        maze = []
        with open(maze_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                maze.append(line)
        return maze
    
    def ini(self):
        pacman = None
        goal = []
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j]=="P":
                    pacman = (i ,j)
                elif self.state[i][j]==".":
                    goal.append((i, j))
        if not pacman or not goal:
            print("Invalid environment.")
            exit()
        return pacman, goal
    
    def out_maze(self):
        for line in self.state:
            print(line)
    
    def animate(self) -> None:
        if self.solution[0]!='Stop':
            def update(line_maze, col, p):
                st = list(line_maze)
                st[col] = p
                return ''.join(st)
            os.system('cls')
            self.out_maze()
            input()
            for i in self.solution:
                os.system('cls')
                if i == 'Stop':
                    self.out_maze()
                    print("Congratulations!")
                    break
                self.state[self.init_state[0]] = update(self.state[self.init_state[0]], self.init_state[1], ' ')
                if i == 'N':
                    self.state[self.init_state[0]-1] = update(self.state[self.init_state[0]-1], self.init_state[1], 'P')
                    self.init_state = (self.init_state[0]-1, self.init_state[1])
                elif i == 'S':
                    self.state[self.init_state[0]+1] = update(self.state[self.init_state[0]+1], self.init_state[1], 'P')
                    self.init_state = (self.init_state[0]+1, self.init_state[1])
                elif i == 'E':
                    self.state[self.init_state[0]] = update(self.state[self.init_state[0]], self.init_state[1]+1, 'P')
                    self.init_state = (self.init_state[0], self.init_state[1]+1)
                elif i == 'W':
                    self.state[self.init_state[0]] = update(self.state[self.init_state[0]], self.init_state[1]-1, 'P')
                    self.init_state = (self.init_state[0], self.init_state[1]-1)
                self.out_maze()
                input()
        else:
            print('Path is not found.')


class MultiFoodSearchProblem:
    def __init__(self, maze_file):

        # Đọc map cho pacman
        self.state = self.read_maze(maze_file)
        
        # Khởi tạo vị trí ban đầu và vị trí đích đến (food)
        self.init_state, self.goal_state = self.ini()

        # Khởi tạo vị trí ban đầu cho node (pacman)
        self.node = self.init_state

        # Đường đi từ node đến food
        self.solution = []

    # Tìm kiếm và sắp xếp các successors theo ý tưởng ưu tiên các successor giúp pacman tiến nhanh đến
    # food hơn (ưu tiên các successor hướng tới food)
    def successor_func(self, curr_node, curr_goal):

        def sortbyCond_ar_dc(a, b): # ascending row - descending column
            if (a[0] != b[0]):
                return (a[0] - b[0])
            else:
                return b[1] - a[1] # Trường hợp cùng hàng thì so sánh cột
            
        def sortbyCond_dr_ac(a, b): # descending row - ascending column
            if (a[0] != b[0]):
                return b[0] - a[0]
            else:
                return b[1] - a[1] # Trường hợp cùng hàng thì so sánh cột
            
        # node = [hànd, cột]
        row = curr_node[0]
        column = curr_node[1]

        # Số hàng của map
        numRows = len(self.state)

        # Số cột của map
        numCols = len(self.state[0])

        successors = []

        # Xét 4 hướng vị
        for newPos in [(row, column + 1), (row + 1, column), (row, column - 1), (row - 1, column)]:
            
            # Kiểm tra vị trí hợp lệ của pacman
            if newPos[0] < numRows and newPos[1] < numCols and self.state[newPos[0]][newPos[1]] != '%':
                successors.append(newPos)

        # Theo ý tưởng của hàm
        # self.goal_state
        if curr_goal[0] >= row and curr_goal[1] <= column:
            successors.sort(key = cmp_to_key(sortbyCond_ar_dc))
        elif curr_goal[0] >= row and curr_goal[1] >= column:
            successors.sort(key = cmp_to_key(sortbyCond_dr_ac), reverse=True)
        elif curr_goal[0] <= row and curr_goal[1] <= column:
            successors.sort(key = cmp_to_key(sortbyCond_dr_ac))
        else:
            successors.sort(key = cmp_to_key(sortbyCond_ar_dc), reverse=True)
        return successors
    
    # Kiểm tra đã đến food chưa
    def goal_test_func(self, all_food):
        if len(self.goal_state)!=len(all_food):
            return False
        for i in self.goal_state:
            if self.goal_state.count(i) != all_food.count(i):
                return False
        return True
    
    # Trừ chữ 'Stop' trong path
    def path_cost_func(self):
        return len(self.solution) - 1
    
    # Đọc mê cung
    def read_maze(self, maze_file):
        maze = []
        with open(maze_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                maze.append(line)
        return maze
    
    # Lấy vị trí của pacman và vị trí các food
    def ini(self):
        pacman = None
        goals = []
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j]=="P":
                    pacman = (i ,j)
                elif self.state[i][j]==".":
                    goals.append((i,j))
        if not pacman or not goals:
            print("Invalid environment.")
            exit()
        return pacman, goals
    
    # In ra map màn hình console
    def out_maze(self):
        for line in self.state:
            print(line)
    
    # Play game
    def animate(self) -> None:
        
        # Khi không tìm được đường, thì path chỉ chứa "Stop"
        if self.solution[0]!="Stop":

            # Để thay đổi " " bằng P mỗi khi pacman đi được một bước
            def update(line_maze, col, p):
                st = list(line_maze)
                st[col] = p
                return ''.join(st)
            
            # Xóa tất cả
            os.system('cls')

            # Trạng thái ban đầu
            self.out_maze()
            input()

            # Pacman bắt đầu đi
            for i in self.solution:
                os.system('cls')
                if i == 'Stop':
                    self.out_maze()
                    print("Congratulations!")
                    break
                self.state[self.init_state[0]] = update(self.state[self.init_state[0]], self.init_state[1], ' ')
                if i == 'N':
                    self.state[self.init_state[0]-1] = update(self.state[self.init_state[0]-1], self.init_state[1], 'P')
                    self.init_state = (self.init_state[0]-1, self.init_state[1])
                elif i == 'S':
                    self.state[self.init_state[0]+1] = update(self.state[self.init_state[0]+1], self.init_state[1], 'P')
                    self.init_state = (self.init_state[0]+1, self.init_state[1])
                elif i == 'E':
                    self.state[self.init_state[0]] = update(self.state[self.init_state[0]], self.init_state[1]+1, 'P')
                    self.init_state = (self.init_state[0], self.init_state[1]+1)
                elif i == 'W':
                    self.state[self.init_state[0]] = update(self.state[self.init_state[0]], self.init_state[1]-1, 'P')
                    self.init_state = (self.init_state[0], self.init_state[1]-1)
                self.out_maze()
                input()
        else:
            print('Path is not found.')
            