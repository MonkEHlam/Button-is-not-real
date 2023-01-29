import pygame
import constants
from load_image_func import load_image
import random


class Radio(pygame.sprite.Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.is_on = False
        self.volume = 0.5
        self.noizes = False

        pygame.mixer.music.load("sounds/radio.mp3")
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_pos(random.randint(15, constants.RADIO_MUSIC_LENGTH)) # set random position for effect of real life
        
        self.s_click = pygame.mixer.Sound("sounds/radio_click.ogg")
        self.s_noizes = pygame.mixer.Sound("sounds/noizes.ogg")
        self.s_noizes.set_volume(0.7)

        self.image = load_image("radio.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = constants.RADIO_POS

    def update(self, *args, **kwargs) -> None:
        #on off radio
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and args[0].button == 1
            and self.rect.collidepoint(args[0].pos)
        ):
            self.s_click.play()
            self.is_on = not self.is_on
            print(1)
            if self.is_on:
                if self.noizes:
                    self.s_noizes.set_volume(0.7)
                else:
                    pygame.mixer.music.set_volume(self.volume)
            else:
                if self.noizes:
                    self.s_noizes.set_volume(0)
                    print(1)
                else:
                    pygame.mixer.music.set_volume(0)

        # Turn up volume
        if (
            args
            and self.is_on
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and args[0].button == 4
            and not self.noizes
            and self.rect.collidepoint(args[0].pos)
        ):
            if self.volume < 1:
                self.volume += 0.1
                pygame.mixer.music.set_volume(self.volume)

        # Turn down volume
        if (
            args
            and self.is_on
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and args[0].button == 5
            and not self.noizes
            and self.rect.collidepoint(args[0].pos)
        ):
            if self.volume > 0.1:
                self.volume -= 0.1
                pygame.mixer.music.set_volume(self.volume)
            else:
                self.volume = 0.15
                pygame.mixer.music.set_volume(0)
                self.s_click.play()
                self.is_on = False
        
        if args and args[0].type == constants.EVENTS["RADIOCRACK"]:
            if not self.noizes:
                pygame.time.set_timer(constants.EVENTS["RADIOCRACK"], 8000)
                self.s_noizes.play(-1)
                self.is_on = True
                self.noizes = True
            else:
                pygame.time.set_timer(constants.EVENTS["RADIOCRACK"], 0)
                self.s_noizes.stop()
                self.noizes = False