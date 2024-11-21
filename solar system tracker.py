import solarsystem as sol
import datetime
import pygame
import math
import sys
import random

SCRW = 1000
SCRH = 800

pygame.init()
SCREEN = pygame.display.set_mode((SCRW,SCRH))
pygame.display.set_caption("Planet tracker")
clock = pygame.time.Clock()

class Info:
    def __init__(self):
        self.H = None
        self.planets = None
        self.min = 0
        self.stars = []

        self.lastStar = 0

        for i in range(100):
            self.make_star(corner=False)

        self.imgs = []
        for i in range(8):
            self.imgs.append(pygame.image.load(f"planet{i + 1}.png"))

        self.names = ["Mercury",
                      "Venus",
                      "Earth",
                      "Mars",
                      "Jupiter",
                      "Saturn",
                      "Uranus",
                      "Neptune"]

    def make_star(self,corner=True):
        x = 0 if corner else random.randint(0,SCRW)
        brightness = random.randint(100,255)
        self.stars.append(
                    {"pos":[x,random.randint(0,SCRH)],
                    "speed":random.randint(1,5),
                    "brighness":(brightness,brightness,brightness),
                    "size":random.randint(1,3)})

    def tick_stars(self):
        if pygame.time.get_ticks() - self.lastStar > 3000:
            self.lastStar = pygame.time.get_ticks()
            self.make_star()

        for item in self.stars:
            item["pos"][0] += item["speed"]/100
            if item["pos"][0] > SCRW:
                self.stars.remove(item)

    def tick(self):
        self.min += 1/3600
        time = str(datetime.datetime.now())
        self.H = sol.Heliocentric(year=int(time[0:4]), month=int(time[5:7]),
                             day=int(time[8:10]), hour=int(time[11:13]),minute=self.min)
        self.planets = self.H.planets()

    def get_dists(self, angle, radius):
        vert = radius * math.sin(math.radians(angle))
        horz = radius * math.cos(math.radians(angle))
        return vert, horz

    def draw(self):
        for item in self.stars:
            pygame.draw.circle(SCREEN,item["brighness"],item["pos"],item["size"])

        pygame.draw.circle(SCREEN,(255,220,0),(SCRW//2,SCRH//2),50)
        idx = 0
        for i in range(8):
            #print(self.planets[self.names[idx]][1])
            dists = self.get_dists(self.planets[self.names[idx]][0],(idx+1.5)*45)
            self.blit_to_center(self.imgs[idx], (dists[0] + SCRW//2,dists[1] + SCRH//2))
            idx += 1

    def blit_to_center(self,img,pos):
        SCREEN.blit(img, (pos[0] -img.get_width()//2,
                    pos[1] - img.get_height()//2))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

info = Info()

while True:
    pygame.display.flip()
    SCREEN.fill((0,0,0))
    handle_events()
    clock.tick(60)

    info.tick_stars()
    info.tick()
    info.draw()