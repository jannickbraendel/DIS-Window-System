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
        self.taskBarHeight = 35

    def checkWindowPosition(self, window, x, y):
        # TODO: Check later if function is implemented correctly when handling window-dragging
        # check if window is top-level window and return otherwise
        if window.parentWindow.identifier != "SCREEN":
            pass
        screen = window.parentWindow

        minimumTitleBarVisibility = 6
        titleBarVisibleLeft = x + window.width > 0 + minimumTitleBarVisibility
        titleBarVisibleRight = x - window.width < screen.width - minimumTitleBarVisibility

        titleBarVisibleTop = y + self.titleBarHeight > 0 + minimumTitleBarVisibility
        titleBarVisibleBottom = y - self.titleBarHeight < screen.height - minimumTitleBarVisibility
        # returns true if title bar is visible towards all directions
        return titleBarVisibleLeft and titleBarVisibleRight and titleBarVisibleTop and titleBarVisibleBottom

    # TODO: Title bar only appears after clicking for the first time (children are appended after drawing -> see
    #  Screen.draw())
    def decorateWindow(self, window, ctx):
        # stroke border around window
        ctx.setStrokeColor(COLOR_GRAY)
        startX, startY = window.convertPositionToScreen(0, 0)
        ctx.setOrigin(startX, startY)
        ctx.strokeRect(0, 0, window.width, window.height)
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

        # add title to title Bar
        titleWindow = Window(0, 0, titleBar.width/2, titleBar.height, titleBar.identifier + " - Title")
        titleWindow.setBackgroundColor(titleBar.backgroundColor)
        titleBar.addChildWindow(titleWindow)
        titleWindowX, titleWindowY = titleWindow.convertPositionToScreen(0, 0)
        ctx.setOrigin(titleWindowX, titleWindowY)
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.setFont(Font(family="Helvetica", size=10, weight="bold"))
        ctx.drawString(window.identifier, 3, 1)

        # add buttons windows
        buttonWidth = 10
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
        # draw minimize button
        minButtonX, minButtonY = minimizeButton.convertPositionToScreen(0, 0)
        ctx.setOrigin(minButtonX, minButtonY)
        ctx.drawLine(0, minimizeButton.height/2, buttonWidth, minimizeButton.height/2)
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
        xCounter = self.taskBarHeight + 1
        iconIndex = 0
        for i in range(len(topLevelWindows) + 1):
            if xCounter < x:
                xCounter += self.taskBarHeight + 1
                iconIndex += 1

        if iconIndex == 0:
            quit()
        else:
            window = topLevelWindowsSorted[iconIndex-1]
            window.isHidden = False
            self.windowSystem.bringWindowToFront(window)
            self.windowSystem.requestRepaint()


    def handleTitleBarDragged(self, window, deltaX, deltaY):
        """

        :param window: low-level window which is dragged
        :param x:
        :param y:
        """
        # find top level window this window belongs to
        topLevelWindow = window.getTopLevelWindow()
        if self.checkWindowPosition(topLevelWindow, topLevelWindow.x + deltaX, topLevelWindow.y + deltaY):
            topLevelWindow.x += deltaX
            topLevelWindow.y += deltaY
        else:
            print("out of screen bounds")

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

    @staticmethod
    def closeWindow(window):
        print("Pressed close-button of window", window.identifier)
        window.removeFromParentWindow()

    @staticmethod
    def minimizeWindow(window):
        print("Pressed minimize-button of window", window.identifier)
        window.isHidden = True

