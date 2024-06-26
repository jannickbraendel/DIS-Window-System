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
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors=LayoutAnchor.top | LayoutAnchor.left,
                 backgroundColor=COLOR_CLEAR):
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, backgroundColor)

    def draw(self, ctx):
        super().draw(ctx)


class Container(Widget):
    def __init__(self, originX, originY, width, height, identifier, containerWindows: [Window],
                 horizontalDist=True, spacing=0, layoutAnchors=LayoutAnchor.top | LayoutAnchor.left,
                 backgroundColor=COLOR_CLEAR):
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, backgroundColor)
        self.containerWindows = containerWindows
        # boolean that is true when items should be horizontally distributed, otherwise they are vertically distributed
        self.horizontalDist = horizontalDist
        # spacing between items
        self.spacing = spacing

    # new window is added to container windows array. No window object should be in a container twice
    # (not used right now but maybe useful for future apps?)
    def addWindowToContainer(self, window):
        if window not in self.containerWindows:
            self.containerWindows.append(window)
            # adapt container to added window
            self.resize(self.x, self.y, self.width, self.height)

    # window is removed from container windows array
    # (not used right now but maybe useful for future apps?)
    def removeWindowFromContainer(self, window):
        if window in self.containerWindows:
            self.containerWindows.remove(window)
            # adapt container to removed window
            self.resize(self.x, self.y, self.width, self.height)

    # override resize function of window: container distributes its space between the container windows and resizes
    # them to have the same width/height and position them while leaving space in between if spacing is defined.
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
                if isinstance(window, Container):
                    # nested container: call resize to adjust container windows of that container
                    window.resize(window.x, window.y, window.width, window.height)

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
                if isinstance(window, Container):
                    # nested container: call resize to adjust container windows of that container
                    window.resize(window.x, window.y, window.width, window.height)

    def draw(self, ctx):
        super().draw(ctx)

    # override hitTest function and always return false since were are not interested in if the container was hit
    def hitTest(self, x, y):
        return False


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, text, centered=True,
                 font=None, fontColor=None, layoutAnchors=LayoutAnchor.top | LayoutAnchor.left,
                 backgroundColor=COLOR_CLEAR):
        # text displayed in label
        self.text = text
        # boolean that is true, if text should be centered inside label
        self.centered = centered
        # font as optional parameter, will be set to default if none
        if font is None:
            font = Font(family="Helvetica", size=12)
        # font color as opt. parameter
        if fontColor is None:
            fontColor = COLOR_BLACK
        self.font = font
        self.fontColor = fontColor
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, backgroundColor)

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
            # check if text should be centered and set coordinates and centered attribute accordingly
            if self.centered:
                ctx.drawString(self.text, tempWidth/2, tempHeight/2, centered=True)
            else:
                ctx.drawString(self.text, 1, tempHeight*0.2)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, text, hoverBackgroundColor,
                 pressedBackgroundColor, centered=True, font=None, fontColor=None, action=None, borderColor=COLOR_WHITE,
                 layoutAnchors=LayoutAnchor.top | LayoutAnchor.left, backgroundColor=COLOR_CLEAR):
        # lambda function that is executed when button is clicked
        self.action = action
        # state can either be "NORMAL", "HOVERED", or "PRESSED"
        self.state = "NORMAL"
        # font and font color same as in label class
        if font is None:
            font = Font(family="Helvetica", size=12)
        if fontColor is None:
            fontColor = COLOR_BLACK
        self.hoverBackgroundColor = hoverBackgroundColor
        self.pressedBackgroundColor = pressedBackgroundColor
        # temp variable to store original background color -> used while changing button state from Hovered to Normal
        # again
        self.tempBackgroundColor = None
        # color used for left and top line of the border as the other lines are drawn in black to get depth effect
        self.borderColor = borderColor
        super().__init__(originX, originY, width, height, identifier, text, centered, font, fontColor, layoutAnchors,
                         backgroundColor)

    def draw(self, ctx):
        super().draw(ctx)
        # set background color according to current state
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
        # after mouse click mouse is still on button so state changes to HOVERED
        self.changeState("HOVERED")

    # update button state with state parameter
    def changeState(self, state):
        if self.state == "NORMAL" and state == "HOVERED":
            # store background color while changing state from NORMAL to HOVERED
            self.tempBackgroundColor = self.backgroundColor
        if state in ["NORMAL", "HOVERED", "PRESSED"]:
            self.state = state
        else:
            raise ValueError("Button state must be 'NORMAL' or 'HOVERED' or 'PRESSED'")


class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier, defaultSliderValue=0.5, action=None,
                 layoutAnchors=LayoutAnchor.top | LayoutAnchor.left, backgroundColor=COLOR_CLEAR):
        # Value is in range [0,1]
        self.sliderValue = defaultSliderValue
        # Size of the element that can be moved around
        self.sliderElementWidth = 30
        # Position of the slider element, this is offset from the value, because the position
        # is set from the center, and the value is measured from the left side of the element
        self.sliderPosition = self.sliderValue * width
        self.state = "NORMAL"
        self.action = action
        super().__init__(originX, originY, width, height, identifier, layoutAnchors, backgroundColor)
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
