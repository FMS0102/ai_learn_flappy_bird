import pygame
import os
import random

VIEW_HEIGTH = 500
VIEW_WIDTH = 800

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()

FONT_POINTS = pygame.font.SysFont('arial', 50)


class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.heigth = self.y
        self.time = 0
        self.count_image = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.heigth = self.y

    def move(self):
        # calculate displacement
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time

        # restrict displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # bird angle
        if displacement < 0 or self.y < (self.heigth + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, view):
        # set bird image
        self.count_image += 1

        if self.count_image < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.count_image < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]
        elif self.count_image < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]
        elif self.count_image < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]
        elif self.count_image >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.count_image = 0

        # set falling bird image
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.count_image = self.ANIMATION_TIME * 2

        # draw image
        rotation_image = pygame.transform.rotate(self.image, self.angle)
        img_center_position = self.image.get_rect(topleft=(self.x, self.y))
        rectangle = rotation_image.get_rect(center=img_center_position)

        view.blit(rotation_image, rectangle.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.image)


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.heigth = 0
        self.top_position = 0
        self.base_position = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.BASE_PIPE = PIPE_IMAGE
        self.passed_pipe = False
        self.set_heigth()

    def set_heigth(self):
        self.heigth = random.randrange(50, 450)
        self.base_position = self.heigth - self.TOP_PIPE.get_height()
        self.base_position = self.heigth + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, view):
        view.blit(self.TOP_PIPE, (self.x, self.top_position))
        view.blit(self.BASE_PIPE, (self.x, self.base_position))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)

        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        base_distance = (self.x - bird.x, self.base_position - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        base_point = bird_mask.overlap(base_mask, base_distance)

        if base_point or top_point:
            return True
        else:
            return False


class Background:
    SPEED = 5
    WIDTH = BACKGROUND_IMAGE.get_width()
    IMAGE = BACKGROUND_IMAGE

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH

    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        if self.x0 + self.WIDTH < 0:
            self.x0 = self.x1 + self.WIDTH
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x0 + self.WIDTH

    def draw(self, view):
        view.blit(self.IMAGE, (self.x0, self.y))
        view.blit(self.IMAGE, (self.x1, self.y))
