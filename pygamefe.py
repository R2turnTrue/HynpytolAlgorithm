import pygame
from game import read_map, GameState, get_vector_from_direction
import time

MACRO = True
#MACRO_VALUE = "DAADSWWSDADADDDASWWSDAADSWADDASWWSDASWADSWWSADSSWDAADDASWWSDAADSWDASWWSDAADDDAADSWWSDAADWWSDAADSWDDADAADSWDASWDADDAADDASWWSDAADSWWWSDAADDAAADSWWSDAADSWWSDAAD"
MACRO_VALUE = "WSADDASSSWDAWSDAWSDDDAWSWSADSWADSWDASWADWSADWSDAWS"
MACRO_CURSOR = 0

m = read_map()
game_state = GameState(m)

TILE_SIZE = 32

pygame.init()
screen = pygame.display.set_mode((TILE_SIZE * len(m[0]), TILE_SIZE * len(m)))
pygame.display.set_caption("Hynpytol")

def keyp(k, game_state):
    dir = [0, 0]
    if k == 'W':
        dir = [0, -1]
        print('W pressed')
    elif k == 'S':
        dir = [0, 1]
        print('S pressed')
    elif k == 'A':
        dir = [-1, 0]
        print('A pressed')
    elif k == 'D':
        dir = [1, 0]
        print('D pressed')

    dir_opposite = [-dir[0], -dir[1]]
    
    if dir != [0, 0]:
        if not game_state.player_arm_state or dir == game_state.player_arm_direction:
            return game_state.push_arm(dir)
        elif dir == [-game_state.player_arm_direction[0], -game_state.player_arm_direction[1]]:
            return game_state.pull_arm()

def pygame_key_to_string(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            return 'W'
        elif event.key == pygame.K_s:
            return 'S'
        elif event.key == pygame.K_a:
            return 'A'
        elif event.key == pygame.K_d:
            return 'D'

macro_timer = 0.05
prevTime = time.time()
running = True
while running:
    now = time.time()
    deltaTime = now - prevTime
    prevTime = now

    if MACRO:
        macro_timer -= deltaTime
        if macro_timer <= 0:
            macro_timer = 0.05
            if MACRO_CURSOR < len(MACRO_VALUE):
                k = MACRO_VALUE[MACRO_CURSOR]
                MACRO_CURSOR += 1
                game_state = keyp(k, game_state)
            else:
                print('macro fin')
                MACRO = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            dir = [0, 0]
            if event.key == pygame.K_r:
                #reset map
                print('Reloading map')
                m = read_map()
                game_state = GameState(m)
            k = pygame_key_to_string(event)
            game_state = keyp(k, game_state)
    
    screen.fill((0, 0, 0))  # Fill the screen with black
    
    for y in range(len(game_state.m)):
        for x in range(len(game_state.m[y])):
            tile_value = game_state.m[y][x]
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
    
    if game_state.player_arm_state:
        pygame.draw.line(screen, (0, 128, 128), 
                         (game_state.player_pos[0] * TILE_SIZE + TILE_SIZE // 2, game_state.player_pos[1] * TILE_SIZE + TILE_SIZE // 2), 
                         ((game_state.player_arm_raycast_to[0] - game_state.player_arm_direction[0]/2.0) * TILE_SIZE + TILE_SIZE // 2, 
                          (game_state.player_arm_raycast_to[1] - game_state.player_arm_direction[1]/2.0) * TILE_SIZE + TILE_SIZE // 2), 
                         5)
        pygame.draw.circle(screen, (0, 128, 128), ((game_state.player_arm_raycast_to[0] - game_state.player_arm_direction[0]/2.0) * TILE_SIZE + TILE_SIZE // 2, 
                          (game_state.player_arm_raycast_to[1] - game_state.player_arm_direction[1]/2.0) * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)
        pygame.draw.rect(screen, (0, 128, 128), (game_state.player_pos[0] * TILE_SIZE, game_state.player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    else:
        pygame.draw.rect(screen, (0, 128, 255), (game_state.player_pos[0] * TILE_SIZE, game_state.player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()  # Update the display
    
pygame.quit()