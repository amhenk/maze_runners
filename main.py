from sys import argv
import argparse
import maze

def main():
    global EUC_DIST
    if EUC_DIST == 0:
        EUC_DIST = (height * width) * .01#(min([height, width]) / max([height, width]))
    m = maze.Maze(height, width, EUC_DIST)
    m.gen_maze()
    # m.print_maze()
    b = maze.validate_maze(m, verbose, diag)
    if b[1] == False:
        if verbose:
            m.print_maze()
        print "After {} iterations there was no path to G".format(b[0])
    else:
        for p in b[1]:
            if p in [m.s_pos, m.g_pos]:
                continue
            m.maze[p[0]][p[1]] = maze.TRAVEL_TOKEN
        m.print_maze()
        print "After {} iterations a path to G was found".format(b[0])


if __name__ == '__main__':
    global EUC_DIST
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--verbose', help='Verbose Output', action="store_true")
    ap.add_argument('-d', '--diagonal', help='Allow diagonal Movement', action="store_true")
    ap.add_argument('-l', '--length', help='Length of maze', default=10, type=int)
    ap.add_argument('-w', '--width', help='Width of maze', default=10, type=int)
    ap.add_argument('-dist', '--distance', help='Euclidean Distance between start and goal', default=0.0, type=float)

    args = vars(ap.parse_args())
    verbose = args["verbose"]
    diag = args["diagonal"]
    height = args["length"]
    width = args["width"]
    EUC_DIST = args["distance"]
    
    main()
