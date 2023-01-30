import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_group, sheet, columns, rows, x, y):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )

    def update(self, *args):
        if args:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
