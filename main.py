import pygame as pg
import sys
from settings import *
from objects import *
from os import path
import json
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game

        with open("bodies/vine1.txt", "r") as json_file:
            my_dict = json.load(json_file)
        self.particles = []
        self.springs = []
        self.grounded = []
         # center
        sum_vec = vec(0,0)
        for n, p in enumerate(my_dict["points"]):
            sum_vec+=vec(p)*my_dict['scale']
            particle = Particle(vec(p)*my_dict['scale'],10)
            if n in my_dict["grounded"]:
                particle.locked = True
                self.grounded.append(particle)
            self.particles.append(particle)

        center_vec = sum_vec.copy()/len(my_dict["points"])
        self.offsets_for_base = []
        for p in self.grounded:
            self.offsets_for_base.append(p.pos-center_vec)



        for con in my_dict["connections"]:
            self.springs.append(Spring(self.particles[con[0]],self.particles[con[1]], 0.1, 30))
        # for i in range(5):
        #     self.particles.append(Particle((WIDTH//2,i*50),15))
        # for i in range(len(self.particles)):
        #     if i != 0:
        #         self.springs.append(Spring(self.particles[i-1],self.particles[i], 0.01, 50))





    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        for p in self.particles:
            p.apply_force(vec(0,0.01))
            p.update(self.dt)

        for s in self.springs:
            s.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        #self.all_sprites.draw(self.screen)
        for p in self.particles:
            p.draw(self.screen)

        for s in self.springs:
            s.draw(self.screen)

        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        if pg.mouse.get_pressed()[0]:
            for n, p in enumerate(self.grounded):
                p.pos = vec(pg.mouse.get_pos()) + self.offsets_for_base[n]
                p.vel *= 0
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                



# create the game object
g = Game()
g.new()
g.run()
