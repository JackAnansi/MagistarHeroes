'''
Created on Jan 24, 2016

@author: Dan
'''

import pygame
import universe
import character

pygame.init()

# Game setup
WIDTH = 800
HEIGHT = 600
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magistar Heroes')
clock = pygame.time.Clock()
game_objects = {}

def show_title_screen():
    gameDisplay.fill((0,0,0))
    try:
        logo = pygame.image.load('../img/magistar-logo.gif')
    except pygame.error:
        print ('Cannot load image')
        raise SystemExit
    logo = logo.convert()
    center_image(logo, gameDisplay)
    pygame.display.update()
    show_title = True
    while show_title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                show_title = False
    
def show_main_menu():
    # Give the user multiple options
    
    # TODO: Implement this
    
    # For now, assume they start a new game
    return "new game"

def handle_key_presses(keys):
    action = None
    
    for key in keys:
        #WASD movement
        # While key pressed, increase acceleration
        if key == pygame.K_a:
            player.move_left()
        elif key == pygame.K_d:
            player.move_right()
        # jump
        elif key == pygame.K_w:
            player.jump()

def move_and_draw_all_game_objects():
    gameDisplay.fill((255,255,255))
    for name, sprite in game_objects.items():
        sprite.update(clock)
        gameDisplay.blit(sprite.image, sprite.position)
    pygame.display.update()
    
def center_image(img, screen):
    w, h = img.get_size()
    pos = ((WIDTH / 2) - (w / 2), (HEIGHT / 2) - (h / 2))
    screen.blit(img, pos)
    
if __name__ == "__main__":
    # Title Screen
    show_title_screen()
    
    # Main menu
    option = show_main_menu()
    # TODO: only update dirty rects
    
    
    if option == "new game":
        playing = True
        dimension = universe.Universe("MagistarHeroes")    # this is the seed
        planet = dimension.galaxies[0].solars[0].planets[0]
        player = character.Character('mage', (20,200), 'Player')
        game_objects['player'] = player
    
    while playing:
        # Game loop
        
        # Handle events
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    playing = False
                #print(event)    #TODO: Pass key events to the key event handler, handle actions
                keys.append(event.key)
        handle_key_presses(keys)
            
            
        # Draw loop
        
        move_and_draw_all_game_objects()
    
        # Tick
        clock.tick_busy_loop(60)
        
