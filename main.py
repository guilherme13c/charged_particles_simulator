import pygame, os, sys
import random
from pygame.locals import *

#Definition of classes
class Point:
  def __init__(self, color:pygame.Color, x:int, y:int, charge:int):
    self.color = color
    self.radius = 4
    self.velocity = [0, 0]
    self.pos = [x, y]
    self.charge = charge
    self.trace = []

  #Definition of methods
  def draw(self):
    pygame.draw.circle(screen, self.color, self.pos, self.radius)

pygame.init()
pygame.event.set_allowed([QUIT])

os.environ['SDL_VIDEO_WINDOW_POS'] = '1'

#Definition of screen settings
WIDTH = 1200
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.set_alpha(None)

#Definition of colors
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
GREY = pygame.Color(200,200,200)
RED = pygame.Color(255,0,0)
BLUE = pygame.Color(0,0,255)

FPS = 60
clock = pygame.time.Clock()

screen.fill(GREY)
points = []

K = 2
MASS = 1
MAX_VELOCITY = FPS * 0.8

#Needed Liner Algebra functions
def calculateDisplacementVector(p1:Point, p2:Point):
  return [p1.pos[0]-p2.pos[0], p1.pos[1]-p2.pos[1]]

def calculateVectorNorm(vect:list):
  r = (vect[0]**2+vect[1]**2)**(1/2)
  return r

def calculateElectricForceValue(p1:Point, p2:Point):
  d = calculateVectorNorm(calculateDisplacementVector(p1,p2))

  if d == 0:    #this conditional avoids division by zero errors
    d = 0.0001

  return (K*p1.charge*p2.charge)/(d**2)

#Game Loop
while True:
  screen.fill(GREY)

  #store and draw trace
  for point1 in points:
    point1.trace.append([int(point1.pos[0]), int(point1.pos[1])])
    if len(point1.trace) > 100:
      point1.trace.pop(0)

    if (point1.pos[0]+point1.velocity[0] > WIDTH) or (point1.pos[0]+point1.velocity[0] < 0):
      point1.velocity[0] = -0.8*point1.velocity[0]
    if (point1.pos[1]+point1.velocity[1] > HEIGHT) or (point1.pos[1]+point1.velocity[1] < 0):
      point1.velocity[1] = -0.8*point1.velocity[1]

    point1.pos[0] += point1.velocity[0]
    point1.pos[1] += point1.velocity[1]

    if point1.velocity[0] > MAX_VELOCITY:
      point1.velocity[0] = MAX_VELOCITY
    if point1.velocity[1] > MAX_VELOCITY:
      point1.velocity[1] = MAX_VELOCITY

    if len(point1.trace) >= 2:
      pygame.draw.lines(screen, point1.color, False, point1.trace, 1)
    point1.draw()

    #calculate and update velocity
    for point2 in points:
      if point2 != point1:
        forceVal = calculateElectricForceValue(point1, point2)
        direction = calculateDisplacementVector(point1, point2)
        directionNorm = calculateVectorNorm(direction)
        if directionNorm < 1:
          directionNorm = 1

        directionNormalized = direction[0]/directionNorm, direction[1]/directionNorm

        point1.velocity[0] += directionNormalized[0]*forceVal/MASS
        point1.velocity[1] += directionNormalized[1]*forceVal/MASS

        #impact detection and trajectory update
        if (calculateVectorNorm(calculateDisplacementVector(point1, point2))-point1.radius-point2.radius <= 0):
          impactDirection = [0, 0]
          impactDirection[0] = calculateDisplacementVector(point1, point2)[0]/calculateVectorNorm(calculateDisplacementVector(point1, point2))
          impactDirection[1] = calculateDisplacementVector(point1, point2)[1]/calculateVectorNorm(calculateDisplacementVector(point1, point2))

          point1.velocity[0] *= -0.9*impactDirection[0]
          point1.velocity[1] *= -0.9*impactDirection[1]

          point2.velocity[0] *= 0.9*impactDirection[0]
          point2.velocity[1] *= 0.9*impactDirection[1]

  #Input detection/receiving
  for event in pygame.event.get():
    if (event.type == QUIT):
      pygame.quit()
      sys.exit()
    elif (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
      elif (event.key == pygame.K_SPACE):
        seed = random.random()
        if (seed > 0.5):
          newPoint = Point(RED , random.randint(0, WIDTH), random.randint(0, HEIGHT), +10)
        else:
          newPoint = Point(BLUE , random.randint(0, WIDTH), random.randint(0, HEIGHT), -10)
        points.append(newPoint)
    else:
      mouse_button = pygame.mouse.get_pressed()
      if (mouse_button[0]):
        newPoint = Point(BLUE, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], -10)
        points.append(newPoint)
      if (mouse_button[2]):
        newPoint = Point(RED , pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], +10)
        points.append(newPoint)  

  #screen updating
  pygame.display.update()
  clock.tick(FPS)
