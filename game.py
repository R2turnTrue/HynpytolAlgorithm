import copy
import sys

##ACTIONS
# 0: 팔 밀기
# 1: 팔 당기기

# 비어 있음: 0
# 벽: 1
# 단핵구: 2

# 감염세포 (왼쪽 바라봄): 3
# 감염세포 (오른쪽 바라봄): 4
# 감염세포 (위쪽 바라봄): 5
# 감염세포 (아래쪽 바라봄): 6

# 플레이어: 7
# 목적지: 8
WALL_TILES = [1, 2, 3, 4, 5, 6]

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

def read_map():
    map_file = open(sys.argv[1], 'r', encoding='utf-8')
    m = eval(map_file.read())
    map_file.close()
    return m

def figure_player_pos(m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] == 7:
                player_pos = [x, y]
                #print(f'Player found at {player_pos}')
                return player_pos
    raise ValueError('Player not found in the map!')

def raycast_tile(m, start_pos, direction):
    x, y = start_pos
    dx, dy = direction
    while 0 <= x < len(m[0]) and 0 <= y < len(m):
        if m[y][x] in WALL_TILES:  # If not empty tile
            return (x, y)
        x += dx
        y += dy
    raise ValueError(f'Raycast {start_pos} to {direction} did not hit any wall tile! Start position or direction may be invalid.')

def swap_tile(m, tp_01, tp_02):
    m[tp_01[1]][tp_01[0]], m[tp_02[1]][tp_02[0]] = m[tp_02[1]][tp_02[0]], m[tp_01[1]][tp_01[0]]
    
    return m

