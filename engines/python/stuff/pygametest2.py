import os
import pygame
import time
os.environ["SDL_FBDEV"] = "/dev/fb0"
os.putenv("SDL_VIDEODRIVER", "kmsdrm")
os.putenv("SDL_FBDEV" , "/dev/fb0")

pygame.init()
display = pygame.display.set_mode((0, 0))
print(pygame.display.get_driver())
display.fill((0,0,0))
pygame.display.update()
pygame.draw.line(display, (30,80,200),[100,100],[200,200],2);
pygame.display.update()
time.sleep(5)
