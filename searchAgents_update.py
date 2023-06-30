from fringes import Stack, Queue, PriorityQueue
from problems import SingleFoodSearchProblem
import numpy as np
from operator import itemgetter

############################# TASK 1 ####################################
def order_goals(goals, pacman_loc):
    if len(goals)==0:
        return goals
    o = []
    # print(pacman_loc)
    for goal in goals:
        dist = np.sum(np.square(np.array(goal, dtype=object) - np.array(pacman_loc, dtype=object)))
        o.append((goal, dist))
    # print(o)
    o = sorted(o, key=itemgetter(1))
    o = list(np.array(o, dtype=object)[:,0])
    return o

def bfs(pacman) -> list:

    # Kiểm tra pacman thuộc loại Single hay Multi
    single_pacman = isinstance(pacman, SingleFoodSearchProblem)

    if not single_pacman:

        # Sắp xếp lại các vị trí của food, theo ý tưởng ưu tiên các food gần vị trí của pacman
        goals = order_goals(pacman.goal_states, pacman.init_state)
    else:

        # Ép thành list để dùng cho cả 2 obj không bị lỗi
        goals = [pacman.goal_state]

    # Xét hết tất cả các food
    while goals:

        # Lấy food ra làm đích đến
        pacman.goal_state = goals.pop(0)

        # Tạo hàng đợi
        frontier = Queue()

        # Đưa node vào hàng đợi
        frontier.enqueue(pacman.node)

        # Tạo set kiểm tra các successors đã được đi
        explored = set()

        # Khởi tạo parent, để tìm lại path khi đã tìm được food
        parent = {pacman.node: None}
        
        # Kiểm tra nếu hàng đợi còn successor chưa đi và chưa tìm được goal thì tìm tiếp
        while not frontier.empty():

            # Lấy vị trí pacman (phần tử đầu tiên của frontier)
            pacman.node = frontier.dequeue()

            # Vị trí đã được dùng
            explored.add(pacman.node)

            # Kiểm tra coi đã đến đích chưa
            if pacman.goal_test_func():
                path = []

                # Tìm lại đường đi từ food về vị trí ban đầu của pacman
                while pacman.node is not None:
                    path.append(pacman.node)
                    pacman.node = parent[pacman.node]

                # Đảo path lại cho đúng thứ tự
                path.reverse()

                # Single thì trả về luôn (1 path)
                if single_pacman:
                    pacman.solution = direction(path)
                    return pacman.solution
                
                # Multi thì thêm vào danh sách đường đi và xét tiếp goal khác
                else:
                    # Thêm vào danh sách đường đi
                    pacman.solution.extend(direction(path))

                    # Gán điểm bắt đầu cho goal tiếp theo là điểm đích đến của goal hiện tại
                    pacman.node = pacman.goal_state

                    # Vì vị trí hiện tại khác với vị trí ban đầu của node
                    # do đó vị trí các food so với pacman đã khác nên phải
                    # sắp xếp lại các goals mỗi khi bắt đầu tìm goal mới.
                    goals = order_goals(goals, pacman.node)

                    # tìm goal mới
                    break

            # Tìm các successors (đường đi 4 phía)
            successors = pacman.successor_func()

            # Vì trong successors có cài đặt đk, trong ngữ cảnh của bfs thì 
            # phải đảo lại thì mới đúng tính chất thuật toán =)
            successors.reverse()

            # Xét từng succ
            for successor in successors:
                
                # Nếu succ chưa được dùng thì mới được xét (để không lặp lạ đường cũ (graph search))
                if successor not in explored:

                    # Gán parent của succ là node đang được xét
                    parent[successor] = pacman.node

                    # Đưa các succ vào sau cùng của frontier
                    frontier.enqueue(successor)

        # Chưa tìm được goal, Single thì trả về, Multi tìm goal khác
        if single_pacman:
            pacman.solution.append('Stop')
            return pacman.solution
        
    # Bỏ các stop dư thừa vd:
    # 'W', 'N', 'Stop', 'W', 'E', 'Stop'
    # => 'W', 'N', 'W', 'E', 'Stop'
    while 'Stop' in pacman.solution: pacman.solution.remove('Stop')
    pacman.solution.append('Stop')
    return pacman.solution


def dfs(pacman) -> list:
    single_pacman = isinstance(pacman, SingleFoodSearchProblem)
    if not single_pacman:
        goals = order_goals(pacman.goal_states, pacman.init_state)
    else:
        goals = [pacman.goal_state]
    while goals:
        pacman.goal_state = goals.pop(0)
        frontier = Stack()
        frontier.push(pacman.node)
        explored = set()
        parent = {pacman.node: None}
        while not frontier.empty():

            # Lấy vị trí pacman (phần tử cuối cùng của frontier)
            pacman.node = frontier.pop()
            explored.add(pacman.node)
            if pacman.goal_test_func():
                path = []
                while pacman.node is not None:
                    path.append(pacman.node)
                    pacman.node = parent[pacman.node]
                path.reverse()
                if single_pacman:
                    pacman.solution = direction(path)
                    return pacman.solution
                else:
                    pacman.solution.extend(direction(path))
                    pacman.node = pacman.goal_state
                    goals = order_goals(goals, pacman.node)
                    break
            successors = pacman.successor_func()
            for successor in successors:
                if successor not in explored:
                    parent[successor] = pacman.node 

                    # Đưa các succ vào sau cùng của frontier
                    frontier.push(successor)

        if single_pacman:
            pacman.solution.append('Stop')
            return pacman.solution
    while 'Stop' in pacman.solution: pacman.solution.remove('Stop')
    pacman.solution.append('Stop')
    return pacman.solution

