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
        self.resizeCornerTolerance = 8
        self.tlwMinWidth = 3 * self.titleBarButtonWidth + 50
        self.tlwMinHeight = self.titleBarHeight + 10

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
        if window.width > 100:
            # draw full title as window is wide enough
            ctx.drawString(window.identifier, 3, 1)
        else:
            # draw first letters of identifier
            ctx.drawString(window.identifier[:3], 3, 1)

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
        # draw resizing area in bottom right corner
        distResizeLines = self.resizeCornerTolerance/2
        ctx.setStrokeColor(COLOR_BLACK)
        for i in range(2):
            ctx.setOrigin(startX + window.width - self.resizeCornerTolerance + i * distResizeLines,
                          startY + window.height)
            ctx.drawLine(0, 0, 0, -self.resizeCornerTolerance + i * distResizeLines)
            ctx.drawLine(0, -self.resizeCornerTolerance + i * distResizeLines, self.resizeCornerTolerance - i * distResizeLines,
                         -self.resizeCornerTolerance + i * distResizeLines)

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
        if window.getTopLevelWindow() is None:
            return
        topLevelWindow = window.getTopLevelWindow()
        if self.checkWindowPosition(topLevelWindow, x - offsetX, y - offsetY):
            # reposition the window using the absolute position and subtracting the mouse offset
            # (offset is important, so you can click anywhere on the title bar to drag)
            topLevelWindow.x = x - offsetX
            topLevelWindow.y = y - offsetY

    def handleResizeDragged(self, window, width, height):
        topLevelWindow = window.getTopLevelWindow()
        topLevelWindow.resize(topLevelWindow.x, topLevelWindow.y, width - topLevelWindow.width, height - topLevelWindow.height)

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

