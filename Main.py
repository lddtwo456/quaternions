import sys
import time
import numpy as np
import pygame
import pyopencl as cl
from Camera import Camera
from ObjectsHandler import ObjectsHandler
from Quaternion import Quaternion
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
times_per_loop = {}
times = []
prev_time = 0

# object handler init
ObjectsHandler.init(ctx, queue)
objects = 1
for i in range(objects):
  ObjectsHandler.addObject(model="./Models/teapot.obj")
ObjectsHandler.buildBuffers()

cam = Camera()

# main run loop

def runLoop(run, clockmult):
  t = time.time()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      pygame.quit()
      sys.exit()

  # execute code
  evt = prg.redify(queue, (win.w, win.h), None, win.IMGbuf, win.writeIMG, np.uint32(time.time()))
  evt.wait()

  ObjectsHandler.getTransforms(cam)

  win.IMGbuf = win.writeIMG
  win.updateWIN()

  print(time.time()-t)
  clock.tick(60*clockmult)

run = True
while run:
  runLoop(run, 1)