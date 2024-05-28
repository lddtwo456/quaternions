import numpy as np
import pyopencl as cl
import pygame
import sys

class Window:
  def __init__(self, width, height, ctx, queue):
    self.w = width
    self.h = height

    img_form = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNSIGNED_INT8)
    self.IMGbuf = cl.Image(ctx, cl.mem_flags.READ_WRITE, img_form, shape=(width, height))

    self.writeIMG = cl.Image(ctx, cl.mem_flags.READ_WRITE, img_form, shape=(width, height))

    self.WIN = pygame.display.set_mode((width, height))

    self.ctx = ctx
    self.queue = queue

  def updateWIN(self):
    data_out = np.empty((self.h, self.w, 4), dtype=np.uint8)
    cl.enqueue_copy(self.queue, data_out, self.IMGbuf, origin=(0,0,0), region=(self.w,self.h, 1))
    data_out = data_out.swapaxes(0, 1)

    SURF = pygame.surfarray.make_surface(data_out[:,:,:3])
    self.WIN.blit(SURF, (0,0))
    pygame.display.flip()

  def getIMGbuf(self):
    return self.IMGbuf
  
  def setIMGbuf(self, imgbuf):
    self.IMGbuf = imgbuf