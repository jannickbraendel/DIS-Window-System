#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by Felix Umland (#406886)
and Jannick Brändel (#405391)
"""

from GraphicsEventSystem import *
from collections import namedtuple

# initialize bit mask for resizing/anchoring
AllAnchors = namedtuple('AllAnchors', "top right bottom left")
LayoutAnchor = AllAnchors(1 << 0, 1 << 1, 1 << 2, 1 << 3)


class Window:
    def __init__(self, originX, originY, width, height, identifier, layoutAnchors=LayoutAnchor.top | LayoutAnchor.left):
        """
        Constructor for a new window setting the relevant attributes and the default background color
        :param originX: X coordinate of the top left corner of the window (coordinate system of parent window)
        :param originY: Y coordinate of the top left corner of the window (coordinate system of parent window)
        :param width: Width of the window
        :param height: Height of the window
        :param identifier: window ID
        :param layoutAnchors: anchors to parent window in all directions (default: top-left)
        """
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.backgroundColor = None

        self.childWindows = []
        self.parentWindow = None
        # used to minimize top-level windows
        self.isHidden = False
        # window is anchored to top-left by default
        self.layoutAnchors = layoutAnchors

        # non-top level windows: save margins to bottom and right
        self.marginRight = 0
        self.marginBottom = 0

    def addChildWindow(self, window):
        """
        Add given window as child window.
        :param window: window which is added as child window
        """
        self.childWindows.append(window)
        window.parentWindow = self

        """
        if self.identifier == "SCREEN":
            screen = self
        else:
            screen = self.getTopLevelWindow().parentWindow
        
        # check if child window exceeds parent window in size and adjust accordingly (NOT NEEDED FOR TL WINDOWS)
        if self.identifier == "SCREEN":
            return

        if window.x < 0:
            window.x = 0

        titleBarHeight = screen.windowSystem.windowManager.titleBarHeight
        if window.parentWindow.parentWindow == screen and "- Title Bar" not in window.identifier:
            # child windows of top-level windows (that are not the title bar itself) should not cover the title bar
            if window.y < titleBarHeight:
                window.y = titleBarHeight
        else:
            if window.y < 0:
                window.y = 0

        if window.parentWindow.identifier != "SCREEN":
            windowRightBorder = window.x + window.width
            windowLowerBorder = window.y + window.height
            if windowRightBorder > self.width:
                widthToRemove = windowRightBorder - self.width
                window.width -= widthToRemove
            if windowLowerBorder > self.height:
                heightToRemove = windowLowerBorder - self.height
                window.height -= heightToRemove
        """
        # save margins to bottom and right: they might be broken while resizing and have to be re-established
        window.marginRight = self.width - (window.x + window.width)
        window.marginBottom = self.height - (window.y + window.height)
        # trigger resize to ensure window is correctly positioned according to anchors
        if not self.identifier == "SCREEN" and "- Title Bar" not in window.identifier:
            self.resize(self.x, self.y, self.width, self.height)

    def removeFromParentWindow(self):
        """
        Remove current window from its parent's child windows.
        """
        self.parentWindow.childWindows.remove(self)
        self.parentWindow = None

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
            # transform the position into the child's local coord. system and checks if it is hit
            if child.hitTest(x - child.x, y - child.y):
                if len(child.childWindows) > 0:
                    # child window has children -> function is called recursively
                    return child.childWindowAtLocation(x - child.x, y - child.y)
                else:
                    # top-most child window (with no children) found and returned
                    return child

        # no child window was hit -> return Self
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
            return x <= self.width and y <= self.height

    def convertPositionToScreen(self, x, y):
        """
        Takes local position and converts it to the global coordinate system of the screen.
        :param x: x-value of screen position
        :param y: y-value of screen position
        :return: x and y value of the converted screen position
        """
        totalX = x + self.x
        totalY = y + self.y
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
        screenX, screenY = self.convertPositionToScreen(0, 0)
        localX = x - screenX
        localY = y - screenY
        return localX, localY

    def draw(self, ctx):
        """
        Draw current window and all child windows on screen and filling them with the specified background color.
        :param ctx: Current graphics context
        """
        # temporary width and height values are based on if the window is clipped by its parent
        tempWidth, tempHeight = self.getDrawingSize()

        # do not draw if hidden currently:
        if self.isHidden:
            return

        # set ctx origin to the global position of the window's origin
        position = self.convertPositionToScreen(0, 0)
        ctx.setOrigin(position[0], position[1])
        # ctx should draw with bg color
        if self.backgroundColor is not None:
            ctx.setFillColor(self.backgroundColor)
        else:
            ctx.setFillColor(COLOR_CLEAR)
        # fill the complete window
        ctx.fillRect(0, 0, tempWidth, tempHeight)

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

    def getTopLevelWindow(self):

        if self.identifier == "SCREEN":
            return self

        topLevelWindow = self
        while topLevelWindow.parentWindow.identifier != "SCREEN":
            topLevelWindow = topLevelWindow.parentWindow

        return topLevelWindow

    # resizes itself and all its child windows
    def resize(self, x, y, width, height):
        titleBarHeight = self.getTopLevelWindow().parentWindow.windowSystem.windowManager.titleBarHeight
        parentWidth = self.parentWindow.width
        parentHeight = self.parentWindow.height
        if self.parentWindow.identifier == "SCREEN":
            # TOP-LEVEL WINDOW: RESIZING
            # resize window with updated values
            self.x = x
            self.y = y
            # new width/height should not be lower than min width/height
            self.width = max(self.parentWindow.windowSystem.windowManager.tlwMinWidth, width)
            self.height = max(self.parentWindow.windowSystem.windowManager.tlwMinHeight, height)
        else:
            # NO TOP-LEVEL WINDOW: RESIZING
            # keep width and height the same for anchored windows (unless it is changed below)
            width, height = self.width, self.height
            # store current window anchors to use in the following
            topAnchor = self.layoutAnchors & LayoutAnchor.top
            rightAnchor = self.layoutAnchors & LayoutAnchor.right
            bottomAnchor = self.layoutAnchors & LayoutAnchor.bottom
            leftAnchor = self.layoutAnchors & LayoutAnchor.left

            # HORIZONTAL ANCHORING:
            # not anchored to either left or right: keep relative distance to left and right
            if not (leftAnchor or rightAnchor):
                x = parentWidth/2 - self.width/2
            # anchored to left and right: keep exact margins to left and right
            elif leftAnchor and rightAnchor:
                width = parentWidth - 2 * x
            # only anchored to right: keep exact distance to the right
            elif rightAnchor:
                x = parentWidth - width - self.marginRight
                # x += deltaWidth

            # VERTICAL ANCHORING:
            # not anchored to either top or bottom: keep relative distance to top and bottom
            if not (topAnchor or bottomAnchor):
                y = parentHeight/2 - self.height/2
            # anchored to top and bottom: resize vertically
            elif topAnchor and bottomAnchor:
                height = parentHeight - 2 * y
            # only anchored to bottom: keep exact distance to bottom
            elif bottomAnchor:
                y = parentHeight - height - self.marginBottom
                # y += deltaHeight

            # CONSTRAINTS:
            # if x or y get negative, stick them to left side of window
            if x < 0:
                x = 0
            if y < titleBarHeight:
                y = titleBarHeight
            # minimum size values for child windows
            if width < 20:
                width = 20
            if height < 20:
                height = 20

            """
            # if window reaches out of parent on any side, clip it (set hidden)
            self.isHidden = x + width > self.parentWindow.width or y + height > self.parentWindow.height
            """
            # resize window with updated values
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        # resize child windows
        for child in self.childWindows:
            child.resize(child.x, child.y, child.width, child.height)

    # returns temporary width and height values of a window to clip it to the bounds of its parent window (if exceeding)
    def getDrawingSize(self):
        # TODO: Check edge case where grandchild window exceeds tl window but is not clipped
        tempWidth = self.width
        tempHeight = self.height
        # TL windows keep their size
        if not self.parentWindow.identifier == "SCREEN":
            # HORIZONTALLY
            if self.x + self.width > self.parentWindow.width:
                # width set to distance between parent's right border and x origin (has to be <=0)
                tempWidth = max(0, self.parentWindow.width - self.x)
            # VERTICALLY
            if self.y + self.height > self.parentWindow.height:
                # height set to distance between parent's lower border and y origin (has to be <=0)
                tempHeight = max(0, self.parentWindow.height - self.y)

            # window should disappear in the case of temp width or height being 0
            self.isHidden = tempWidth == 0 or tempHeight == 0

        return tempWidth, tempHeight


class Screen(Window):
    def __init__(self, windowSystem):
        """
        Window that includes the whole screen of the window system.
        :param windowSystem: Window system the screen belongs to
        """
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN")
        self.windowSystem = windowSystem

    def draw(self, ctx):
        """
        Draw screen and task bar using the window manager and call draw function on all top level windows.
        :param ctx: Current graphics context
        """
        self.windowSystem.windowManager.drawDesktop(ctx)
        # call draw function on top-level windows and decorate them using the WM.
        for topLevelWindow in self.childWindows:
            if not topLevelWindow.isHidden:
                self.windowSystem.windowManager.decorateWindow(topLevelWindow, ctx)
                topLevelWindow.draw(ctx)
                self.windowSystem.windowManager.drawWindowDecorations(topLevelWindow, ctx)
        # task bar is drawn in the end to be in the foreground compared to other windows
        self.windowSystem.windowManager.drawTaskbar(ctx)
