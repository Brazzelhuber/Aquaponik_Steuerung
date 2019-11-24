

from __future__ import division, print_function
import pygame, pygame.gfxdraw       # pygame ist eigentlich für Spieleentwicklung. \
                                        # Aber auch geeigent um Grafikfenster zu steuern
from pygame.locals import *
import tkinter as Tk           # GUI-Bibliothek
import time

pygame.init()
##B = 1000
##H = 500
##pencere = pygame.display.set_mode((B,H))
##pygame.display.set_caption("Grafikfester")
##x= B
##y= H
##white = (255,255,255)
##Button_Farbe = (255,0,0)
##Button_Farbe2 = Button_Farbe
##pygame.font.get_fonts
##
##class Counter:
##    count = 0
##    def click(self):
##        self.count += 1
##
##number = Counter()
##def text_objects(text, font, color):
##    textSurface = font.render(text, True, color)
##    return textSurface, textSurface.get_rect()
##
##def button(msg,x,y,w,h,c,ic,action=None):
##    mouse = pygame.mouse.get_pos()
##    click = pygame.mouse.get_pressed()
##    pygame.draw.rect(pencere, c,(x,y,w,h))
##
##    smallText = pygame.font.Font("freesans.ttf",20)
##    textSurf, textRect = text_objects(msg, smallText, white)
##    textRect.center = ( (x+(w/2)), (y+(h/2)) )
##    pencere.blit(textSurf, textRect)
##
##    if x+w > mouse[0] > x and y+h > mouse[1] > y:
##        pygame.draw.rect(pencere, ic,(x,y,w,h))
##        if click[0] == 1 != None:
##            action()
##        smallText = pygame.font.Font("freesans.ttf",20)
##        textSurf, textRect = text_objects(msg, smallText, white)
##        textRect.center = ( (x+(w/2)), (y+(h/2)) )
##        pencere.blit(textSurf, textRect)
##def loop():
##    cikis = False
##    while not cikis:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                cikis = True
##                pygame.quit()
##                quit()
##            pencere.fill(white)
##            smallText = pygame.font.Font("freeSans.ttf",50)
##            textSurf, textRect = text_objects(str(number.count), smallText, Button_Farbe)
##            textRect.center = ((x/2)), (30)
##            pencere.blit(textSurf, textRect)
##            button("Click",B-120,H-60,100,50,Button_Farbe,Button_Farbe2,number.click)
##            pygame.display.update()
##loop()
##pygame.quit()
##quit()
##
pygame.font.get_fonts()
