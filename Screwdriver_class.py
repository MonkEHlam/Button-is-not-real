import pygame
import constants
from load_image_func import load_image


class Screwdriver(pygame.sprite.Sprite):
    def __init__(self, sprite_group, screen, blink):
        super().__init__(sprite_group)
        self.screen = screen

        # Load all pictures of sprite
        self.base_image = load_image("screwdriver.png", folder="/screwdriver")
        self.rotation_in = [
            load_image("rotation1.png", folder="/screwdriver"),
            load_image("rotation2.png", folder="/screwdriver"),
        ] + [
            load_image("rotation1.png", folder="/screwdriver"),
            load_image("rotation2.png", folder="/screwdriver"),
        ]
        self.rotation_out = self.rotation_in[::-1]
        self.boom = [
            load_image("boom1.png", folder="/screwdriver"),
            load_image("boom2.png", folder="/screwdriver"),
            load_image("boom3.png", folder="/screwdriver"),
            0,
        ]
        self.rotation_in.append(0)
        self.rotation_out.append(0)

        self.anim_number = 0
        self.blink = blink
        self.image = self.base_image  # Variable for storing the selected image
        self.is_grab = False
        self.fixing = False
        self.rect = self.image.get_rect()
        self.screw = 0

        # Set start position of sprite
        self.rect.x, self.rect.y = constants.SCREWDRIVER_POS

    def update(self, *args) -> None:

        # Check is screwdriver is picked up
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and args[0].button == 1
            and not self.fixing
            and self.rect.collidepoint(args[0].pos)
            and not self.blink.is_blink
        ):
            self.is_grab = True
            self.image = self.base_image
            self.rect = self.image.get_rect()
            self.image.set_alpha(255)

        # Check is screwdriver is drop up
        if args and args[0].type == pygame.MOUSEBUTTONUP:
            self.is_grab = False
        # Moving scerdriver if it is picked up
        if self.is_grab:
            self.rect.center = pygame.mouse.get_pos()

        if args and args[0].type == constants.EVENTS["SCREWDRIVERANIMUPDATE"]:
            if self.anim_number == 0:
                if self.rotation_in[-1] == 4:
                    if self.screw != 3:
                        self.screw += 1
                        self.rotation_in[-1] = 0
                    else:
                        self.screw = 0
                        self.anim_number += 1
                        self.rotation_in[-1] = 0
                if self.rotation_in[-1] < 4:
                    self.rect.topleft = constants.SCREWS_POS[self.screw]
                    self.image = self.rotation_in[self.rotation_in[-1]]
                    self.rotation_in[-1] += 1

            elif self.anim_number == 1:
                self.rect.topleft = constants.BOOM_POS
                if self.boom[-1] == 3:
                    self.boom[-1] = 0
                    self.anim_number += 1

                if self.boom[-1] < 3:
                    self.image = self.boom[self.boom[-1]]
                    self.boom[-1] += 1

            else:
                if self.rotation_out[-1] < 4:
                    self.rect.topleft = constants.SCREWS_POS[self.screw]
                    self.image = self.rotation_out[self.rotation_out[-1]]
                    self.rotation_out[-1] += 1

                if self.rotation_out[-1] == 4:
                    if self.screw != 3:
                        self.screw += 1
                        self.rotation_out[-1] = 0
                    else:
                        self.screw = 0
                        self.rotation_out[-1] = 0
                        pygame.time.set_timer(
                            constants.EVENTS["SCREWDRIVERANIMUPDATE"], 0
                        )
                        self.rect.x, self.rect.y = constants.SCREWDRIVER_POS
                        self.anim_number = 0
                        self.image = self.base_image
