import random
from math import sqrt
from pprint import pprint
from collections import defaultdict

try:
    from colorama import Fore, Back, init
    crama = True
except ImportError:
    crama = False


def euclidean(n, p):
    (x1,y1) = n
    (x2, y2) = p
    return sqrt(pow((x1-x2),2) + pow((y1-y2),2))


def reset():
    if crama:
        return Fore.RESET


if crama:
    init(autoreset=True)

    WALL_TOKEN = Fore.GREEN + '#' + reset()
    FLOOR_TOKEN = Fore.WHITE + '.' + reset()
    BOT_TOKEN = Back.WHITE + 'b' + Back.RESET
    GOAL_TOKEN = Back.YELLOW + 'G' + Back.RESET
    TRAVEL_TOKEN = Fore.RED + 'x' + reset()
else:
    WALL_TOKEN = '#'
    FLOOR_TOKEN = '.'
    BOT_TOKEN = 'b'
    GOAL_TOKEN = 'G'
    TRAVEL_TOKEN = 'x'


class Maze():
    def __init__(self, h,w, dist):
        self.height = h
        self.width = w
        self.maze = []
        self.s_pos = None
        self.g_pos = None
        self.eu_dist = dist

    def gen_maze(self):
        tried_goals, c = [], []
        for x in range(self.height+2):
            c = []
            if x == 0 or x == self.height+1:
                c = [ WALL_TOKEN ] * (self.width+2)
            else:
                for y in range(self.width+2):
                    r = random.randint(0,2)
                    if y == 0 or y == self.width+1 or r == 1:
                        c.append(WALL_TOKEN)
                    else:
                        c.append(FLOOR_TOKEN) 
                reset()
            self.maze.append(c)

        # Start position
        self.s_pos = (random.randint(1, self.height), random.randint(1, self.width))
        # Goal position
        self.g_pos = (random.randint(1, self.height), random.randint(1, self.width))

        # If the distance is less than the desired eu_dist then try again! The goal of this
        # is to make the solution at least mildly interesting.
        eu = euclidean(self.g_pos, self.s_pos)
        print("Finding decent Euclidean Distance that is larger than: {:.4f}".format(self.eu_dist))
        while eu < self.eu_dist:
            self.s_pos = (random.randint(1, self.height), random.randint(1, self.width))
            self.g_pos = (random.randint(1, self.height), random.randint(1, self.width))
            eu = euclidean(self.g_pos, self.s_pos)
        print("Distance found:", eu)

        self.maze[self.s_pos[0]][self.s_pos[1]] = BOT_TOKEN
        self.maze[self.g_pos[0]][self.g_pos[1]] = GOAL_TOKEN

    def print_maze(self):
        m = "\n"
        for x in range(self.height+2):
            if crama:
                m += Fore.WHITE + "{:<4} ".format(x) + reset()
            else:
                m += "{:<4} ".format(x)
            for y in range(self.width+2):
                m += self.maze[x][y]
            m += "\n" 
        print(m)

def validate_maze(maze, verbose, diag):

    # Finds the minimizing element of a list
    def argmin(ls):
        return min(ls.items(), key=lambda x: x[1])

    def reconstruct_path(cameFrom, current):
        total_path = []
        for c in cameFrom.keys():
            c = cameFrom[c]
            total_path.append(c)
        return total_path

    def a_star(start, goal):
        def heuristic(n, p):
            (x1,y1) = n
            (x2, y2) = p
            return abs(x1-x2) + abs(y1-y2)
        iterations = 0
        surroundings = [(0,1),(0,-1),(1,0),(-1,0)]
        if diag:
            surroundings.extend([(1,-1),(1,1),(-1,1),(-1,-1)])
        closed = []
        openset = [start]
        camefrom = {}

        gScore = defaultdict(lambda: float("inf"))
        fScore = defaultdict(lambda: float("inf"))

        gScore[start] = 0
        fScore[start] = heuristic(start, goal)

        while openset:
            if verbose:
                pprint("Coords in open -> {}".format(openset))
            c = argmin(fScore)[0] 
            if c == goal:
                return (iterations, reconstruct_path(camefrom, c))

            openset.remove(c)
            del fScore[c]
            closed.append(c)
            for x in surroundings:
                n = (c[0]+x[0],c[1]+x[1])
                if n in closed or m[n[0]][n[1]] == WALL_TOKEN:
                    continue
                tent_gScore = gScore[c] + 1
                if n not in openset:
                    openset.append(n)
                elif tent_gScore >= gScore[n]:
                    continue

                camefrom[n] = c
                gScore[n] = tent_gScore
                fScore[n] = gScore[n] + heuristic(n, goal)

            iterations += 1
        return (iterations, False)

    start, goal = maze.s_pos, maze.g_pos
    m = maze.maze
    bucket = a_star(start, goal)
    return bucket

