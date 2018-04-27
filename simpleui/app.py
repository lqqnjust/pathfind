#!/usr/bin/env python
# coding:utf-8
import pygame
from pygame.locals import *

class Application(object):
    def __init__(self, title, winsize):
        self.winsize = winsize
        self.title = title
    
        pygame.init()
        self.screen = pygame.display.set_mode(self.winsize, 0, 32)

        pygame.display.set_caption(self.title)

        self.objects = []


        self.fpsClock = pygame.time.Clock()
        self.fps = 60


    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()


            pygame.display.flip()
            self.fpsClock.tick(60)
            