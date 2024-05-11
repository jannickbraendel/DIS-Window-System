#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Felix Umland (#406886)
and Jannick Brändel (#405391)
"""

from GraphicsEventSystem import *
from Window import *


class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.titleBarHeight = 18
        self.titleBarButtonWidth = 10
        self.taskBarHeight = 35
        self.resizeCornerTolerance = 10

    def checkWindowPosition(self, window, x, y):
        # check if window is top-level window and return otherwise
        if window.parentWindow.identifier != "SCREEN":
            pass
        screen = window.parentWindow
        # amount of pixels of titlebar that should still be visible
        minimumTitleBarVisibility = 10
        titleBarVisibleLeft = x + window.width > minimumTitleBarVisibility + (3 * self.titleBarButtonWidth)
        titleBarVisibleRight = x < screen.width - minimumTitleBarVisibility

        titleBarVisibleTop = y + minimumTitleBarVisibility > 0
        titleBarVisibleBottom = y < screen.height - minimumTitleBarVisibility - self.taskBarHeight
        # returns true if title bar is visible towards all directions
        return titleBarVisibleLeft and titleBarVisibleRight and titleBarVisibleTop and titleBarVisibleBottom

    # creates windows for window decorations (title bar, buttons)
    def decorateWindow(self, window, ctx):
        # add title bar
        titleBar = Window(0, 0, window.width, self.titleBarHeight, window.identifier + " - Title Bar")
        # set background color based on if window is selected
        topLevelWindows = self.windowSystem.screen.childWindows
        windowIsSelected = topLevelWindows[len(topLevelWindows) - 1].identifier == window.identifier
        if windowIsSelected:
            # window is selected
            titleBar.setBackgroundColor(COLOR_DARK_GREEN)
        else:
            # window is in the background
            titleBar.setBackgroundColor(COLOR_LIGHT_GREEN)
        # append title bar to window
        window.addChildWindow(titleBar)
        # remove old title bar if already existing
        if len(window.childWindows) > 1 and "- Title Bar" in window.childWindows[len(window.childWindows) - 2].identifier:
            window.childWindows[len(window.childWindows) - 2].removeFromParentWindow()

        # add title window to title Bar
        titleWindow = Window(0, 0, titleBar.width/2, titleBar.height, titleBar.identifier + " - Title")
        titleWindow.setBackgroundColor(titleBar.backgroundColor)
        titleBar.addChildWindow(titleWindow)

        # add buttons windows
        buttonWidth = self.titleBarButtonWidth
        buttonHeight = self.titleBarHeight - 8
        distanceBetweenButtons = 5

        closeButton = Window(titleBar.width - buttonWidth - distanceBetweenButtons, 4, buttonWidth, buttonHeight, titleBar.identifier + " - Close Button")
        maximizeButton = Window(titleBar.width - (2 * buttonWidth + 2 * distanceBetweenButtons), 4, buttonWidth, buttonHeight, titleBar.identifier + " - Maximize Button")
        minimizeButton = Window(titleBar.width - (3 * buttonWidth + 3 * distanceBetweenButtons), 4, buttonWidth, buttonHeight, titleBar.identifier + " - Minimize Button")
        # buttons have same background color as titlebar
        closeButton.setBackgroundColor(titleBar.backgroundColor)
        maximizeButton.setBackgroundColor(titleBar.backgroundColor)
        minimizeButton.setBackgroundColor(titleBar.backgroundColor)
        # append buttons to title bar
        titleBar.addChildWindow(closeButton)
        titleBar.addChildWindow(maximizeButton)
        titleBar.addChildWindow(minimizeButton)

    # Does the drawing part of window decoration (title string, button icons)
    def drawWindowDecorations(self, window, ctx):
        # stroke border around window
        ctx.setStrokeColor(COLOR_GRAY)
        startX, startY = window.convertPositionToScreen(0, 0)
        ctx.setOrigin(startX, startY)
        ctx.strokeRect(0, 0, window.width, window.height)

        # get title and button window objects
        titleBar = window.childWindows[len(window.childWindows) - 1]
        titleWindow = None
        minimizeButton = None
        maximizeButton = None
        closeButton = None
        for child in titleBar.childWindows:
            if "- Minimize Button" in child.identifier:
                minimizeButton = child
            elif "- Maximize Button" in child.identifier:
                maximizeButton = child
            elif "- Close Button" in child.identifier:
                closeButton = child
            elif "- Title" in child.identifier:
                titleWindow = child
        # draw title string
        if None in (titleWindow, minimizeButton, maximizeButton, closeButton):
            return

        titleWindowX, titleWindowY = titleWindow.convertPositionToScreen(0, 0)
        ctx.setOrigin(titleWindowX, titleWindowY)
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.setFont(Font(family="Helvetica", size=10, weight="bold"))
        ctx.drawString(window.identifier, 3, 1)

        buttonWidth = self.titleBarButtonWidth
        buttonHeight = self.titleBarHeight - 8
        # draw minimize button
        minButtonX, minButtonY = minimizeButton.convertPositionToScreen(0, 0)
        ctx.setOrigin(minButtonX, minButtonY)
        ctx.drawLine(0, minimizeButton.height / 2, buttonWidth, minimizeButton.height / 2)
        # draw maximize button
        maxButtonX, maxButtonY = maximizeButton.convertPositionToScreen(0, 0)
        ctx.setOrigin(maxButtonX, maxButtonY)
        ctx.strokeRect(0, 0, buttonWidth, buttonHeight)
        # draw close button
        closeButtonX, closeButtonY = closeButton.convertPositionToScreen(0, 0)
        ctx.setOrigin(closeButtonX, closeButtonY)
        ctx.drawLine(0, 0, buttonWidth, buttonHeight)
        ctx.drawLine(0, buttonHeight, buttonWidth, 0)

    def drawDesktop(self, ctx):
        # desktop is filled with light blue color
        ctx.setFillColor(COLOR_LIGHT_BLUE)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)

    def drawTaskbar(self, ctx):
        # TODO: Border around icon buttons only when the window is selected not everywhere
        # set origin to top-left corner of task bar
        ctx.setOrigin(0, self.windowSystem.height - self.taskBarHeight)
        # draw task bar
        ctx.setFillColor(COLOR_DARK_BLUE)
        ctx.setStrokeColor(COLOR_GRAY)
        ctx.fillRect(0, 0, self.windowSystem.width, self.taskBarHeight)
        ctx.strokeRect(0, 0, self.windowSystem.width, self.taskBarHeight)

        # draw quit button
        ctx.setFillColor(COLOR_RED)
        ctx.fillRect(0, 0, self.taskBarHeight, self.taskBarHeight)
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.setFont(Font(family="Helvetica", size=20, weight="bold"))
        ctx.drawString("X", self.taskBarHeight * 0.23, self.taskBarHeight * 0.1)

        # draw window icons
        curX, curY = (self.taskBarHeight + 1, self.windowSystem.height - self.taskBarHeight)
        topLevelWindows = self.windowSystem.screen.childWindows
        # sort windows alphabetically to have fixed order of icons
        topLevelWindowsSorted = sorted(topLevelWindows, key=lambda x: x.identifier)
        # add icon for each top level window
        for topLevelWindow in topLevelWindowsSorted:
            ctx.setOrigin(curX, curY)
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.strokeRect(0, 0, self.taskBarHeight, self.taskBarHeight)
            windowIsSelected = topLevelWindows[len(topLevelWindows) - 1].identifier == topLevelWindow.identifier
            if windowIsSelected:
                # window is selected
                ctx.setFillColor(COLOR_DARK_GREEN)
                ctx.setStrokeColor(COLOR_WHITE)
            else:
                # window is in the background
                ctx.setFillColor(COLOR_LIGHT_GREEN)
                ctx.setStrokeColor(COLOR_WHITE)

            ctx.fillRect(0, 0, self.taskBarHeight, self.taskBarHeight)
            windowIcon = topLevelWindow.identifier[0]
            ctx.setFont(Font(family="Helvetica", size=20, weight="bold"))
            ctx.drawString(windowIcon, self.taskBarHeight * 0.23, self.taskBarHeight * 0.1)

            curX += self.taskBarHeight + 1

    def handleTaskBarClicked(self, x):
        topLevelWindows = self.windowSystem.screen.childWindows
        topLevelWindowsSorted = sorted(topLevelWindows, key=lambda win: win.identifier)
        # counter goes through taskbar icons and stops when it reaches the x parameter, so we know which icon was clicked
        xCounter = self.taskBarHeight + 1
        iconIndex = 0
        for i in range(len(topLevelWindows) + 1):
            if xCounter < x:
                xCounter += self.taskBarHeight + 1
                iconIndex += 1

        if iconIndex == 0:
            # quit button was clicked
            quit()
        else:
            # selected window is brought to front or reopened if minimized before
            window = topLevelWindowsSorted[iconIndex-1]
            window.isHidden = False
            self.windowSystem.bringWindowToFront(window)
            self.windowSystem.requestRepaint()

    def handleTitleBarDragged(self, window, x, y, offsetX, offsetY):
        """

        :param window: low-level window which is dragged
        :param x:
        :param y:
        """
        # find top level window this window belongs to
        if window.getTopLevelWindow() is not None:
            topLevelWindow = window.getTopLevelWindow()
        if self.checkWindowPosition(topLevelWindow, x - offsetX, y - offsetY):
            # reposition the window using the absolute position and subtracting the mouse offset
            # (offset is important, so you can click anywhere on the title bar to drag)
            topLevelWindow.x = x - offsetX
            topLevelWindow.y = y - offsetY

    def handleResizeDragged(self, window, width, height):
        topLevelWindow = window.getTopLevelWindow()
        deltaWidth = width - topLevelWindow.width
        deltaHeight = height - topLevelWindow.height
        topLevelWindow.resize(window.x, window.y, width, height)

        for child in topLevelWindow.childWindows:
            self.resizeAnchoredWindow(child, deltaWidth, deltaHeight)

    def resizeAnchoredWindow(self, window, deltaWidth, deltaHeight):
        """
        Resizes windows with anchors to any side (e.g. child windows of top-level windows)
        :param window: Current window to be resized
        :param deltaWidth: Change in width of parent window
        :param deltaHeight: Change in height of parent window
        """
        # store current window anchors to use in the following
        topAnchor = window.layoutAnchors & LayoutAnchor.top
        rightAnchor = window.layoutAnchors & LayoutAnchor.right
        bottomAnchor = window.layoutAnchors & LayoutAnchor.bottom
        leftAnchor = window.layoutAnchors & LayoutAnchor.left

        newParentWidth = window.parentWindow.width + deltaWidth
        newParentHeight = window.parentWindow.height + deltaHeight

        newX, newY, newWidth, newHeight = window.x, window.y, window.width, window.height

        # HORIZONTAL ANCHORING:
        # not anchored to either left or right: keep relative distance to left and right
        if not (leftAnchor or rightAnchor):
            newX += deltaWidth / 2
        # anchored to left and right: resize horizontally
        elif leftAnchor and rightAnchor:
            newWidth += deltaWidth
        # only anchored to right: keep exact distance to the right
        elif rightAnchor:
            newX += deltaWidth

        # VERTICAL ANCHORING:
        # not anchored to either top or bottom: keep relative distance to top and bottom
        if not (topAnchor or bottomAnchor):
            newY += deltaHeight / 2
        # anchored to top and bottom: resize vertically
        elif topAnchor and bottomAnchor:
            newHeight += deltaHeight / 2
        # only anchored to bottom: keep exact distance to bottom
        elif bottomAnchor:
            newY += deltaHeight

        # CONSTRAINTS:

        # if x or y get negative, stick them to left side of window
        if newX < 0:
            newX = 0
        if newY < 0:
            newY = 0
        # minimum size values
        if newWidth < 20:
            width = 20
        if newHeight < 20:
            height = 20

        # if window reaches out of parent on any side, clip it (set hidden)
        window.isHidden = newX + newWidth > newParentWidth or newY + newHeight > newParentHeight

        # resize window with updated values
        window.resize(newX, newY, newWidth, newHeight)

        # resize child windows
        for child in window.childWindows:
            self.resizeAnchoredWindow(child, deltaWidth, deltaHeight)

    def handleTitleBarClicked(self, window):
        """
        Checks which title bar button was pressed and calls respective helper function to execute command.
        :param window: low-level window, which has been clicked on (part of title bar)
        """
        # find top level window this window belongs to
        topLevelWindow = window.getTopLevelWindow()

        # check which part of title bar was pressed exactly
        if "Title Bar - Close Button" in window.identifier:
            self.closeWindow(topLevelWindow)
        elif "Title Bar - Minimize Button" in window.identifier:
            self.minimizeWindow(topLevelWindow)

    def closeWindow(self, window):
        window.removeFromParentWindow()
        self.windowSystem.requestRepaint()

    def minimizeWindow(self, window):
        window.isHidden = True
        window.parentWindow.childWindows.remove(window)
        window.parentWindow.childWindows.insert(0, window)
        self.windowSystem.requestRepaint()

