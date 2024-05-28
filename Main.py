import sys
import time
import numpy as np
import pygame
import pyopencl as cl
from Quaternion import quaternion
from Vector3D import v3d
from Window import Window

width, height = 800, 600

# cl init
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

# build program
kernels = ''.join(open('./cl/redify.cl', 'r', encoding='utf-8').readlines())
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
  t = time.time()
  evt = prg.redify(queue, (win.w, win.h), None, win.IMGbuf, win.writeIMG)
  evt.wait()
  print(time.time()-t)
  t = time.time()
  win.IMGbuf = win.writeIMG
  print(time.time() - t)
  t = time.time()
  win.updateWIN()
  print(f"{time.time()-t}\n")

  clock.tick(60)