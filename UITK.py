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
        # self.backgroundColor = COLOR_CLEAR

    def draw(self, ctx):
        super().draw(ctx)


class Container(Widget):
    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, text,
                 font=None, fontColor=None):
        self.text = text
        if font is None:
            font = Font(family="Helvetica", size=12)
        if fontColor is None:
            fontColor = COLOR_BLACK
        self.font = font
        self.fontColor = fontColor
        super().__init__(originX, originY, width, height, identifier, layoutAnchors)

    def draw(self, ctx):
        # draw background with superclass function
        super().draw(ctx)
        # draw text with specified font (color) into label
        if not self.isHidden:
            x, y = self.convertPositionToScreen(0, 0)
            ctx.setOrigin(x, y)
            ctx.setStrokeColor(self.fontColor)
            ctx.setFont(self.font)
            ctx.drawString(self.text, 3, 1)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, text, hoverBackgroundColor, pressedBackgroundColor,
                 font=None, fontColor=None, action=None):
        # lambda function that is executed when button is clicked
        self.action = action
        # state can either be "NORMAL", "HOVERED", or "PRESSED"
        self.state = "NORMAL"
        if font is None:
            font = Font(family="Helvetica", size=12)
        if fontColor is None:
            fontColor = COLOR_BLACK
        self.hoverBackgroundColor = hoverBackgroundColor
        self.pressedBackgroundColor = pressedBackgroundColor
        self.tempBackgroundColor = None
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, text, font, fontColor)

    def draw(self, ctx):
        # TODO: change background color based on button state
        super().draw(ctx)
        # TODO: draw borders (with depth?)
        if self.state == "HOVERED":
            self.setBackgroundColor(self.hoverBackgroundColor)
        elif self.state == "PRESSED":
            self.setBackgroundColor(self.pressedBackgroundColor)
        else:
            if self.tempBackgroundColor is not None:
                self.setBackgroundColor(self.tempBackgroundColor)

        if not self.isHidden:
            x,y = self.convertPositionToScreen(0,0)
            ctx.setOrigin(x,y)
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawLine(0, 0, self.width, 0)
            ctx.drawLine(0, 0, 0, self.height)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.drawLine(self.width, 0, self.width, self.height)
            ctx.drawLine(0, self.height, self.width, self.height)
    # Call-back function that is executed when button is clicked
    def handleMouseClicked(self, x, y):
        if self.action is not None:
            self.action()
        self.changeState("HOVERED")
        print("button clicked")


    def changeState(self, state):
        if self.state == "NORMAL" and state == "HOVERED":
            self.tempBackgroundColor = self.backgroundColor
        if state in ["NORMAL", "HOVERED", "PRESSED"]:
            self.state = state
        else:
            raise ValueError("Button state must be 'NORMAL' or 'HOVERED' or 'PRESSED'")

class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, defaultSliderValue=0.5):
        # Value is in range [0,1]
        self.sliderValue = defaultSliderValue
        # Size of the element that can be moved around
        self.sliderElementWidth = 30
        # Position of the slider element, this is offset from the value, because the position
        # is set from the center, and the value is measured from the left side of the element
        self.sliderPosition = self.sliderValue * width
        self.state = "NORMAL"
        super().__init__(originX, originY, width, height, identifier, layoutAnchors)

    def changeState(self, state):
        if state in ["NORMAL", "PRESSED"]:
            self.state = state
        else:
            raise ValueError("Button state must be 'NORMAL' or 'HOVERED' or 'PRESSED'")

    def changeSlider(self, x):
        # The left most position is elementWidth/2 but has to be value 0
        # The right most position is width-elementWidth/2 but has to be value 1
        # so the actual usable position range is from elementWidth/2 to width-elementWidth/2
        if x >= (self.sliderElementWidth/2) and x <= (self.width - self.sliderElementWidth/2):
            # value is calculated from the left side of the element, so from x - elementWidth/2
            leftPosition = x-self.sliderElementWidth/2
            # The usable value range is (width - elementWidth) because having the slider
            # at the right most position means the left slide (where we measure value) of the element isn't at 100%
            usableRange = self.width-self.sliderElementWidth
            # normalize the position to a value in range [0,1]
            self.sliderValue = leftPosition/usableRange
            print(self.sliderValue)
            self.sliderPosition = x
            print(self.sliderPosition)


    def draw(self, ctx):
        super().draw(ctx)
        # Draw stroke
        if not self.isHidden:
            # Stroke
            x,y = self.convertPositionToScreen(0,0)
            ctx.setOrigin(x,y)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.drawLine(0, 0, self.width, 0)
            ctx.drawLine(0, 0, 0, self.height)
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawLine(self.width, 0, self.width, self.height)
            ctx.drawLine(0, self.height, self.width, self.height)

            # Slider Element Fill
            x, y = self.convertPositionToScreen(self.sliderPosition-(self.sliderElementWidth/2), 0)
            ctx.setOrigin(x,y)
            ctx.setFillColor(COLOR_LIGHT_GRAY)
            ctx.fillRect(0, 0, self.sliderElementWidth, self.height)

            # Slider Element Stroke
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawLine(0, 0, self.sliderElementWidth, 0)
            ctx.drawLine(0, 0, 0, self.height)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.drawLine(self.sliderElementWidth, 0, self.sliderElementWidth, self.height)
            ctx.drawLine(0, self.height, self.sliderElementWidth, self.height)
