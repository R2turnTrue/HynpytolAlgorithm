from queue import PriorityQueue

# 비어 있음: 0
# 벽: 1
# 단핵구: 2

# 감염세포 (왼쪽 바라봄): 3
# 감염세포 (오른쪽 바라봄): 4
# 감염세포 (위쪽 바라봄): 5
# 감염세포 (아래쪽 바라봄): 6

# 플레이어: 7
# 목적지: 8

# 흰피톨 챕터 1: 움직이기 전에 생각했나요?

COLLIDABLE_TILES = [1, 2, 3, 4, 5, 6]
MAX_CAST_ITERATION = 20
m = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 8, 0, 0, 0, 6, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 4, 0, 0, 2, 0, 0, 0, 3, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

print('Figuring out the player pos & goal...')

class MapState:
    def __init__(self, player_pos, goal_pos, infected_cells):
        self.player_pos = player_pos
        self.goal_pos = goal_pos
        self.infected_cells = infected_cells

def search_map(m):
    player_pos = [-1, -1]
    goal_pos = [-1, -1]

    # (x, y, direction) for infected cells
    # direction: 0 = left, 1 = right, 2 = up, 3 = down
    infected_cells = []
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] == 7:
                player_pos = [x, y]
                print(f'Player found at {player_pos}')
            
            if m[y][x] == 8:
                goal_pos = [x, y]
                print(f'Goal found at {goal_pos}')
            
            if m[y][x] >= 3 and m[y][x] <= 6:
                infected_cells.append((x, y, m[y][x] - 3))
                print(f'Infected cell found at {infected_cells[-1]}')

    if player_pos == [-1, -1]:
        raise ValueError('Player not found in the map!')

    if goal_pos == [-1, -1]:
        raise ValueError('Goal not found in the map!') 
    
    return MapState(player_pos, goal_pos, infected_cells)

default_map_state = search_map(m)

class StateNode:
    def __init__(self, player_pos, m, remain_infected, is_pulling=False, pull_direction=[-1,-1]):
        self.player_pos = player_pos
        self.map = m
        self.remain_infected = remain_infected
        self.is_pulling = is_pulling
        self.pull_direction = pull_direction

    def __hash__(self):
        return hash((tuple(self.player_pos), tuple(tuple(row) for row in self.map)))

pq = PriorityQueue()

# f(x) = g(x) + h(x)
# g(x) = 0 (현재 상태에서의 비용)
# h(x) = sqrt((목표 x - 현재 x)^2 + (목표 y - 현재 y)^2) + ... + (그 목표가 감염세포도 포함함.) (목표까지의 예상 비용, 목표까지의 거리.)
pq.put((0, StateNode(default_map_state.player_pos, m, len(default_map_state.infected_cells))))

def get_vector_from_direction(direction):
    if direction == 0:  # left
        return [-1, 0]
    elif direction == 1:  # right
        return [1, 0]
    elif direction == 2:  # up
        return [0, -1]
    elif direction == 3:  # down
        return [0, 1]
    else:
        raise ValueError('Invalid direction')

while not pq.empty():
    node: StateNode = pq.get()[1]

    if node.remain_infected == 0 and node.player_pos == default_map_state.goal_pos:
        print('Goal reached!')
        break

    current_map_state = search_map(node.map)

    if not node.is_pulling:
        # 기본 상태
        # 0 = left, 1 = right, 2 = up, 3 = down
        for i in range(4):
            direction_vector = get_vector_from_direction(i)
            new_player_pos = [node.player_pos[0] + direction_vector[0], node.player_pos[1] + direction_vector[1]]
            opposite_player_pos = [node.player_pos[0] - direction_vector[0], node.player_pos[1] - direction_vector[1]]
            
            if node.map[new_player_pos[1]][new_player_pos[0]] != 1 or node.map[opposite_player_pos[1]][opposite_player_pos[0]] != 1:
                pq.put((0, StateNode(node.player_pos, node.map, node.remain_infected, True, direction_vector)))
    else:
        after_pull = [node.player_pos[0], node.player_pos[1]]
        find_pull = False
        new_map = [row[:] for row in node.map]
        
        for i in range(MAX_CAST_ITERATION):
            tileId = node.map[after_pull[1] + node.pull_direction[1]][after_pull[0] + node.pull_direction[0]]
            if tileId in COLLIDABLE_TILES:
                if tileId >= 3 and tileId <= 6:
                    facing_vec = get_vector_from_direction(tileId - 3)
                    if node.pull_direction == [-facing_vec[0], -facing_vec[1]]:
                        find_pull = True
                        break
                else:
                    find_pull = True
                    break
            
            after_pull[0] += node.pull_direction[0]
            after_pull[1] += node.pull_direction[1]
        
        if not find_pull:
            print('Pulling failed, no wall found in the direction.')
            continue

        if node.map[after_pull[1]][after_pull[0]] >= 3 and node.map[after_pull[1]][after_pull[0]] <= 6:
            # 감염세포를 당겼을 때
            new_map[after_pull[1] + node.pull_direction[1]][after_pull[0] + node.pull_direction[0]] = 0
            # todo:
        
        pq.put((0, StateNode(after_pull, new_map, node.remain_infected, False, [-1, -1])))