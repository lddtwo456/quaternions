import numpy as np
import pygame
import sys

class Window:
  def __init__(self, width, height):
    self.w = width
    self.h = height

    self.IMG = np.zeros((width, height, 3), dtype=np.uint8, order='C')
    self.WIN = pygame.display.set_mode((width, height))

  def updateWIN(self):
    print(self.IMG[0][0][0])
    SURF = pygame.surfarray.make_surface(self.IMG)
    self.WIN.blit(SURF, (0,0))
    pygame.display.flip()

  def clearIMG(self):
    self.IMG = np.zeros((self.w, self.h, 3), dtype=np.uint8, order='C')

  def getIMG(self):
    return self.IMG
  
  def setIMG(self, img):
    self.IMG = img