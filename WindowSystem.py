#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by Felix Umland (#406886)
and Jannick Brändel (#405391)
"""
import GraphicsEventSystem
import re
from WindowManager import WindowManager
from UITK import *


class WindowSystem(GraphicsEventSystem):
    def start(self):
        """
        Prepare screen and initialize needed attributes (e.g. mouse-click tolerance).
        """
        # add window manager
        self.windowManager = WindowManager(self)
        # add screen
        self.screen = Screen(self)
        # temporarily save mouse down position to compare with release position or handle mouse dragging
        self.tempMouseDown = (0, 0)
        # temporarily save the window that the mouse down event happened on, used for dragging
        self.tempMouseDownWindow = None
        # temporarily save the TOP-LEVEL window that the mouse down event happened on, used for dragging (especially
        # getting updated child windows e.g. title bar)
        self.tempMouseDownTLWindow = None
        # temporarily save the offset with which a window's title bar was clicked, used for dragging
        self.tempMouseDragOffset = (0, 0)
        # temporarily save the dimensions of the window on mouse down
        self.tempMouseDownDimensions = (0, 0)
        # set a boolean, when this is true the bottom right corner was pressed for resizing
        self.tempMouseDownResizing = False
        # temporarily save hovered window to compare in next hovering event (used for buttons)
        self.tempHoveredWindow = None
        # amount of pixels the user can move the mouse in between pressing and releasing
        self.mouseClickTolerance = 2
        # list of apps
        self.apps = []
    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        """
        Create a new window on screen and return it
        :param x: x value of the window's origin
        :param y: y value of the window's origin
        :param width: window width
        :param height: window height
        :param identifier: window id
        :return: created window
        """
        window = Window(x, y, width, height, identifier)
        # window is displayed on screen
        self.screen.addChildWindow(window)
        return window

    def bringWindowToFront(self, window):
        """
        Find top-level window the specified window is a child of and bring it to front.
        :param window: window which was selected.
        """
        # if screen is clicked don't bring it to front
        if window.parentWindow is None:
            return

        # find top level window this window belongs to
        topLevelWindow = window.getTopLevelWindow()

        # calculate new position
        topLevelWindow.x, topLevelWindow.y = topLevelWindow.convertPositionToScreen(0, 0)
        # remove the parent
        topLevelWindow.removeFromParentWindow()
        # add window as top level window
        self.screen.addChildWindow(topLevelWindow)

    """
    DRAWING
    """

    def handlePaint(self):
        """
        Repaint the screen, taskbar and start menu by calling the draw function.
        """
        self.screen.draw(self.graphicsContext)
        self.windowManager.drawTaskbar(self.graphicsContext)
        if self.windowManager.startMenuVisible:
            self.windowManager.drawStartMenu(self.graphicsContext)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        """
        When the left mouse button is pressed, bring selected window to front, update buttons and sliders,
        update temp variables for dragging and repaint the screen.
        :param x: x value of mouse position when pressed
        :param y: y value of mouse position when pressed
        """
        # save mouse position to check when button is released
        self.tempMouseDown = (x, y)

        # check if the start menu was clicked
        if (self.windowManager.startMenuVisible and x <= self.windowManager.startMenuWidth
                and self.height - self.windowManager.startMenuHeight - self.windowManager.taskBarHeight <= y <= self.height - self.windowManager.taskBarHeight):
            # start menu was pressed
            return

        # check if the taskbar was clicked
        if y >= self.height - self.windowManager.taskBarHeight:
            # task bar was clicked, do nothing
            return
        # check which window was pressed
        child = self.screen.childWindowAtLocation(x, y)
        if child:
            if child.identifier == "SCREEN":
                return
            self.bringWindowToFront(child)
            # check if button was pressed and change its state accordingly
            if isinstance(child,Button):
                child.changeState("PRESSED")
                self.requestRepaint()
            # check if slider was pressed and change its state accordingly
            elif isinstance(child, Slider):
                child.changeState("PRESSED")
                localX, _ = child.convertPositionFromScreen(x, y)
                child.changeSlider(localX)
                self.requestRepaint()

            # DRAGGING TEMP VARIABLES
            # save which window was pressed for dragging
            self.tempMouseDownWindow = child
            # get the top level window and calculate the offset between the window origin and
            # where the mouse clicked the title bar (only used for dragging)
            topLevelWindow = child.getTopLevelWindow()
            # save top level window for dragging (to get updated child windows (e.g. title bar))
            self.tempMouseDownTLWindow = topLevelWindow
            self.tempMouseDragOffset = x - topLevelWindow.x, y - topLevelWindow.y
            self.tempMouseDownDimensions = topLevelWindow.width, topLevelWindow.height

            # check if resizing icon in bottom left of window was pressed
            if x > topLevelWindow.x + topLevelWindow.width - self.windowManager.resizeCornerTolerance and y > topLevelWindow.y + topLevelWindow.height - self.windowManager.resizeCornerTolerance:
                self.tempMouseDownResizing = True

    def handleMouseReleased(self, x, y):
        """
        When the left mouse button is released, check if mouse click occurred and send event to respective child
        window OR window manager if title bar was clicked.
        :param x: x value of mouse position when released
        :param y: y value of mouse position when released
        """
        # calculate distance between release and pressed position
        deltaX, deltaY = abs(self.tempMouseDown[0] - x), abs(self.tempMouseDown[1] - y)
        # if distance is less than mouseClickTolerance send mouse-click event to child where click occurred.
        if deltaX <= self.mouseClickTolerance and deltaY <= self.mouseClickTolerance:
            # check if taskbar is clicked (without checking the start menu)
            if y >= self.height - self.windowManager.taskBarHeight:
                # task bar was clicked
                self.windowManager.handleTaskBarClicked(x)
            elif (self.windowManager.startMenuVisible and x <= self.windowManager.startMenuWidth
                  and self.height - self.windowManager.startMenuHeight - self.windowManager.taskBarHeight <= y <= self.height - self.windowManager.taskBarHeight):
                # start menu was clicked
                self.windowManager.handleStartMenuClicked(y)
            else:
                # hide start menu again if it is open
                if self.windowManager.startMenuVisible:
                    self.windowManager.startMenuVisible = False
                clickedWindow = self.screen.childWindowAtLocation(x, y)
                # handle clicking of a window's title bar or click inside window
                if clickedWindow:
                    if "- Title Bar" in clickedWindow.identifier:
                        # title bar was clicked
                        self.windowManager.handleTitleBarClicked(clickedWindow)
                    else:
                        clickedWindow.handleMouseClicked(x, y)
                        self.requestRepaint()

        # Slider update
        if isinstance(self.tempMouseDownWindow, Slider):
            self.tempMouseDownWindow.changeState("NORMAL")

        # reset temp variables
        self.tempMouseDownWindow = None
        self.tempMouseDownTLWindow = None
        self.tempMouseDownResizing = False

    def handleMouseMoved(self, x, y):
        hoveredWindow = self.screen.childWindowAtLocation(x, y)
        # check if start menu is hovered
        if (self.windowManager.startMenuVisible and x <= self.windowManager.startMenuWidth
                and self.height - self.windowManager.startMenuHeight - self.windowManager.taskBarHeight <= y <= self.height - self.windowManager.taskBarHeight):
            # start menu was hovered, now highlight the element at that location
            self.windowManager.handleStartMenuHovered(y)
        if isinstance(hoveredWindow, Button):
            # mouse is moved over a button -> change its state to HOVERED
            hoveredWindow.changeState("HOVERED")
        elif isinstance(self.tempHoveredWindow, Button):
            # mouse moved away from button -> change its state to NORMAL
            self.tempHoveredWindow.changeState("NORMAL")
        if self.tempHoveredWindow != hoveredWindow:
            if isinstance(self.tempHoveredWindow, Button):
                # make sure that the last hovered window is set to normal again
                # this makes sure that fast mouse movements don't create several hovered buttons
                self.tempHoveredWindow.changeState("NORMAL")

        self.tempHoveredWindow = hoveredWindow
        self.requestRepaint()

    def handleMouseDragged(self, x, y):
        # position of last MousePressed event
        clickedX, clickedY = self.tempMouseDown
        if self.tempMouseDownWindow is None:
            return
        # window where last MousePressed event occurred on
        window = self.tempMouseDownWindow
        # calculate the delta between the originally clicked position and the current drag position
        deltaX, deltaY = x - clickedX, y - clickedY

        # update slider while it is dragged (if current window is a slider)
        if isinstance(window, Slider):
            window.changeState("PRESSED")
            localX, _ = window.convertPositionFromScreen(x, y)
            window.changeSlider(localX)
            self.requestRepaint()

        # if window is resized, send resized event to WM and let it resize the window
        if self.tempMouseDownResizing:
            self.windowManager.handleResizeDragged(
                window,
                self.tempMouseDownDimensions[0] + deltaX,
                self.tempMouseDownDimensions[1] + deltaY
            )

        if "- Title Bar" in window.identifier and "Button" not in window.identifier:
            # title bar is dragged but not title bar buttons
            # reposition the window with the absolute position and mouse offset
            self.windowManager.handleTitleBarDragged(
                self.tempMouseDownTLWindow,
                clickedX + deltaX,
                clickedY + deltaY,
                self.tempMouseDragOffset[0],
                self.tempMouseDragOffset[1]
            )

    def handleKeyPressed(self, char):
        if len(self.screen.childWindows) == 0:
            # no app is opened, key presses should not do anything here
            return
        # focused window is last element of child window array (at z-level in front)
        focusedWindow = self.screen.childWindows[-1]
        # search apps that are currently opened for calculator
        for app in self.apps:
            if "Calculator" in app.appWindow.identifier and focusedWindow.identifier == app.appWindow.identifier:
                # focused app is Calculator -> pass key input to that app window
                if char == "A":
                    # pressing A should result in AllClear
                    char = "AC"
                if char == "n":
                    # pressing n should result in +/- (negate)
                    char = "+/-"
                # pass key input
                app.handleInput(char)

    # When opening a new instance of an app, this function will be called
    # it returns a unique instance number that is then used for the identifier
    def getInstanceNumber(self, appName):
        openInstances = 0
        # check if the window is already open
        for app in reversed(self.apps):
            if appName in app.appWindow.identifier:
                # find the highest instance number of this app
                openInstances = int(re.findall("[0-9]+", app.appWindow.identifier)[0])
                break
        return str(openInstances + 1)


# Let's start your window system!
w = WindowSystem(1600, 800)
