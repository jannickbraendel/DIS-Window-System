#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Felix Umland (#406886)
and Jannick Brändel (#405391)
"""
from ColorsApp import ColorsApp
from CalculatorApp import CalculatorApp
from GraphicsEventSystem import *
from ResizingApp import ResizingApp
from Window import *
from HelloWorldApp import HelloWorldApp


class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.titleBarHeight = 18
        self.titleBarButtonWidth = 10
        self.taskBarHeight = 35
        self.resizeCornerTolerance = 8
        self.tlwMinWidth = 3 * self.titleBarButtonWidth + 50
        self.tlwMinHeight = self.titleBarHeight + 10

        # Start Menu Variables
        self.startMenuVisible = False
        self.apps = ["Hello World", "Colors", "Calculator", "Resizing", "Shutdown"]
        # height of a single element in the start menu
        self.startMenuItemHeight = 50
        self.startMenuItemHovered = None
        # set size of the start menu
        self.startMenuWidth = 200
        self.startMenuHeight = len(self.apps * self.startMenuItemHeight)


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
        ctx.setFillColor("#BDBDBD")
        ctx.setStrokeColor(COLOR_GRAY)
        ctx.fillRect(0, 0, self.windowSystem.width, self.taskBarHeight)
        ctx.strokeRect(0, 0, self.windowSystem.width, self.taskBarHeight)

        # draw start menu button
        # ctx.setFillColor("#BDBDBD")
        # ctx.fillRect(0, 0, self.taskBarHeight, self.taskBarHeight)
        # Add button stroke
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.drawLine(0, 0, self.taskBarHeight, 0)
        ctx.drawLine(0, 0, 0, self.taskBarHeight)

        ctx.setStrokeColor(COLOR_BLACK)
        ctx.drawLine(0, self.taskBarHeight, self.taskBarHeight, self.taskBarHeight)
        ctx.drawLine(self.taskBarHeight, 0, self.taskBarHeight, self.taskBarHeight)

        # Add start menu icon
        ctx.setFillColor(COLOR_RED)
        ctx.fillRect(self.taskBarHeight/4, self.taskBarHeight/4, self.taskBarHeight/2, self.taskBarHeight/2)
        ctx.setFillColor(COLOR_GREEN)
        ctx.fillRect(self.taskBarHeight/2, self.taskBarHeight / 4, self.taskBarHeight / 4 * 3, self.taskBarHeight / 2)
        ctx.setFillColor(COLOR_BLUE)
        ctx.fillRect(self.taskBarHeight/4, self.taskBarHeight / 2, self.taskBarHeight / 2, self.taskBarHeight / 4 * 3)
        ctx.setFillColor(COLOR_YELLOW)
        ctx.fillRect(self.taskBarHeight / 2, self.taskBarHeight / 2, self.taskBarHeight / 4 * 3, self.taskBarHeight / 4 * 3)

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
        # todo: clicking taskbar where there is no item leads to an exception
        if iconIndex == 0:
            # start menu button was clicked
            self.startMenuVisible = not self.startMenuVisible
        else:
            # selected window is brought to front or reopened if minimized before
            window = topLevelWindowsSorted[iconIndex-1]
            window.isHidden = False
            self.windowSystem.bringWindowToFront(window)
            self.windowSystem.requestRepaint()

    def drawStartMenu(self, ctx):
        startMenuOriginY = self.windowSystem.height-self.taskBarHeight-self.startMenuHeight
        iconSize = 35
        itemSpacing = 10

        # background
        ctx.setOrigin(0, startMenuOriginY)
        ctx.setFillColor("#BDBDBD")
        ctx.fillRect(0, 0, self.startMenuWidth, self.startMenuHeight)

        for i in range(len(self.apps)):
            # Item Area
            # Only draw if item i is hovered
            if self.startMenuItemHovered == i:
                ctx.setFillColor("#030280")
                y = (i * self.startMenuItemHeight)
                ctx.fillRect(0, y, self.startMenuWidth, y + self.startMenuItemHeight)

            # App Icon
            # ctx.setFillColor(COLOR_RED)
            # x = itemSpacing
            # y = i * self.startMenuItemHeight + (self.startMenuItemHeight - iconSize) / 2
            # ctx.fillRect(x, y, x + iconSize, y + iconSize)

            self.drawStartMenuIcon(i, ctx)

            # App String
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.setFont(Font(family="Helvetica", size=20, weight="bold"))
            ctx.drawString(self.apps[i], itemSpacing * 2 + iconSize, i * self.startMenuItemHeight + self.startMenuItemHeight / 4)

    def drawStartMenuIcon(self, i, ctx):
        startMenuOriginY = self.windowSystem.height - self.taskBarHeight - self.startMenuHeight
        iconSize = 35
        itemSpacing = 10
        x = itemSpacing
        y = i * self.startMenuItemHeight + (self.startMenuItemHeight - iconSize) / 2
        ctx.setStrokeColor(COLOR_WHITE)
        if i == 0:
            # Hello World App
            ctx.setFillColor("#E0E081")
            ctx.fillRect(x, y, x + iconSize, y + iconSize)
            ctx.setFont(Font(family="Helvetica", size=25, weight="bold"))
            ctx.drawString("H",x + 7, y + 5)
        elif i == 1:
            # Colors APP
            ctx.setFillColor("#404040")
            ctx.fillRect(x, y, x + iconSize, y + iconSize)
            # red line
            ctx.setFillColor("#D80000")
            ctx.fillRect(x + 10, y + 5, x + 25, y + 10)
            # green line
            ctx.setFillColor("#0EB102")
            ctx.fillRect(x + 10, y + 15, x + 25, y + 20)
            # blue line
            ctx.setFillColor("#0001F8")
            ctx.fillRect(x + 10, y + 25, x + 25, y + 30)
        elif i == 2:
            # Calculator App
            # Background
            ctx.setFillColor("#FE9F0B")
            ctx.fillRect(x, y, x + iconSize, y + iconSize)
            ctx.setFillColor(COLOR_WHITE)
            # Top dot
            ctx.fillRect(x + 12.5, y + 5, x + 21, y + 12.5)
            # Middle Line
            ctx.fillRect(x + 5, y + 15, x + 30, y + 20)
            # Bottom dot
            ctx.fillRect(x + 12.5, y + 22.5, x + 21, y + 30)
        elif i == 3:
            # Resizing App
            # Background
            ctx.setFillColor("#04DDF9")
            ctx.fillRect(x, y, x + iconSize, y + iconSize)
            ctx.setFillColor(COLOR_WHITE)
            # Top Left Bracket
            ctx.fillRect(x + 5, y + 5, x+20, y + 10)
            ctx.fillRect(x + 5, y + 5, x+10, y + 20)
            # Bottom Right Bracket
            ctx.fillRect(x + 15, y + 25, x + 30, y + 30)
            ctx.fillRect(x + 25, y + 15, x + 30, y + 30)
        elif i == 4:
            # Quit Button
            ctx.setFillColor(COLOR_RED)
            ctx.fillRect(x, y, x + iconSize, y + iconSize)
            ctx.drawLine(x + 5, y + 5, x + 30, y + 30)
            ctx.drawLine(x+ 30, y + 5, x + 5, y + 30)


    def handleStartMenuClicked(self, y):
        item = self.startMenuItemAtY(y)
        if item == 0:
            HelloWorldApp(self.windowSystem)
        elif item == 1:
            ColorsApp(self.windowSystem)
        elif item == 2:
            CalculatorApp(self.windowSystem)
        elif item == 3:
            ResizingApp(self.windowSystem)
        elif item == 4:
            quit()

    def handleStartMenuHovered(self, y):
        self.startMenuItemHovered = self.startMenuItemAtY(y)

    def startMenuItemAtY(self, y):
        startMenuOriginY = self.windowSystem.height - self.taskBarHeight - self.startMenuHeight
        relativeY = y - startMenuOriginY

        return int(relativeY / self.startMenuItemHeight)



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
        topLevelWindow.resize(topLevelWindow.x, topLevelWindow.y, width, height)
        self.windowSystem.requestRepaint()

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

