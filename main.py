import pygame
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from Car import *

import pyglet

FPS = 60
#track = [(187, 300), (188, 256), (220, 208), (292, 173), (440, 143), (550, 109), (668, 69), (730, 55), (787, 65), (866, 113), (907, 179), (916, 274), (930, 360), (912, 460), (888, 498), (818, 549), (752, 570), (645, 566), (532, 558), (439, 504), (383, 464), (295, 406), (221, 373), (187, 300), (274, 274), (273, 301), (292, 342), (339, 364), (391, 389), (447, 424), (518, 461), (620, 494), (740, 496), (828, 460), (860, 396), (856, 305), (845, 229), (791, 163), (742, 132), (656, 131), (566, 156), (459, 185), (380, 198), (318, 214), (279, 233), (274, 274)]
track = [(176, 279), (144, 223), (141, 149), (181, 101), (233, 73), (296, 68), (374, 91), (408, 133), (433, 192), (460, 206), (794, 199), (881, 204), (905, 227), (913, 256), (904, 299), (868, 312), (496, 322), (464, 358), (444, 381), (394, 411), (324, 424), (253, 425), (208, 408), (157, 379), (127, 336), (151, 304), (176, 279), (221, 219), (205, 182), (233, 142), (273, 131), (313, 133), (345, 156), (360, 189), (368, 221), (375, 242), (399, 244), (461, 251), (517, 249), (812, 247), (849, 246), (861, 262), (847, 275), (529, 277), (462, 278), (433, 304), (390, 341), (338, 365), (271, 369), (225, 352), (191, 341), (218, 309), (236, 272), (221, 219)]

track_geom = Polygon(track)
#track_geom.contains(point)
wasd_keys = {repr([False, True, False, False]): 0, repr([False, False, False, True]): 1,
             repr([True, False, False, False]): 2, repr([False, False, True, False]): 3,
             repr([True, True, False, False]): 4, repr([True, False, False, True]): 5,
             repr([False, True, True, False]): 6, repr([False, False, True, True]): 7,
             repr([False, False, False, False]): 8, repr([True, True, False, True]): 2,
             repr([True, True, True, False]): 0, repr([True, False, True, True]): 1,
             repr([False, True, False, True]): 8
             }

run = True
pygame.init()
pygame.display.set_caption("car game")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1080, 720), 0, 32)
car1 = Car()
while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    pygame.draw.polygon(screen, (25, 25, 25), track)
    car1.draw(screen)

    keys = pygame.key.get_pressed()
    wasd = [keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_a]]


    car1.updateWithAction(wasd_keys[repr(wasd)])
    car1.updateControls()
    car1.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break



    pygame.display.update()
pygame.quit()
