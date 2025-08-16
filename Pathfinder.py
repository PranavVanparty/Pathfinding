import pygame
from queue import PriorityQueue
from Space import Space
import math
     

WIDTH = 800 
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def make_grid(rows, width):
    grid = [] 
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            space = Space(i, j, gap, rows)
            if (i == 0 or i == rows-1) or (j == 0 or j == rows-1):
                space.make_barrier()
            grid[i].append(space)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))
            
def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for space in row:
            space.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    x, y = pos
    gap = width // rows
    row = y // gap
    col = x // gap
    return row, col

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # Manhattan distance - It makes an L shape path since we can't traverse diagonally
    return abs(x2 - x1) + abs(y2 - y1)

def a_star_algorithm(draw, grid, start, end):
    count = 0 # Used to break ties by choosing based on what was inserted first
    
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    
    came_from = {}
    
    f_score = {space : float("inf") for row in grid for space in row} # Total Score (g_score + h_score). Init value is infinity
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    g_score = {space : float("inf") for row in grid for space in row} # Distance from start. Init value is infinity
    g_score[start] = 0
    
    open_set_hash = {start}
    
    while not open_set.empty():
        print("started while loop")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            # Reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:  # Don't change the start node's color
                    current.make_path()
                draw()
            return True
        
        print("neighbors: ", len(current.neighbors))
        for neighbor in current.neighbors:
            print("looking at neighbors")
            temp_g_score = g_score[current] + 1  # Fix: Use current's g_score + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    print("Considared neighbor")
                
        draw()
        
        if current != start:
            current.make_closed()
            
    return False  # No path found

def main(win, width):
    rows = 50 
    grid = make_grid(rows, width)
    
    start = None
    end = None
    
    run = True
    started = False
    
    while run :
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(pos, rows, width)  # NOTE: col=rowIndex, row=colIndex intentionally
                space = grid[row][col]  # adjust indexing to match swapped variable meaning
                if start is None and space != end and not space.is_barrier():
                    start = space
                    start.make_start()
                elif end is None and space != start and not space.is_barrier():
                    end = space
                    end.make_end()
                elif space != end and space != start:
                    space.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(pos, rows, width)  # NOTE: swapped naming retained
                space = grid[row][col]  # adjusted
                if space == start:
                    start = None
                if space == end:
                    end = None
                space.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    # Guard: need both start and end
                    if start and end:
                        for row_list in grid:
                            for space in row_list:
                                space.update_neighbors(grid)
                        started = True
                        path_found = a_star_algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                        # Optional: Display message if no path found
                        if not path_found:
                            print("No path found!")
                        started = False
                    # else: silently ignore or add print for debugging
                elif event.key == pygame.K_c:
                    # Optional clear grid shortcut
                    start = None
                    end = None
                    grid = make_grid(rows, width)
    
    pygame.quit()
    
main(WIN, WIDTH)
