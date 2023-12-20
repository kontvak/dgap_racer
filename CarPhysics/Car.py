import ast
import pygame
from CarPhysics.geomery_methods import *
from geomery_methods import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


file = open('Assets/track0.txt', 'r')
track_out = ast.literal_eval(next(file))
track_in = ast.literal_eval(next(file))
track_score = ast.literal_eval(next(file))
file.close()

class Car():
    def __init__(self, start=(180, 265)):
        self.x, self.y = start
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
        """
        Двигает машину
        """
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
        """
        Отрисовка
        :param screen: экран
        """
        rotated_image = pygame.transform.rotate(self.carPic, -get_angle(self.direction) - 90)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect)

    def not_cross_wall(self):
        """
        Проверяет пересечение со стенами
        """
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
    def __init__(self, start=False):
        if not start:
            Car.__init__(self)
        else:
            Car.__init__(self, start)

        self.carPic = pygame.image.load('Assets/usercar.png')
        self.carPic = pygame.transform.scale(self.carPic, (self.height, self.width))

    def updateWithUser(self, wasd_list):
        """
        Применяет двействия с клавиатуры
        :param wasd_list: нажатие клавиш
        """
        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False

        (self.accelerating, self.turningLeft, self.reversing, self.turningRight) = wasd_list

    def cross_wall_reaction(self):
        """
        Двействие в случае пересечения границы
        """
        if not self.not_cross_wall():
            self.vel *= 0.97


class BotCar(Car):
    def __init__(self, start=False):
        if not start:
            Car.__init__(self)
        else:
            Car.__init__(self, start)

        self.dead = False
        self.now_iteration = 0
        self.max_iteration = 150
        self.last_score = 19

        self.carPic = pygame.image.load('Assets/botcar.png')
        self.carPic = pygame.transform.scale(self.carPic, (self.height, self.width))

    def cross_wall_reaction(self):
        """
        Двействие в случае пересечения границы
        """
        if not self.not_cross_wall():
            self.dead = True

    def step(self, action):
        """
        Примененяет action и обновляет положение и self.max_iteration для обучения
        """
        #global track_score
        self.updateWithAction(action)
        self.move()
        self.cross_wall_reaction()

        self.now_iteration += 1
        now_score = (score_distanse((self.x, self.y), track_score)[0]) // 20 % 135
        if now_score == 134:
            self.last_score = 0
        if 0 < now_score - self.last_score <= 5:
            self.max_iteration += ((now_score - self.last_score) % 132) * (12 - 0.0025 * self.now_iteration)
            self.last_score = now_score
        if self.max_iteration < self.now_iteration:
            self.dead = True


    def get_state(self):
        """
        Параметры для обучения
        """
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
        """
        Применяет действие из его номера
        """
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
