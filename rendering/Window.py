import numpy as np
import pyopencl as cl
import pygame
import sys

from rendering.Renderer import Renderer

class Window:
  def __init__(self, width, height, ctx, queue):
    self.w = width
    self.h = height

    img_form = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNSIGNED_INT8)
    self.IMGbuf = cl.Image(ctx, cl.mem_flags.READ_WRITE, img_form, shape=(width, height))

    self.writeIMG = cl.Image(ctx, cl.mem_flags.READ_WRITE, img_form, shape=(width, height))
    self.data_out = np.empty((self.h, self.w, 4), dtype=np.uint8)

    self.WIN = pygame.display.set_mode((width, height))

    self.ctx = ctx
    self.queue = queue

  def updateWIN(self):
    Renderer.renderScene(self.IMGbuf)
  
    cl.enqueue_copy(self.queue, self.data_out, self.IMGbuf, origin=(0,0,0), region=(self.w,self.h, 1))
    pygame.surfarray.blit_array(self.WIN, self.data_out[:,:,:3].swapaxes(0, 1))
    pygame.display.flip()

  def getIMGbuf(self):
    return self.IMGbuf
  
  def setIMGbuf(self, imgbuf):
    self.IMGbuf = imgbuf