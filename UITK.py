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
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, containerWindows: [Window],
                 horizontalDist=True, spacing=0):
        super().__init__(originX, originY, width, height, identifier, layoutAnchors)
        self.containerWindows = containerWindows
        # boolean that is true when items should be horizontally distributed, otherwise they are vertically distributed
        self.horizontalDist = horizontalDist
        # spacing between items
        self.spacing = spacing

    def addWindowToContainer(self, window):
        if window not in self.containerWindows:
            self.containerWindows.append(window)
            # adapt container to added window
            self.resize(self.x, self.y, self.width, self.height)
    
    def removeWindowFromContainer(self, window):
        if window in self.containerWindows:
            self.containerWindows.remove(window)
            # adapt container to removed window
            self.resize(self.x, self.y, self.width, self.height)

    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)
        if len(self.containerWindows) == 0:
            return
        totalSpacing = self.spacing * (len(self.containerWindows) - 1)
        # if not self.isHidden:
        if self.horizontalDist:
            # DISTRIBUTE HORIZONTALLY
            # calculate width for each window inside container
            conWindowWidth = (self.width - totalSpacing) / len(self.containerWindows)
            if conWindowWidth < 20:
                conWindowWidth = 20
            # x is increased for each containerWindow ensuring spacing
            currentX = self.x
            for window in self.containerWindows:
                window.x = currentX
                window.y = self.y
                window.width = conWindowWidth
                window.height = self.height
                currentX += window.width + self.spacing
                # as window's width changed, check if it reaches out of parent window
                window.isHidden = window.x + window.width > window.parentWindow.width or window.y + window.height > window.parentWindow.height
            # container height is the same as the maximum container window height
            # self.height = max(window.height for window in self.containerWindows)
        else:
            # DISTRIBUTE VERTICALLY
            # calculate width for each window inside container
            conWindowHeight = (self.height - totalSpacing) / len(self.containerWindows)
            if conWindowHeight < 20:
                conWindowHeight = 20
            # y is increased for each containerWindow ensuring spacing
            currentY = self.y
            for window in self.containerWindows:
                window.y = currentY
                window.x = self.x
                window.width = self.width
                window.height = conWindowHeight
                currentY += window.height + self.spacing
                # as window's height changed, check if it reaches out of parent window
                window.isHidden = window.x + window.width > window.parentWindow.width or window.y + window.height > window.parentWindow.height
            # container width is the same as the maximum container window height

    def draw(self, ctx):
        super().draw(ctx)
        """
        if not self.isHidden:
            # draw border to test container resizing
            x, y = self.convertPositionToScreen(0, 0)
            ctx.setOrigin(x, y)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.strokeRect(0, 0, self.width, self.height)
        """

    # override hitTest function and always return false since were are not interested in if the container was hit
    def hitTest(self, x, y):
        return False


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, text, centered=True,
                 font=None, fontColor=None):
        self.text = text
        self.centered = centered
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

        tempWidth, tempHeight = self.getDrawingSize()

        # draw text with specified font (color) into label
        if not self.isHidden:
            x, y = self.convertPositionToScreen(0, 0)
            ctx.setOrigin(x, y)
            ctx.setStrokeColor(self.fontColor)
            ctx.setFont(self.font)
            if self.centered:
                ctx.drawString(self.text, tempWidth/2, tempHeight/2, centered=True)
            else:
                ctx.drawString(self.text, 1, tempHeight*0.2)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, text, hoverBackgroundColor,
                 pressedBackgroundColor, centered=True, font=None, fontColor=None, action=None, borderColor=COLOR_WHITE):
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
        self.borderColor = borderColor
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, text, centered, font, fontColor)

    def draw(self, ctx):
        super().draw(ctx)
        if self.state == "HOVERED":
            self.setBackgroundColor(self.hoverBackgroundColor)
        elif self.state == "PRESSED":
            self.setBackgroundColor(self.pressedBackgroundColor)
        else:
            if self.tempBackgroundColor is not None:
                self.setBackgroundColor(self.tempBackgroundColor)

        # check temporary size to ensure clipping
        tempWidth, tempHeight = self.getDrawingSize()

        if not self.isHidden:
            x, y = self.convertPositionToScreen(0,0)
            ctx.setOrigin(x, y)
            # draw border in two colors to get depth effect
            ctx.setStrokeColor(self.borderColor)
            ctx.drawLine(0, 0, tempWidth, 0)
            ctx.drawLine(0, 0, 0, tempHeight)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.drawLine(tempWidth, 0, tempWidth, tempHeight)
            ctx.drawLine(0, tempHeight, tempWidth, tempHeight)

    # Call-back function that is executed when button is clicked
    def handleMouseClicked(self, x, y):
        if self.action is not None:
            self.action()
        self.changeState("HOVERED")
        print("button clicked")


    def changeState(self, state):
        if self.state == "NORMAL" and state == "HOVERED":
            # store background color while changing state from NORMAL to HOVERED
            self.tempBackgroundColor = self.backgroundColor
        if state in ["NORMAL", "HOVERED", "PRESSED"]:
            self.state = state
        else:
            raise ValueError("Button state must be 'NORMAL' or 'HOVERED' or 'PRESSED'")


