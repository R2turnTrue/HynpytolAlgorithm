VISUALIZE = True
PATH = ''

from queue import PriorityQueue
import heapq
import itertools
from game import read_map, GameState, get_vector_from_direction
if VISUALIZE:
    import pygame
import time

def d2array_to_tuple(d2array):
    return tuple(tuple(row) for row in d2array)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

m = read_map()
st_game_state = GameState(m)

start_pos = st_game_state.player_pos

checkpoints = st_game_state.get_all_infected_cells_array()
checkpoints = {tuple(pos): idx for idx, pos in enumerate(checkpoints)}

total_checkpoints = len(checkpoints)
goal_pos = st_game_state.get_destination()

start_state = (st_game_state.clone(), frozenset())
counter = itertools.count()
queue = [(0 + heuristic(start_pos, goal_pos), 0, next(counter), start_state)]
visited = set()

min_chkp = 99999

screen = None

if VISUALIZE:
    TILE_SIZE = 32
    pygame.init()
    screen = pygame.display.set_mode((TILE_SIZE * len(m[0]), TILE_SIZE * len(m)))
    pygame.display.set_caption("Pathfinding")
    for i in range(1000):
        pygame.event.get()
        time.sleep(0.001)

while queue:
    f, g, count, (current_state, visited_cp) = heapq.heappop(queue)
    
    skip = False
    for (state, vs_cp) in visited:
        if state.player_pos == current_state.player_pos and state.m == current_state.m and state.last_action() == current_state.last_action() and vs_cp == visited_cp:
            skip = True
            break
    
    if skip:
        continue
    
    visited.add((current_state, visited_cp))
    
    if current_state.player_pos == goal_pos and not current_state.player_arm_state and len(visited_cp) == total_checkpoints:
        print("GOAL!")
        #print(current_state.actions)
        st = ''
        for action in current_state.actions:
            if action[1] == (0, 1):
                st += 'S'
            elif action[1] == (0, -1):
                st += 'W'
            elif action[1] == (1, 0):
                st += 'D'
            elif action[1] == (-1, 0):
                st += 'A'
        print(f'Path: {st}')
        PATH = st
        break

    ########## RENDERING

    if VISUALIZE:
        pygame.event.get()
        screen.fill((0, 0, 0))  # Fill the screen with black
        
        for y in range(len(current_state.m)):
            for x in range(len(current_state.m[y])):
                tile_value = current_state.m[y][x]
                draw_tile = False
                tile_color = (0, 0, 0)
                
                draw_direction = False
                direction_vector = [0, 0]
                
                if tile_value == 1:
                    draw_tile = True
                    tile_color = (255, 255, 255)
                elif tile_value == 2:
                    draw_tile = True
                    tile_color = (0, 255, 0)
                
                elif tile_value >= 3 and tile_value <= 6:
                    draw_tile = True
                    tile_color = (255, 0, 0)
                    draw_direction = True
                    direction_vector = get_vector_from_direction(tile_value - 3)
                
                elif tile_value == 8:
                    draw_tile = True
                    tile_color = (255, 128, 0)
                
                if draw_tile:
                    pygame.draw.rect(screen, tile_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
                if draw_direction:
                    pygame.draw.line(screen, (0, 0, 0), 
                                    (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 
                                    (x * TILE_SIZE + TILE_SIZE // 2 + direction_vector[0] * TILE_SIZE // 2, 
                                    y * TILE_SIZE + TILE_SIZE // 2 + direction_vector[1] * TILE_SIZE // 2), 
                                    3)
        
        if current_state.player_arm_state:
            pygame.draw.line(screen, (0, 128, 128), 
                            (current_state.player_pos[0] * TILE_SIZE + TILE_SIZE // 2, current_state.player_pos[1] * TILE_SIZE + TILE_SIZE // 2), 
                            ((current_state.player_arm_raycast_to[0] - current_state.player_arm_direction[0]/2.0) * TILE_SIZE + TILE_SIZE // 2, 
                            (current_state.player_arm_raycast_to[1] - current_state.player_arm_direction[1]/2.0) * TILE_SIZE + TILE_SIZE // 2), 
                            5)
            pygame.draw.circle(screen, (0, 128, 128), ((current_state.player_arm_raycast_to[0] - current_state.player_arm_direction[0]/2.0) * TILE_SIZE + TILE_SIZE // 2, 
                            (current_state.player_arm_raycast_to[1] - current_state.player_arm_direction[1]/2.0) * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)
            pygame.draw.rect(screen, (0, 128, 128), (current_state.player_pos[0] * TILE_SIZE, current_state.player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, (0, 128, 255), (current_state.player_pos[0] * TILE_SIZE, current_state.player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()  # Update the display

        #time.sleep(0.001)

    ##################
    
    actions: list[GameState] = []
    
    if not current_state.player_arm_state:
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_state = current_state.push_arm([direction[0], direction[1]])
            actions.append(new_state)
    else:
        actions.append(current_state.pull_arm())
        actions.append(current_state.push_arm(current_state.player_arm_direction))

    for new_state in actions:
        new_visited_cp = visited_cp
        if (new_state.player_pos[0], new_state.player_pos[1]) in checkpoints:
            idx = checkpoints[(new_state.player_pos[0], new_state.player_pos[1])]
            new_visited_cp = visited_cp.union([idx])
        
        remain_chp = total_checkpoints - len(new_visited_cp)

        if remain_chp < min_chkp:
            min_chkp = remain_chp
            print(f'Remaining checkpoints: {remain_chp}')

        #print(f'{new_state}')
        new_st = (new_state.clone(), new_visited_cp)
        new_g = g + 1
        new_f = new_g + heuristic(new_state.player_pos, goal_pos)
        
        heapq.heappush(queue, (new_f, new_g, next(counter), new_st))
        #print(new_state)
        #print(f'Checkpoint remain: {total_checkpoints - len(new_visited_cp)}')