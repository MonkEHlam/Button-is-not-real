import pygame
import Button_class
import Counter_class
import Screwdriver_class
import Blink_class
import constants
from load_image_func import load_image



if __name__ == "__main__":
    pygame.init()
    all_sprites = pygame.sprite.Group()
    blink_group = pygame.sprite.Group()
    movable_sprites = pygame.sprite.Group()
    size = width, height = constants.RESOLUTION
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill("white")

    # Create every base sprites
    counter = Counter_class.Counter(all_sprites, screen)
    button = Button_class.Button(all_sprites, screen, counter, movable_sprites)
    screwdriver = Screwdriver_class.Screwdriver(movable_sprites, screen)
    blink = Blink_class.Blink(blink_group, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            screen.fill("white")
            all_sprites.update(event)
            movable_sprites.update(event)
            blink_group.update(event)
        
        screen.fill('white')
        # updating sprites if there is no new events
        all_sprites.update()
        movable_sprites.update()
        blink_group.update()

        all_sprites.draw(screen)
        movable_sprites.draw(screen)
        blink_group.draw(screen)
        
        # The development point of ending score
        if counter.get_score() == 40:
            running = False
        clock.tick(constants.FPS)
        pygame.display.flip()
    pygame.quit()