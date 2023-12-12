import pygame
import time
from shapely.geometry import Point
import ast
from shapely.geometry.polygon import Polygon
from Car import *

import pyglet

FPS = 60
screen_width = 1080
screen_height = 720
BACK_COLOR = (0,0,0)
TRACK_COLOR = (25, 25, 25)

file = open('track0.txt', 'r')
track_out = ast.literal_eval(next(file))
track_in = ast.literal_eval(next(file))
file.close()
#track_geom = Polygon(track)
#track_geom.contains(point)

run = True
pygame.init()
pygame.display.set_caption("racist")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
car1 = Car()
while run:
    clock.tick(FPS)
    screen.fill(BACK_COLOR)
    pygame.draw.polygon(screen, TRACK_COLOR, track_out)
    pygame.draw.polygon(screen, BACK_COLOR, track_in)
    car1.draw(screen)

    keys = pygame.key.get_pressed()
    wasd = (keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_a])

    car1.updateWithUser(wasd)
    car1.updateControls()
    car1.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break



    pygame.display.update()
pygame.quit()