def ucs(pacman):
    single_pacman = isinstance(pacman, SingleFoodSearchProblem)
    if not single_pacman:
        goals = order_goals(pacman.goal_states, pacman.init_state)
    else:
        goals = [pacman.goal_state]
    while goals:
        # print(goals)
        pacman.goal_state = goals.pop(0)
        # print(pacman.goal_state)
        frontier = PriorityQueue()
        frontier.put((0, pacman.node, []))
        explored = set()
        while not frontier.empty():
            cost, pacman.node, path = frontier.get()
            if pacman.goal_test_func():
                if single_pacman:
                    pacman.solution = direction(path + [pacman.node])
                    return pacman.solution
                else:
                    pacman.solution.extend(direction(path + [pacman.node]))
                    pacman.node = pacman.goal_state
                    goals = order_goals(goals, pacman.node)
                    break
            explored.add(pacman.node)
            successors = pacman.successor_func()
            for successor in successors:
                if successor not in explored:

                    # Mỗi bước đi có cost=1
                    updated_cost = cost + 1

                    # (cost mới, successsor, đường đi cũ + vị trí hiện tại)
                    frontier.put((updated_cost, successor, path + [pacman.node]))
        if single_pacman:
            pacman.solution.append('Stop')
            return pacman.solution
    while 'Stop' in pacman.solution: pacman.solution.remove('Stop')
    pacman.solution.append('Stop')
    return pacman.solution


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

############################# TASK 2 ####################################
# YC2-1
def manhattan_Heuristic(pacman):
    y1, x1 = pacman.node
    y2, x2 = pacman.goal_state
    return abs(x1-x2) + abs(y1-y2)
## Tính admissible: vì hàm đánh giá bằng trị tuyệt đối của khoảng cách giữa hai trạng thái, do đó chỉ có thể bằng giá trị thực tế.
## Tính consistent: vì khoảng cách Manhattan giữa các trạng thái liên tiếp để đến trạng thái kế tiếp là bằng chi phí để di chuyển từ trạng thái hiện tại đến trạng thái kế tiếp.

def euclid_Heuristic(pacman, goal_state):
    y1, x1 = pacman.node
    y2, x2 = pacman.goal_state
    return ((x1-x2)**2 + (y1-y2)**2 )**(1/2)
## Tính admissible: vì hàm đánh giá bằng trị tuyệt đối của khoảng cách giữa hai trạng thái, do đó chỉ có thể nhỏ hơn hoặc bằng giá trị thực tế (TH nhỏ hơn: bất đẳng thức tam giác, TH bằng: đường thẳng)
## Không đảm bảo tính consistent: vì khoảng cách Euclid giữa các trạng thái liên tiếp để đến trạng thái kế tiếp có thể lơn hơn chi phí để di chuyển từ trạng thái hiện tại đến trạng thái kế tiếp. (vì cạnh huyền là cạnh dài nhất = sqrt(1^2 + 1^2) ~= 1.414, nhưng chi phí chuyển từ trạng thái trong bài toán này chỉ là 1)

# YC2-2
## Ý tưởng: Heuristic = Chi phí tới goal gần nhất và Chi phí tới các goals
def Cur2Goal2Goals_Heuristic(pacman):
    cur_state = pacman.init_state
    goals = pacman.goal_states
    min_dist = float('inf')

    ### Ước lượng tới goal gần nhất bằng Manhattan Heuristic
    min_dist = min(goals, key=lambda goal: manhattan_Heuristic(cur_state, goal))
    
    ### Ước lượng tới lần lượt các goal gần nhất (P->A, A->B, B->C, ...) bằng Manhattan Heuristic
    while goals:
        nearest_goal = min(goals, key=lambda goal: manhattan_Heuristic(cur_state, goal))
        all_dist += manhattan_Heuristic(cur_state, nearest_goal)

        cur_state = nearest_goal
        goals.remove(nearest_goal)

    return min_dist + all_dist

# YC-3
def astar(pacman, fn_heuristic) -> list:
    single_pacman = isinstance(pacman, SingleFoodSearchProblem)
    if not single_pacman:
        goals = order_goals(pacman.goal_states, pacman.init_state)
    else:
        goals = [pacman.goal_state]

    while goals:
        # print(goals)
        pacman.goal_state = goals.pop(0)
        # print(pacman.goal_state)
        
        frontier = PriorityQueue()
        frontier.put((0, pacman.node, []))
        explored = set()

        while not frontier.empty():
            cost, pacman.node, path = frontier.get()
            if pacman.goal_test_func():
                if single_pacman:
                    pacman.solution = direction(path + [pacman.node])
                    return pacman.solution
                else:
                    pacman.solution.extend(direction(path + [pacman.node]))
                    pacman.node = pacman.goal_state
                    goals = order_goals(goals, pacman.node)
                    break

            explored.add(pacman.node)
            pacman_node = pacman.node
            successors = pacman.successor_func()
            for successor in successors:
                if successor not in explored:
                    pacman.node = successor
                    update_cost = cost + 1
                    evaluation_function = update_cost + fn_heuristic(pacman)
                    frontier.put((evaluation_function, successor, path + [pacman_node]))

        if single_pacman:
            return pacman.solution
        
    while 'Stop' in pacman.solution: 
        pacman.solution.remove('Stop')
    pacman.solution.append('Stop')
    return pacman.solution
