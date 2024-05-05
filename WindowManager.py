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
        # TODO: Check later if function is implemented correctly when handling window-dragging
        # check if window is top-level window and return otherwise
        if window.parentWindow.identifier != "SCREEN":
            pass
        screen = window.parentWindow

        minimumTitleBarVisibility = 6
        titleBarVisibleLeft = x + window.width > 0 + minimumTitleBarVisibility + (3 * self.titleBarButtonWidth)
        titleBarVisibleRight = x < screen.width - minimumTitleBarVisibility

        titleBarVisibleTop = y > 0
        titleBarVisibleBottom = y < screen.height - minimumTitleBarVisibility
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
        # remove old title bar if already existing
        if len(window.childWindows) > 1 and "- Title Bar" in window.childWindows[len(window.childWindows) - 2].identifier:
            window.childWindows[len(window.childWindows) - 2].removeFromParentWindow()

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
        # store current window anchors to use in the following
        topAnchor = window.layoutAnchors & LayoutAnchor.top
        rightAnchor = window.layoutAnchors & LayoutAnchor.right
        bottomAnchor = window.layoutAnchors & LayoutAnchor.bottom
        leftAnchor = window.layoutAnchors & LayoutAnchor.left

        windowOrigin = window.convertPositionToScreen(0, 0)
        parentOrigin = window.parentWindow.convertPositionToScreen(0, 0)

        newX, newY, newWidth, newHeight = window.x, window.y, window.width, window.height

        # go through anchor combinations and change coordinates and width/height accordingly
        if topAnchor and rightAnchor and bottomAnchor and leftAnchor:
            newWidth += deltaWidth
            newHeight += deltaHeight

        elif topAnchor and rightAnchor:
            # window is only moved on x-axis by the width delta of the parent
            if newX + deltaWidth >= 0:
                newX += deltaWidth

        elif topAnchor and leftAnchor:
            pass

        elif bottomAnchor and rightAnchor:
            # window is moved on x- and y-axis by the width/height delta of the parent
            if newX + deltaWidth >= 0:
                newX += deltaWidth
            if newY + deltaHeight >= 0:
                newY += deltaHeight

        elif bottomAnchor and leftAnchor:
            if newY + deltaHeight >= 0:
                newY += deltaHeight

        elif topAnchor:
            # window keeps distance to left and right and does not change height
            newX += deltaWidth / 2

        elif bottomAnchor:
            # window keeps distance to left and moves on y-axis by height delta of parent
            newX += deltaWidth / 2
            if newY + deltaHeight >= 0:
                newY += deltaHeight

        elif rightAnchor:
            # window keeps distance to top and bottom and moves on x-axis by width delta of parent
            newY += deltaHeight / 2
            if newX + deltaWidth >= 0:
                newX += deltaWidth

        elif leftAnchor:
            # window keeps distance to top and bottom
            newY += deltaHeight / 2

        window.resize(newX, newY, newWidth, newHeight)

        '''
        # resize child windows
        for child in window.childWindows:
            self.resizeAnchoredWindow(child, factorWidth, factorHeight)
        '''

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
        print("Pressed close-button of window", window.identifier)
        window.removeFromParentWindow()
        self.windowSystem.requestRepaint()

    def minimizeWindow(self, window):
        print("Pressed minimize-button of window", window.identifier)
        window.isHidden = True
        window.parentWindow.childWindows.remove(window)
        window.parentWindow.childWindows.insert(0, window)
        self.windowSystem.requestRepaint()

