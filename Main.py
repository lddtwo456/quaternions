import sys
import time
import numpy as np
import pygame
import pyopencl as cl
from Quaternion import quaternion
from Vector3D import v3d
from Window import Window

p = v3d(2, 2, 2)
q = quaternion.fromEulerDeg(v3d(90, 0, 0))

print(q)

v = v3d(2, 3, 5)

print(q.applyToPoint(p))

print(cl.VERSION)

# this is going to be hell
width, height = 800, 600

# cl init
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

# build program
kernels = ''.join(open('./cl/redderfier.cl', 'r', encoding='utf-8').readlines())
prg = cl.Program(ctx, kernels).build()

# pygame init 
pygame.init()
win = Window(width, height, ctx, queue)
clock = pygame.time.Clock()

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      pygame.quit()
      sys.exit()

  # execute code
  evt = prg.redify(queue, (win.w, win.h), None, win.IMGbuf, win.writeIMG)
  evt.wait()
  win.IMGbuf = win.writeIMG

  win.updateWIN()
  clock.tick(60)