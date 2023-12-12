import math
import pygame


def rotate(vec, angle):
    angle = angle * math.pi / 180
    vec = [vec[0] * math.cos(angle) - vec[1] * math.sin(angle), vec[0] * math.sin(angle) + vec[1] * math.cos(angle)]
    return vec


def get_angle(vec):
    if vec[0] ** 2 + vec[1] ** 2 == 0:
        return 0
    return math.degrees(math.atan2(vec[1], vec[0]))


class Car:

    def __init__(self):
        self.x = 258
        self.y = 288
        self.vel = 0
        self.direction = [0, 1]
        self.direction = rotate(self.direction, 180 / 12)
        self.acc = 0
        self.width = 20
        self.height = 15
        self.turningRate = 2.2 / self.width
        self.friction = 0.99
        self.maxSpeed = self.width / 2.2
        self.maxReverseSpeed = -1 * self.maxSpeed / 9
        self.accelerationSpeed = self.width / 1060.0
        self.dead = False
        self.driftMomentum = 0
        self.driftFriction = 0.87
        self.lineCollisionPoints = []
        self.collisionLineDistances = []
        self.vectorLength = 300
        self.StartDrift = 0.5
        self.DriftAmountConst = self.width / (9.0 * 7.0) * 1.4

        self.carPic = None

        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False

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

    def updateWithUser(self, wasd_list):
        self.turningLeft = False
        self.turningRight = False
        self.accelerating = False
        self.reversing = False

        (self.accelerating, self.turningLeft, self.reversing, self.turningRight) = wasd_list

    def move(self):
        global vec2
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

    def updateControls(self):
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

    def draw(self, screen):
        if not bool(self.carPic):
            self.carPic = pygame.image.load('car.png')
            self.carPic = pygame.transform.scale(self.carPic, (self.height, self.width))
        rotated_image = pygame.transform.rotate(self.carPic, -get_angle(self.direction) - 90)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))

        screen.blit(rotated_image, new_rect)
