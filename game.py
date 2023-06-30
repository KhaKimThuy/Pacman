from problems import SingleFoodSearchProblem, MultiFoodSearchProblem
from searchAgents import bfs, dfs, ucs

if __name__=='__main__':
    pacman = SingleFoodSearchProblem('maze.txt')
    # pacman = MultiFoodSearchProblem('maze.txt')
    bfs(pacman)
    pacman.animate()
    # print(bfs(pacman))
# (3, 11)
# [((8, 1), 125)]
# [(8, 1)]