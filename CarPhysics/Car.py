import math
import pygame
from CarPhysics.geomery_methods import *
import gym
from gym import spaces
from gym.utils import seeding
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Car():
    def __init__(self):
        self.x, self.y = 180, 265
        self.vel = 0
        self.direction = [1, 0]
        self.direction = rotate(self.direction, -5)
        self.acc = 0
        self.width = 20
        self.height = 15
        self.turningRate = 2.2 / self.width
        self.friction = 0.99
        self.maxSpeed = self.width / 2.2
        self.maxReverseSpeed = -1 * self.maxSpeed / 9
        self.accelerationSpeed = self.width / 1060.0
        self.driftMomentum = 0
        self.driftFriction = 0.87
        self.lineCollisionPoints = []
        self.collisionLineDistances = []
        self.vectorLength = 300
        self.StartDrift = 0.5
        self.DriftAmountConst = self.width / (9.0 * 7.0) * 1.6

        self.carPic = None

        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False



    def move(self):
        multiplier = 1
        if abs(self.vel) < 5:
            multiplier = abs(self.vel) / 5
        if self.vel < 0:
            multiplier *= -1

        if self.vel < self.StartDrift:
            driftAmount = 0
        else:
            driftAmount = self.vel * self.turningRate * self.DriftAmountConst

        if self.turningLeft:
            self.direction = rotate(self.direction, 180 / math.pi * self.turningRate * multiplier)
            self.driftMomentum -= driftAmount
        elif self.turningRight:
            self.direction = rotate(self.direction, -180 / math.pi * self.turningRate * multiplier)
            self.driftMomentum += driftAmount
        self.acc = 0
        if self.accelerating:
            if self.vel < 0:
                self.acc = 3 * self.accelerationSpeed
            else:
                self.acc = self.accelerationSpeed
        elif self.reversing:
            if self.vel > 0:
                self.acc = -3 * self.accelerationSpeed
            else:
                self.acc = -1 * self.accelerationSpeed

        self.vel += self.acc * (1.2 - abs(self.vel / self.maxSpeed))
        self.vel *= self.friction
        if self.maxSpeed < self.vel:
            self.vel = self.maxSpeed
        elif self.vel < self.maxReverseSpeed:
            self.vel = self.maxReverseSpeed

        addVector = [0, 0]

        addVector[0] += self.vel * self.direction[0]
        addVector[0] += self.driftMomentum * (- self.direction[1])
        addVector[1] += self.vel * self.direction[1]
        addVector[1] += self.driftMomentum * self.direction[0]
        self.driftMomentum *= self.driftFriction

        self.x += addVector[0]
        self.y += addVector[1]


    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.carPic, -get_angle(self.direction) - 90)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))

        screen.blit(rotated_image, new_rect)


    def reset(self):
        self.done = False
        self.x, self.y = (180, 265)
        self.vel = 0
        self.direction = [1, 0]
        self.acc = 0
        self.reward = 0




    def not_cross_wall(self):
        track_in = self.track_in
        track_out = self.track_out
        polygon_in = Polygon(track_in)
        polygon_out = Polygon(track_out)
        for x, y in [(self.x + (self.width / 2 - 3) * self.direction[0] + (self.height / 2 - 3) * self.direction[1],
                      self.y + (self.width / 2 - 3) * self.direction[1] - (self.height / 2 - 3) * self.direction[0]),
                     (self.x - (self.width / 2 - 3) * self.direction[0] - (self.height / 2 - 3) * self.direction[1],
                      self.y - (self.width / 2 - 3) * self.direction[1] + (self.height / 2 - 3) * self.direction[0]),
                     (self.x + (self.width / 2 - 3) * self.direction[0] + (self.height / 2 - 3) * self.direction[1],
                      self.y + (self.width / 2 - 3) * self.direction[1] - (self.height / 2 - 3) * self.direction[0]),
                     (self.x - (self.width / 2 - 3) * self.direction[0] + (self.height / 2 - 3) * self.direction[1],
                      self.y - (self.width / 2 - 3) * self.direction[1] - (self.height / 2 - 3) * self.direction[0])
                     ]:
            point = Point(x, y)
            in_in = polygon_in.contains(point)
            if in_in:
                return False
            in_out = polygon_out.contains(point)
            if not in_out:
                return False

        return True








