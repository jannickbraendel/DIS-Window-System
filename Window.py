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
        """
        Constructor for a new window setting the relevant attributes and the default background color to BLUE
        :param originX: X coordinate of the top left corner of the window (coordinate system of parent window)
        :param originY: Y coordinate of the top left corner of the window (coordinate system of parent window)
        :param width: Width of the window
        :param height: Height of the window
        :param identifier: window ID
        """
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.backgroundColor = COLOR_LIGHT_BLUE

        self.childWindows = []
        self.parentWindow = None

    def addChildWindow(self, window):
        """
        Add given window as child window.
        :param window: window which is added as child window
        """
        self.childWindows.append(window)
        window.parentWindow = self

    def removeFromParentWindow(self):
        """
        Remove current window from its parent's child windows.
        """
        self.parentWindow.childWindows.remove(self)

    def childWindowAtLocation(self, x, y):
        """
        Takes hit position, checks which child windows of the curr window are hit while choosing the topmost child
        according to its z-level.
        :param x: x-value of hit position
        :param y: y-value of hit position
        :return: Topmost child window (z-level) that was hit
        """
        # loop through child windows in reverse as they are sorted by ascending z-level, and we want the topmost one
        for i in reversed(range(len(self.childWindows))):
            child = self.childWindows[i]
            print("testing: " + child.identifier)
            # transform the position into the child's local coord. system and checks if it is hit
            if child.hitTest(x - child.x, y - child.y):
                print("hit: " + child.identifier)
                print("x: " + str(x - child.x) + " y: " + str(y - child.y))
                if len(child.childWindows) > 0:
                    # child window has children -> function is called recursively
                    return child.childWindowAtLocation(x - child.x, y - child.y)
                else:
                    # top-most child window (with no children) found and returned
                    return child

        # no child window was hit -> return None
        return self

    def hitTest(self, x, y):
        """
        Check if the hit position specified by x and y parameters is inside the local coordinate system.
        :param x: x-value of hit position
        :param y: y-value of hit position
        :return: True if hit position is inside the local coordinate system.
        """
        if x < 0 or y < 0:
            # hit occurred above or to the left of the window -> no hit
            return False
        else:
            # x and y are above 0 and if they are less than the width or height respectively, return true
            return x < self.width and y < self.height

    def convertPositionToScreen(self, x, y):
        """
        Takes local position and converts it to the global coordinate system of the screen.
        :param x: x-value of screen position
        :param y: y-value of screen position
        :return: x and y value of the converted screen position
        """
        totalX = x
        totalY = y
        parent = self.parentWindow
        # loop through the path up to the root (screen) and add each x and y value to the given position (results in
        # position on screen)
        while parent is not None:
            totalX += parent.x
            totalY += parent.y
            parent = parent.parentWindow

        return totalX, totalY

    def convertPositionFromScreen(self, x, y):
        """
        Takes screen position and converts it to the local coordinate system of the current window.
        :param x: x-value of screen position
        :param y: y-value of screen position
        :return: converted x and y values in local coordinate system
        """
        # subtract local origin (converted to screen coordinates) from the given global position (results in local x
        # and y)
        localX = x - self.convertPositionToScreen(x, y)[0]
        localY = y - self.convertPositionToScreen(x, y)[1]
        return localX, localY

    def draw(self, ctx):
        """
        Draw current window and all child windows on screen and filling them with the specified background color.
        :param ctx: Current graphics context
        """
        # set ctx origin to the global position of the window's origin
        position = self.convertPositionToScreen(self.x, self.y)
        ctx.setOrigin(position[0], position[1])
        # ctx should draw with bg color
        ctx.setFillColor(self.backgroundColor)
        # fill the complete window
        ctx.fillRect(0, 0, self.width, self.height)
        # recursively draw child windows in ascending z-order
        for child in self.childWindows:
            child.draw(ctx)

    def handleMouseClicked(self, x, y):
        """
        Call-back function when specified position was clicked (mouse pressed and released).
        :param x: x-value of click position in local coordinate system
        :param y: y-value of click position in local coordinate system
        """
        print("Window " + self.identifier + " was clicked.")

    def setBackgroundColor(self, color):
        self.backgroundColor = color


class Screen(Window):
    def __init__(self, windowSystem):
        """
        Window that includes the whole screen of the window system.
        :param windowSystem: Window system the screen belongs to
        """
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

    def draw(self, ctx):
        """
        Apply draw implementation of super-class window.
        :param ctx: Current graphics context
        """
        super().draw(ctx)
