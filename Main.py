import pygame
import Button_class
import Counter_class
import Screwdriver_class
import constants
from load_image_func import load_image


if __name__ == "__main__":
    pygame.init()
    all_sprites = pygame.sprite.Group()
    movable_sprites = pygame.sprite.Group()
    size = width, height = constants.RESOLUTION
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill("white")

    counter = Counter_class.Counter(all_sprites, screen)
    button = Button_class.Button(all_sprites, screen, counter, movable_sprites)
    screwdriver = Screwdriver_class.Screwdriver(movable_sprites, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.fill("white")
            all_sprites.update(event)
            movable_sprites.update(event)
        all_sprites.draw(screen)
        movable_sprites.draw(screen)
        if counter.get_score() == 40:
            running = False
        clock.tick(constants.FPS)
        pygame.display.flip()
    pygame.quit()