class UserCar(Car):
    def __init__(self):
        Car.__init__(self)

        self.carPic = pygame.image.load('Assets/usercar.png')
        self.carPic = pygame.transform.scale(self.carPic, (self.height, self.width))


    def updateWithUser(self, wasd_list):
        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False

        (self.accelerating, self.turningLeft, self.reversing, self.turningRight) = wasd_list




class BotCar(Car):
    def __init__(self):
        Car.__init__(self)


        self.track_out = [(89, 260), (98, 156), (147, 107), (857, 85), (915, 113), (944, 183), (962, 578), (940, 621), (902, 638), (834, 614), (713, 462), (648, 450), (518, 478), (457, 597), (404, 626), (345, 625), (302, 584), (260, 349), (243, 312), (205, 307), (111, 304)]
        self.track_in = [(151, 239), (154, 175), (169, 160), (828, 138), (868, 150), (891, 211), (915, 538), (908, 566), (865, 571), (793, 461), (703, 396), (590, 394), (503, 427), (422, 550), (396, 569), (365, 571), (335, 477), (316, 302), (269, 261)]
        self.track_score = [(297, 119), (156, 127), (109, 160), (104, 250), (123, 290), (283, 288), (302, 320), (324, 589), (378, 610), (452, 583), (509, 439), (599, 412), (699, 412), (840, 602), (903, 622), (949, 580), (924, 177), (899, 121), (839, 94)]

        self.dead = False
        self.now_iteration = 0
        self.max_iteration = 150
        self.last_score = 19

        self.carPic = pygame.image.load('Assets/botcar.png')
        self.carPic = pygame.transform.scale(self.carPic, (self.height, self.width))

    def cross_wall_reaction(self):
        if not self.not_cross_wall():
            self.dead = True

    def step(self, action):

        self.updateWithAction(action)
        self.move()
        #self.reward = score_distanse((self.x, self.y), self.track_score)[0] - 390
        self.cross_wall_reaction()
        #state = self.get_state()
        #return state #, self.reward, self.done, {}

        self.now_iteration += 1
        now_score = (score_distanse((self.x, self.y), self.track_score)[0]) // 20 % 135
        if now_score == 134:
            self.last_score = 0
        if 0 < now_score - self.last_score <= 5:
            self.max_iteration += ((now_score - self.last_score) % 132) * (12 - 0.0025 * self.now_iteration)
            self.last_score = now_score
        if self.max_iteration < self.now_iteration:
            self.dead = True


    def get_state(self):
        track_in = self.track_in
        track_out = self.track_out
        #print(first_intersection((self.x, self.y), rotate(self.direction, 0.5), track_out, track_in))
        d_0_1 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, 0.5), track_out, track_in))
        d_0_2 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, -0.5), track_out, track_in))
        tan_0 = 0.01745 * d_0_1 / (d_0_2 - d_0_1 + 0.00001)
        d_15_1 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, 15), track_out, track_in))
        d_15_2 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, -15), track_out, track_in))
        d_30_1 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, 30), track_out, track_in))
        d_30_2 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, -30), track_out, track_in))
        d_90_1 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, 90), track_out, track_in))
        d_90_2 = distanse((self.x, self.y), first_intersection((self.x, self.y), rotate(self.direction, -90), track_out, track_in))
        #score, number_of_line = score_distanse((self.x, self.y), track_score)
        #score_directoin = normalize(track_score[number_of_line][0] - track_score[number_of_line - 1][0], track_score[number_of_line][1] - track_score[number_of_line - 1][1])
        #score_directoin_cos = score_directoin[0] * self.direction[0] + score_directoin[1] * self.direction[1]

        return [self.vel, d_0_1, tan_0, d_15_1, d_15_2, d_30_1, d_30_2, d_90_1, d_90_2]


    def updateWithAction(self, actionNo):
        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False

        if actionNo == 0:
            self.turningLeft = True
        elif actionNo == 1:
            self.turningRight = True
        elif actionNo == 2:
            self.accelerating = True
        elif actionNo == 3:
            self.reversing = True
        elif actionNo == 4:
            self.accelerating = True
            self.turningLeft = True
        elif actionNo == 5:
            self.accelerating = True
            self.turningRight = True
        elif actionNo == 6:
            self.reversing = True
            self.turningLeft = True
        elif actionNo == 7:
            self.reversing = True
            self.turningRight = True
        elif actionNo == 8:
            pass
