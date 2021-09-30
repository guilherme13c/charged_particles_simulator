import pygame, os, sys
import random
from pygame.locals import *

class Point:
  def __init__(self, color:pygame.Color, x:int, y:int, charge:int):
    self.color = color
    self.radius = 4
    self.velocity = [0, 0]
    self.pos = [x, y]
    self.charge = charge

  def draw(self):
    pygame.draw.circle(screen, self.color, self.pos, self.radius)

pygame.init()
pygame.event.set_allowed([QUIT])

os.environ['SDL_VIDEO_WINDOW_POS'] = '1'

#Definition of screen settings
WIDTH = 1200
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT], DOUBLEBUF)
screen.set_alpha(None)

#Definition of colors
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
GREY = pygame.Color(200,200,200)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

FPS = 100
clock = pygame.time.Clock()

screen.fill(GREY)
points = []

K=0.6
MAX_VELOCITY = FPS - 10

#Needed functions
def calculateDisplacementVector(p1:Point, p2:Point):
  return [p1.pos[0]-p2.pos[0], p1.pos[1]-p2.pos[1]]

def calculateVectorNorm(vect:list):
  return int((vect[0]**2+vect[1]**2)**(1/2))

def calculateElectricForceValue(p1:Point, p2:Point):
  d = calculateVectorNorm(calculateDisplacementVector(p1,p2))
  if d == 0:
    d = 0.001

  return (K*p1.charge*p2.charge)/(d**2)

#Game Loop
while True:
  screen.fill(GREY)

  for point1 in points:
    if (point1.pos[0]+point1.velocity[0] > WIDTH) or (point1.pos[0]+point1.velocity[0] < 0):
      point1.velocity[0] = -point1.velocity[0]
    if (point1.pos[1]+point1.velocity[1] > HEIGHT) or (point1.pos[1]+point1.velocity[1] < 0):
      point1.velocity[1] = -point1.velocity[1]

    point1.pos[0] += point1.velocity[0]
    point1.pos[1] += point1.velocity[1]
    if point1.velocity[0] > MAX_VELOCITY:
      point1.velocity[0] = MAX_VELOCITY
    if point1.velocity[1] > MAX_VELOCITY:
      point1.velocity[1] = MAX_VELOCITY

    point1.draw()

    for point2 in points:
      if point2 != point1:
        forceVal = calculateElectricForceValue(point1, point2)
        direction = calculateDisplacementVector(point1, point2)
        directionNorm = calculateVectorNorm(direction)
        if directionNorm < 1:
          directionNorm = 1

        directionNormalized = direction[0]/directionNorm, direction[1]/directionNorm

        point1.velocity[0] += directionNormalized[0]*forceVal
        point1.velocity[1] += directionNormalized[1]*forceVal

  for event in pygame.event.get():
    if (event.type == QUIT):
      pygame.quit()
      sys.exit()
    elif (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
    else:
      mouse_button = pygame.mouse.get_pressed()
      if (mouse_button[0]):
        newPoint = Point(BLUE, random.randint(0, WIDTH), random.randint(0, HEIGHT), -3)
        points.append(newPoint)
      if (mouse_button[2]):
        newPoint = Point(RED , random.randint(0, WIDTH), random.randint(0, HEIGHT), +3)
        points.append(newPoint)

  pygame.display.update()
  clock.tick(FPS)