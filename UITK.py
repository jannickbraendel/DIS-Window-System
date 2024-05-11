#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Felix Umland (#406886)
and Jannick Brändel (#405391)
"""

from GraphicsEventSystem import *
from Window import *


class Widget(Window):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors):
        super().__init__(originX, originY, width, height, identifier, layoutAnchors)
        self.backgroundColor = COLOR_CLEAR

    def draw(self, ctx):
        super().draw(ctx)


class Container(Widget):
    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, text, backgroundColor,
                 font=Font(family="Helvetica", size=12), fontColor="COLOR_BLACK"):
        self.backgroundColor = backgroundColor
        self.text = text
        self.font = font
        self.fontColor = fontColor
        super().__init__(originX, originY, width, height, identifier, layoutAnchors)

    def draw(self, ctx):
        # draw background with superclass function
        super().draw(ctx)
        # draw text with specified font (color) into label
        ctx.setOrigin(self.convertPositionToScreen(0, 0))
        ctx.setStrokeColor(self.fontColor)
        ctx.setFont(self.font)
        ctx.drawString(3, 1, self.text)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, text, backgroundColor,
                 font=Font(family="Helvetica", size=12), fontColor="COLOR_BLACK", action=None):
        # lambda function that is executed when button is clicked
        self.action = action
        # state can either be "NORMAL", "HOVERED", or "PRESSED"
        self.state = "NORMAL"
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, text, backgroundColor, font, fontColor)

    def draw(self, ctx):
        # TODO: change background color based on button state
        super().draw(ctx)
        # TODO: draw borders (with depth?)

    # Call-back function that is executed when button is clicked
    def handleMouseClicked(self, x, y):
        if self.action is not None:
            self.action()
        self.changeState("NORMAL")

    def changeState(self, state):
        if state in ["NORMAL", "HOVERED", "PRESSED"]:
            self.state = state
        else:
            raise ValueError("Button state must be 'NORMAL' or 'HOVERED' or 'PRESSED'")

class Slider(Widget):
    def draw(self, ctx):
        super().draw(ctx)