class GameState:
    def __init__(self, m):
        self.m = m
        self.player_pos = figure_player_pos(m)
        self.player_arm_state = False
        self.player_arm_direction = [-1, -1]
        self.player_arm_raycast_to = [-1, -1]
        self.player_arm_opposite_raycast_to = [-1, -1]
        self.actions = []
    
    def __str__(self):
        return f'GameState(player_pos={self.player_pos}, player_arm_state={self.player_arm_state}, player_arm_direction={self.player_arm_direction}, player_arm_raycast_to={self.player_arm_raycast_to}, player_arm_opposite_raycast_to={self.player_arm_opposite_raycast_to}), actions={self.actions})'

    def clone(self):
        new_self = GameState(copy.deepcopy(self.m))
        new_self.player_pos = [self.player_pos[0], self.player_pos[1]]
        new_self.player_arm_state = self.player_arm_state
        new_self.player_arm_direction = [self.player_arm_direction[0], self.player_arm_direction[1]]
        new_self.player_arm_raycast_to = [self.player_arm_raycast_to[0], self.player_arm_raycast_to[1]]
        new_self.player_arm_opposite_raycast_to = [self.player_arm_opposite_raycast_to[0], self.player_arm_opposite_raycast_to[1]]
        new_self.actions = list(self.actions)  # Copy the actions list
        return new_self

    def get_all_infected_cells_array(self):
        infected_cells = []
        for y in range(len(self.m)):
            for x in range(len(self.m[y])):
                if self.m[y][x] >= 3 and self.m[y][x] <= 6:
                    tile_dir = get_vector_from_direction(self.m[y][x] - 3)
                    infected_cells.append([x + tile_dir[0], y + tile_dir[1]])
        return infected_cells
    
    def get_destination(self):
        for y in range(len(self.m)):
            for x in range(len(self.m[y])):
                if self.m[y][x] == 8:
                    return [x, y]
        return None
    
    def last_action(self):
        if len(self.actions) == 0:
            return None
        return self.actions[-1]

    def action_tuple(self):
        return tuple(self.actions)

    def movable_directions(self):
        directions = []
        pos = self.player_pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.m[pos[1] + dy][pos[0] + dx] == 0:
                directions.append((dx, dy))
        return directions

    def push_arm(self, dir):
        new_self = self.clone()
        
        dir_opposite = [-dir[0], -dir[1]]
        if not new_self.player_arm_state:
            new_self.player_arm_state = True
            new_self.player_arm_direction = dir
            new_self.player_arm_raycast_to = raycast_tile(new_self.m, new_self.player_pos, dir)
            new_self.player_arm_opposite_raycast_to = raycast_tile(new_self.m, new_self.player_pos, dir_opposite)
            new_self.actions.append((0, tuple(dir)))
        else:
            # 팔 방향과 같은 방향으로 누름 (밀기)
            if new_self.m[new_self.player_pos[1] - dir[1]][new_self.player_pos[0] - dir[0]] == 2:
                # 뒤에 단핵구 있으면 단핵구를 벽 끝까지 이동함.
                back_cast = raycast_tile(new_self.m, [new_self.player_pos[0] - dir[0] * 2, new_self.player_pos[1] - dir[1] * 2], dir_opposite)

                new_self.m = swap_tile(new_self.m, [new_self.player_pos[0] - dir[0], new_self.player_pos[1] - dir[1]], [back_cast[0] + dir[0], back_cast[1] + dir[1]])

                new_self.player_pos = [back_cast[0] + dir[0] * 2, back_cast[1] + dir[1] * 2]
            elif new_self.m[new_self.player_arm_raycast_to[1]][new_self.player_arm_raycast_to[0]] == 2:
                # 팔 뻗은 곳에 단핵구 있으면 단핵구를 벽 끝까지 이동함.
                cast = raycast_tile(new_self.m, [new_self.player_arm_raycast_to[0] + dir[0], new_self.player_arm_raycast_to[1] + dir[1]], dir)

                if new_self.m[cast[1] - dir[1]][cast[0] - dir[0]] in WALL_TILES:
                    # 이미 단핵구가 벽 끝에 있는 상황
                    new_self.player_pos = [new_self.player_arm_opposite_raycast_to[0] + dir[0], new_self.player_arm_opposite_raycast_to[1] + dir[1]]

                new_self.m = swap_tile(new_self.m, [new_self.player_arm_raycast_to[0], new_self.player_arm_raycast_to[1]], [cast[0] - dir[0], cast[1] - dir[1]])
                new_self.player_arm_raycast_to = [cast[0] - dir[0], cast[1] - dir[1]]
            else:
                new_self.player_pos = [new_self.player_arm_opposite_raycast_to[0] + dir[0], new_self.player_arm_opposite_raycast_to[1] + dir[1]]

            new_self.actions.append((0, tuple(dir)))

        return new_self

    def pull_arm(self):
        new_self = self.clone()
        
        if new_self.player_arm_state:
            dir = [-new_self.player_arm_direction[0], -new_self.player_arm_direction[1]]
            cast_tile = new_self.m[new_self.player_arm_raycast_to[1]][new_self.player_arm_raycast_to[0]]
            if cast_tile == 2:
                # 단핵구일 경우 그냥 타일을 본인 앞으로 이동하기만 함
                new_self.m = swap_tile(new_self.m, new_self.player_arm_raycast_to, [new_self.player_pos[0] + new_self.player_arm_direction[0], new_self.player_pos[1] + new_self.player_arm_direction[1]])
            else:
                new_self.player_pos = [new_self.player_arm_raycast_to[0] + dir[0], new_self.player_arm_raycast_to[1] + dir[1]]
                if cast_tile >= 3 and cast_tile <= 6:
                    # 감염세포일 경우 팔 방향과 일치하는지 확인
                    tile_dir = get_vector_from_direction(cast_tile - 3)
                    if dir == tile_dir:
                        # 팔 방향과 일치시
                        #print('ok, removing infected')
                        new_self.m[new_self.player_arm_raycast_to[1]][new_self.player_arm_raycast_to[0]] = 0 # 타일 없앰

            new_self.player_arm_state = False
            new_self.player_arm_direction = [-1, -1]
            new_self.player_arm_raycast_to = [-1, -1]
            new_self.player_arm_opposite_raycast_to = [-1, -1]
            new_self.actions.append((1, tuple(dir)))

        return new_self