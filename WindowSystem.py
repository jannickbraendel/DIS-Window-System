#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by Felix Umland (#406886)
and Jannick Brändel (#405391)
"""

import GraphicsEventSystem
from Window import *
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
        # getting new title bar)
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

        # add a few test windows
        containerTest = Window(80, 80, 280, 280, "Container Test")
        containerTest.setBackgroundColor(COLOR_WHITE)
        window2 = Window(40, 40, 250, 250, "Second Window")
        window2.setBackgroundColor(COLOR_WHITE)
        window3 = Window(20, 20, 40, 40, "3")
        window3.setBackgroundColor(COLOR_ORANGE)
        # test resizing
        resizing = Window(400, 120, 300, 300, "Resizing Test")
        # resizing.setBackgroundColor(COLOR_WHITE)
        top_left = Window(15, 25, 70, 40, "top-left")
        top_left.setBackgroundColor(COLOR_GREEN)
        top = Window(115, 25, 70, 40, "top", LayoutAnchor.top)
        top.setBackgroundColor(COLOR_ORANGE)
        top_right = Window(215, 25, 70, 40, "top-right", LayoutAnchor.top | LayoutAnchor.right)
        top_right.setBackgroundColor(COLOR_GREEN)
        right = Window(215, 135, 70, 40, "right", LayoutAnchor.right)
        right.setBackgroundColor(COLOR_PURPLE)
        bottom_right = Window(215, 245, 70, 40, "bottom-right", LayoutAnchor.bottom | LayoutAnchor.right)
        bottom_right.setBackgroundColor(COLOR_PINK)
        bottom = Window(115, 245, 70, 40, "bottom", LayoutAnchor.bottom)
        bottom.setBackgroundColor(COLOR_BLACK)
        bottom_left = Window(15, 245, 70, 40, "bottom-left", LayoutAnchor.bottom | LayoutAnchor.left)
        bottom_left.setBackgroundColor(COLOR_BROWN)
        left = Window(15, 135, 70, 40, "left", LayoutAnchor.left)
        left.setBackgroundColor(COLOR_PURPLE)
        allAnchors = Window(115, 135, 70, 40, "all", LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right)
        allAnchors.setBackgroundColor(COLOR_RED)
        grandchild = Window(20, 30, 40, 40, "grandchild", LayoutAnchor.top | LayoutAnchor.bottom)
        grandchild.setBackgroundColor(COLOR_GREEN)
        # print(window1.convertPositionFromScreen(30,30))
        self.screen.addChildWindow(containerTest)
        self.screen.addChildWindow(window2)
        self.screen.addChildWindow(resizing)
        window2.addChildWindow(window3)
        label = Label(40, 40, 30, 20, "Label1", LayoutAnchor.top, "Hello World", fontColor=COLOR_RED)
        label.setBackgroundColor(COLOR_BLUE)
        window2.addChildWindow(label)
        button = Button(69, 69, 70,30, "Button", LayoutAnchor.right, "MyButton", COLOR_LIGHT_GRAY, COLOR_GRAY)
        button.setBackgroundColor(COLOR_ORANGE)
        window2.addChildWindow(button)
        slider = Slider(20,200, 200, 20, "Slider", LayoutAnchor.bottom)
        slider.setBackgroundColor(COLOR_GRAY)
        window2.addChildWindow(slider)

        resizing.addChildWindow(top_left)
        resizing.addChildWindow(top)
        resizing.addChildWindow(top_right)
        resizing.addChildWindow(right)
        resizing.addChildWindow(bottom_right)
        resizing.addChildWindow(bottom)
        resizing.addChildWindow(bottom_left)
        resizing.addChildWindow(left)
        resizing.addChildWindow(allAnchors)

        allAnchors.addChildWindow(grandchild)

        # container test:
        conWin1 = Window(0, 0, 40, 20, "conWin1", layoutAnchors=LayoutAnchor.top)
        conWin1.setBackgroundColor(COLOR_BLUE)
        conWin2 = Window(0, 0, 40, 30, "conWin2", layoutAnchors=LayoutAnchor.top)
        conWin2.setBackgroundColor(COLOR_ORANGE)
        conWin3 = Window(0, 0, 40, 40, "conWin3", layoutAnchors=LayoutAnchor.top)
        conWin3.setBackgroundColor(COLOR_GREEN)
        conWin4 = Window(0, 0, 40, 20, "conWin4", layoutAnchors=LayoutAnchor.top)
        conWin4.setBackgroundColor(COLOR_YELLOW)

        container = Container(40, 40, 200, 100, "Container Test", LayoutAnchor.top, [conWin1, conWin2, conWin3, conWin4], spacing=10, horizontalDist=False)
        container.setBackgroundColor(COLOR_CLEAR)
        containerTest.addChildWindow(conWin1)
        containerTest.addChildWindow(conWin2)
        containerTest.addChildWindow(conWin3)
        containerTest.addChildWindow(conWin4)
        containerTest.addChildWindow(container)
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
        Repaint the screen by calling the draw function.
        """
        self.screen.draw(self.graphicsContext)
        self.windowManager.drawTaskbar(self.graphicsContext)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        """
        When the left mouse button is pressed, bring selected window to front and repaint the screen.
        :param x: x value of mouse position when pressed
        :param y: y value of mouse position when pressed
        """
        # save mouse position to check when button is released
        self.tempMouseDown = (x, y)
        child = self.screen.childWindowAtLocation(x, y)
        if child:
            if child.identifier == "SCREEN":
                return
            self.bringWindowToFront(child)
            # check if button was pressed and change its state accordingly
            if isinstance(child,Button):
                child.changeState("PRESSED")
                self.requestRepaint()
            elif isinstance(child, Slider):
                child.changeState("PRESSED")
                localX, _ = child.convertPositionFromScreen(x, y)
                child.changeSlider(localX)
                self.requestRepaint()
            # save which window was pressed for dragging
            self.tempMouseDownWindow = child
            # get the top level window and calculate the offset between the window origin and
            # where the mouse clicked the title bar (only used for dragging)
            topLevelWindow = child.getTopLevelWindow()
            # save top level window for dragging (to get updated child windows (e.g. title bar))
            self.tempMouseDownTLWindow = topLevelWindow
            self.tempMouseDragOffset = x - topLevelWindow.x, y - topLevelWindow.y
            self.tempMouseDownDimensions = topLevelWindow.width, topLevelWindow.height

            if x > topLevelWindow.x + topLevelWindow.width - self.windowManager.resizeCornerTolerance and y > topLevelWindow.y + topLevelWindow.height - self.windowManager.resizeCornerTolerance:
                self.tempMouseDownResizing = True

    def handleMouseReleased(self, x, y):
        """
        When the left mouse button is released, check if mouse click occurred and send event to respective child
        window OR window manager if title bar was clicked.
        :param x: x value of mouse position when released
        :param y: y value of mouse position when released
        """
        self.tempMouseDownWindow = None
        self.tempMouseDownTLWindow = None
        self.tempMouseDownResizing = False
        # calculate distance between release and pressed position
        deltaX, deltaY = abs(self.tempMouseDown[0] - x), abs(self.tempMouseDown[1] - y)
        # if distance is less than mouseClickTolerance send mouse-click event to child where click occurred.
        if deltaX <= self.mouseClickTolerance and deltaY <= self.mouseClickTolerance:
            if y >= self.height - self.windowManager.taskBarHeight:
                # task bar was clicked
                self.windowManager.handleTaskBarClicked(x)
            else:
                clickedWindow = self.screen.childWindowAtLocation(x, y)
                if clickedWindow:
                    if "- Title Bar" in clickedWindow.identifier:
                        # title bar was clicked
                        self.windowManager.handleTitleBarClicked(clickedWindow)
                    else:
                        clickedWindow.handleMouseClicked(x, y)
                        self.requestRepaint()

    def handleMouseMoved(self, x, y):
        hoveredWindow = self.screen.childWindowAtLocation(x, y)
        if hoveredWindow is None:
            return

        if isinstance(hoveredWindow, Button):
            hoveredWindow.changeState("HOVERED")
        else:
            if isinstance(self.tempHoveredWindow, Button):
                self.tempHoveredWindow.changeState("NORMAL")

        self.tempHoveredWindow = hoveredWindow
        self.requestRepaint()

    def handleMouseDragged(self, x, y):
        clickedX, clickedY = self.tempMouseDown
        if self.tempMouseDownWindow is None:
            return
        window = self.tempMouseDownWindow
        # calculate the delta between the originally clicked position and the current drag position
        deltaX, deltaY = x - clickedX, y - clickedY

        if isinstance(window, Slider):
            window.changeState("PRESSED")
            localX, _ = window.convertPositionFromScreen(x, y)
            window.changeSlider(localX)
            self.requestRepaint()

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
        pass


# Let's start your window system!
w = WindowSystem(800, 600)
