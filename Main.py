import sys
import time
import numpy as np
import pygame
import pyopencl as cl
from Quaternion import quaternion
from Vector3D import v3d
from Window import Window

width, height = 1280, 720

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

test = True
if test:
  def recordTime(label):
    times_per_loop.update({label : time.time()})
  def addTimes(loopNum):
    times.append(dict(times_per_loop))
    loopNum += 1
    times_per_loop.clear()
else:
  def recordTime(label):
    pass
  def addTimes(label):
    pass

# main run loop

def runLoop(run, loopNum, clockmult):
  recordTime("start")
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      pygame.quit()
      sys.exit()

  # execute code
  evt = prg.redify(queue, (win.w, win.h), None, win.IMGbuf, win.writeIMG, np.uint32(time.time()))
  evt.wait()
  recordTime("redify")

  win.IMGbuf = win.writeIMG
  recordTime("update image buffer")
  win.updateWIN()
  recordTime("update window")

  clock.tick(60*clockmult)
  recordTime("end frame")
  addTimes(loopNum)

if test:
  for i in range(int(input("test loops: "))):
    runLoop(True, 0, 10)

  # calculate and print average times
  for loop_times in times:
    keys = []
    for key in loop_times:
      keys.append(key)

    for i in range(len(keys)):
      if i + 1 < len(keys):
        loop_times[keys[len(keys)-i-1]] -= loop_times[keys[len(keys)-i-2]]
    
    loop_times.pop("start")

  averages = {}
  for key in times[0]:
    n = 0
    for loop_times in times:
      n += loop_times[key]
    
    n /= len(times)
    averages.update({key : n})

  print('')
  
  total = 0
  max_key_len = max(max(len(key) for key in averages), len("total frame time"))
  for key in averages:
    val = averages[key]
    total += val
    print(f"{key.ljust(max_key_len)} - {int(val*100000)/100000}")
  
  print('')
  print(f"{"total frame time".ljust(max_key_len)} - {int(total*100000)/100000}")
  print(f"    FPS   =   {int(1/total*100000)/100000}")
  print('')
else:
  run = True
  while run:
    runLoop(run, None, 1)