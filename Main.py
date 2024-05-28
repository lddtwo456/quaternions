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

# pygame init 
pygame.init()
win = Window(width, height)
clock = pygame.time.Clock()

# cl init
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

# build program
kernels = ''.join(open('./cl/redderfier.cl', 'r', encoding='utf-8').readlines())
prg = cl.Program(ctx, kernels).build()

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      pygame.quit()
      sys.exit()
  
  t = time.time()
  # create image buffer
  img = win.getIMG()
  img_buffer = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, img.nbytes)
  cl.enqueue_copy(queue, img_buffer, np.ascontiguousarray(img))
  
  print(time.time() - t)

  # execute code
  evt = prg.redify(queue, (img.nbytes, ), (1, ), img_buffer)
  evt.wait()

  print(time.time() - t)

  # get result
  cl.enqueue_copy(queue, img, img_buffer)

  print(time.time() - t)

  win.setIMG(img)
  win.updateWIN()
  clock.tick(60)

  print(time.time() - t)
  print('')