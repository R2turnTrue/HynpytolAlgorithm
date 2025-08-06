from queue import PriorityQueue
import heapq
import itertools
from game import read_map, GameState, get_vector_from_direction

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

came_from = {}

while queue:
    f, g, count, (current_state, visited_cp) = heapq.heappop(queue)
    
    if (current_state, visited_cp) in visited:
        continue
    
    visited.add((current_state, visited_cp))
    
    if current_state.player_pos == goal_pos and len(visited_cp) == total_checkpoints:
        print("GOAL!")
        print(str(current_state))
        lp = None
        path = []
        print(came_from[lp])
        path.reverse()
        print(path)
        break
    
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
        
        new_st = (new_state.clone(), new_visited_cp)
        new_g = g + 1
        new_f = new_g + heuristic(new_state.player_pos, goal_pos)
        
        heapq.heappush(queue, (new_f, new_g, next(counter), new_st))
        came_from[new_state] = current_state
        print(new_state)
        #print(f'Checkpoint remain: {total_checkpoints - len(new_visited_cp)}')