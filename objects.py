import pygame as pg
from settings import *

vec = pg.Vector2
import math
def dist_vec(vec1, vec2):
    return math.sqrt((vec1.x-vec2.x)**2 + (vec1.y-vec2.y)**2)


class Particle:
    def __init__(self, pos, radius):
        self.vel = vec(0, 0)
        self.pos = vec(pos)
        self.acc = vec(0, 0)
        self.radius = radius
        self.mass = 1
        self.locked = False

    def update(self,dt):
        if not self.locked:
            self.vel *= 0.99
            self.vel += self.acc * dt * 50
            self.pos += self.vel * dt * 50
            self.acc *= 0

    def apply_force(self, force):
        f = force.copy()/self.mass
        self.acc += f

    def draw(self, surface):
        pg.draw.circle(surface, WHITE, self.pos, self.radius)

class Spring:
    def __init__(self, start, end, k, rest_length):
        self.start = start
        self.end = end
        self.k = k
        self.rest_length = rest_length

    def update(self):
        dir_vec = self.end.pos - self.start.pos
        dir_vec = dir_vec.normalize()

        force = dir_vec*(-1 * self.k * (dist_vec(self.start.pos,self.end.pos)-self.rest_length))

        self.end.apply_force(force)
        force *= -1
        self.start.apply_force(force)

    def draw(self, surf):
        pg.draw.line(surf, WHITE, self.start.pos, self.end.pos)



