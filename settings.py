from map import *
WIDTH, HEIGHT = (800, 600)
GRID_SIZE = 600
FPS = 60
gap = .1
number_of_nodes = len(map[0])
node_rect_size = ((GRID_SIZE/number_of_nodes) * (1 - gap))
node_gap_size = ((GRID_SIZE/number_of_nodes) * gap)
node_add = GRID_SIZE/number_of_nodes