#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *
from Window import *

class Widget(Window):
	def __init__(self, originX, originY, width, height, identifier):
		super().__init__(originX, originY, width, height, identifier)
		self.backgroundColor = COLOR_CLEAR




class Container(Widget):
	def resize(self, x, y, width, height):
		super().resize(x, y, width, height)




class Label(Widget):
	def draw(self, ctx):
		super().draw(ctx)




class Button(Label):
	def draw(self, ctx):
		super().draw(ctx)



	
class Slider(Widget):
	def draw(self, ctx):
		super().draw(ctx)
		
	
		