import pygame
import os
import sys
import ast

import neat
import pickle

from CarPhysics.Car import *


FPS = 60
screen_width = 1080
screen_height = 720
BACK_COLOR = (0, 0, 0)
TRACK_COLOR = (25, 25, 25)

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


def remove(index):
    """Удалить машину из выборки"""
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)


def eval_genomes(genomes, config):
    """Итерация обучения"""
    global cars, ge, nets
    cars = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        cars.append(BotCar())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        screen.fill(BACK_COLOR)
        pygame.draw.polygon(screen, TRACK_COLOR, track_out)
        pygame.draw.polygon(screen, BACK_COLOR, track_in)

        if len(cars) == 0:
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if car.dead:
                remove(i)

        action = []
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_state())
            action.append(max(enumerate(output),key=lambda x: x[1])[0])

        # Update
        for i in range(len(cars)):
            cars[i].draw(screen)
            cars[i].step(action[i])
        pygame.display.update()


# Setup NEAT Neural Network
def run_neat(config_path):
    """Обучение"""
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes, 2)
    pickle.dump(winner, open('learning/winner.pkl', 'wb'))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'learning/config.txt')
    run_neat(config_path)
