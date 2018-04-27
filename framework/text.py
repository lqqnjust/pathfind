from .node import Node 

import pygame

class TextElement(Node):
    def __init__(self, text='', position=(0,0), **kwargs):
        super(TextElement, self).__init__()

        self.position = position
        self.args = []
        self.kwargs = kwargs
