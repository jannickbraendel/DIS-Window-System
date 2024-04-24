#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by Felix Umland (#406886)
and Jannick Brändel (#405391)
"""

from GraphicsEventSystem import *


class Window:
    def __init__(self, originX, originY, width, height, identifier):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.backgroundColor = COLOR_LIGHT_GRAY

        self.childWindows = []
        self.parentWindow = None

    def addChildWindow(self, window):
        self.childWindows.append(window)
        window.parentWindow = self

    def removeFromParentWindow(self):
        self.parentWindow.childWindows.remove(self)

    def childWindowAtLocation(self, x, y):
        for i in reversed(range(len(self.childWindows))):
            child = self.childWindows[i]
            print("testing: " + child.identifier)
            if child.hitTest(x - child.x, y - child.y):
                print("hit: " + child.identifier)
                print("x: " + str(x - child.x) + " y: " + str(y - child.y))
                if len(child.childWindows) > 0:
                    return child.childWindowAtLocation(x - child.x, y - child.y)
                else:
                    return child
        return None

    def hitTest(self, x, y):
        if x < 0 or y < 0:
            return False
        else:
            return x < self.width and y < self.height

    def convertPositionToScreen(self, x, y):
        totalX = x
        totalY = y
        parent = self.parentWindow

        while parent is not None:
            totalX += parent.x
            totalY += parent.y
            parent = parent.parentWindow

        return totalX, totalY

    def convertPositionFromScreen(self, x, y):
        localX = x - self.convertPositionToScreen(x, y)[0]
        localY = y - self.convertPositionToScreen(x, y)[1]
        return localX, localY

    def draw(self, ctx):
        position = self.convertPositionToScreen(self.x, self.y)
        ctx.setOrigin(position[0], position[1])
        ctx.setFillColor(self.backgroundColor)
        ctx.fillRect(0, 0, self.width, self.height)
        for child in self.childWindows:
            child.draw(ctx)

    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")

    def setBackgroundColor(self, color):
        self.backgroundColor = color


class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

    def draw(self, ctx):
        super().draw(ctx)
