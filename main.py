import os
import ast
import pygame

import pickle
import neat

from CarPhysics.Car import *


FPS = 60
screen_width = 1080
screen_height = 720
BACK_COLOR = (0, 0, 0)
TRACK_COLOR = (25, 25, 25)
RED_COLOR = (205, 0, 55)

file = open('Assets/track0.txt', 'r')
track_out = ast.literal_eval(next(file))
track_in = ast.literal_eval(next(file))
track_score = ast.literal_eval(next(file))
file.close()

run = True
pygame.init()
pygame.display.set_caption("racist")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
car1 = BotCar()
car2 = UserCar((180, 285))

winner = pickle.load(open("learning/winner1.pkl", "rb"))
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'learning/config.txt')
config = neat.config.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path
)
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

clock = pygame.time.Clock()
counter, text = 5, '5'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 500)
font = pygame.font.SysFont('Consolas', 30)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            counter -= 1
            if counter > 0:
                text = str(counter).rjust(3)
            else:
                run = False
        if event.type == pygame.QUIT:
            run = False

    screen.fill(BACK_COLOR)
    pygame.draw.polygon(screen, TRACK_COLOR, track_out)
    pygame.draw.polygon(screen, BACK_COLOR, track_in)
    pygame.draw.polygon(screen, RED_COLOR, track_out, 2)
    pygame.draw.polygon(screen, RED_COLOR, track_in, 2)
    car1.draw(screen)
    car2.draw(screen)
    screen.blit(font.render(text, True, (255, 255, 255)), (32, 48))
    pygame.display.flip()
    clock.tick(60)
run = True
while run:
    clock.tick(FPS)
    screen.fill(BACK_COLOR)
    pygame.draw.polygon(screen, TRACK_COLOR, track_out)
    pygame.draw.polygon(screen, BACK_COLOR, track_in)
    pygame.draw.polygon(screen, RED_COLOR, track_out, 2)
    pygame.draw.polygon(screen, RED_COLOR, track_in, 2)
    car1.draw(screen)
    car2.draw(screen)

    keys = pygame.key.get_pressed()
    wasd = (keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_a])

    car2.move()
    car2.updateWithUser(wasd)
    car2.cross_wall_reaction()

    car1.move()
    ac = winner_net.activate(car1.get_state())
    car1.updateWithAction(max(enumerate(ac),key=lambda x: x[1])[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    pygame.display.update()
pygame.quit()
