import pygame
from pygame.locals import *
import ast


pygame.init()
screen = pygame.display.set_mode((1080, 720), 0, 32)
points = [[], []]
numb = 0
flag = True
while flag:

    for event in pygame.event.get():
        if event.type == QUIT:
            flag = False
        if event.type == MOUSEBUTTONDOWN:
            is_in = False
            for point in points[numb]:
                if (abs(event.pos[0] - point[0]) < 5) and (abs(event.pos[1] - point[1]) < 5):
                    if numb == 0:
                        print(points[numb])
                        numb += 1
                    else:
                        flag = False
                    print('bilo')
                    is_in = True
            if not is_in:
                points[numb].append(event.pos)


    screen.fill((255,255,255))

    if len(points[0]) >= 3:
        pygame.draw.polygon(screen, (0,255,0), points[0])
    if len(points[1]) >= 3:
        pygame.draw.polygon(screen, (255,255,255), points[1])
    for point in points[numb]:
        pygame.draw.circle(screen, (0,0,255), point, 2)

    pygame.display.update()
print(points[0] + [points[0][0]] + points[1] + [points[1][0]])
file = open('track.txt', 'w')
file.write(str(points[0]) + '\n' + str(points[1]))
file.close()