class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors, defaultSliderValue=0.5, action=None):
        # Value is in range [0,1]
        self.sliderValue = defaultSliderValue
        # Size of the element that can be moved around
        self.sliderElementWidth = 30
        # Position of the slider element, this is offset from the value, because the position
        # is set from the center, and the value is measured from the left side of the element
        self.sliderPosition = self.sliderValue * width
        self.state = "NORMAL"
        self.action = action
        super().__init__(originX, originY, width, height, identifier, layoutAnchors)
        self.changeSlider(self.sliderValue * width)

    def changeState(self, state):
        if state in ["NORMAL", "PRESSED"]:
            self.state = state
        else:
            raise ValueError("Slider state must be 'NORMAL' or 'PRESSED' instead of: " + str(state))
        if state == "PRESSED" and self.action is not None:
            self.action()

    def changeSlider(self, x):
        # clamp values to min and max range
        # The left most position is elementWidth/2 but has to be value 0
        # The right most position is width-elementWidth/2 but has to be value 1
        # so the actual usable position range is from elementWidth/2 to width-elementWidth/2
        x = max(self.sliderElementWidth / 2, x)
        x = min(self.width - self.sliderElementWidth / 2, x)
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

        tempWidth, tempHeight = self.getDrawingSize()

        # Draw stroke
        if not self.isHidden:
            # Stroke
            x,y = self.convertPositionToScreen(0,0)
            ctx.setOrigin(x,y)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.drawLine(0, 0, tempWidth, 0)
            ctx.drawLine(0, 0, 0, tempHeight)
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawLine(tempWidth, 0, tempWidth, tempHeight)
            ctx.drawLine(0, tempHeight, tempWidth, tempHeight)

            # slider element exceeds parent window and disappears
            if self.sliderPosition + self.sliderElementWidth/2 > self.parentWindow.width:
                return

            # Slider Element Fill
            x, y = self.convertPositionToScreen(self.sliderPosition-(self.sliderElementWidth/2), 0)
            ctx.setOrigin(x,y)
            if self.state == "NORMAL":
                ctx.setFillColor(COLOR_LIGHT_GRAY)
            if self.state == "PRESSED":
                ctx.setFillColor(COLOR_GRAY)
            ctx.fillRect(0, 0, self.sliderElementWidth, tempHeight)

            # Slider Element Stroke
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawLine(0, 0, self.sliderElementWidth, 0)
            ctx.drawLine(0, 0, 0, tempHeight)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.drawLine(self.sliderElementWidth, 0, self.sliderElementWidth, tempHeight)
            ctx.drawLine(0, tempHeight, self.sliderElementWidth, tempHeight)
