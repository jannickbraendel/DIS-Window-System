#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

import GraphicsEventSystem
from Window import *

class WindowSystem(GraphicsEventSystem):
    def start(self):
        """
        Prepare screen and initialize needed attributes (e.g. mouse-click tolerance).
        """
        # add screen
        self.screen = Screen(self)

        # temporarily save mouse down position to compare with release position
        self.tempMouseDown = (0, 0)
        # amount of pixels the user can move the mouse in between pressing and releasing
        self.mouseClickTolerance = 2

        # add a few test windows
        window1 = Window(20, 20, 80, 80, "1")
        window1.setBackgroundColor(COLOR_GREEN)
        window2 = Window(40, 40, 80, 80, "2")
        window2.setBackgroundColor(COLOR_BLUE)
        window3 = Window(20, 20, 40, 40, "3")
        window3.setBackgroundColor(COLOR_ORANGE)
        window2.addChildWindow(window3)
        self.screen.addChildWindow(window1)
        self.screen.addChildWindow(window2)

    
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
        Specified window is brought to front in z-level direction. It is removed from its original parent window and
        added as a child to the screen
        :param window: window to be brought to front
        """
        # remove the parent
        window.removeFromParentWindow()
        # calculate new position
        window.x, window.y = window.convertPositionToScreen(window.x, window.y)
        # add window as top level window
        self.screen.addChildWindow(window)


    """
    DRAWING
    """
    
    def handlePaint(self):
        """
        Repaint the screen by calling the draw function.
        """
        self.screen.draw(self.graphicsContext)
    
    
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
            self.bringWindowToFront(child)
            self.handlePaint()
        
    def handleMouseReleased(self, x, y):
        """
        When the left mouse button is released, check if mouse click occurred and send event to respective child window.
        :param x: x value of mouse position when released
        :param y: y value of mouse position when released
        """
        # calculate distance between release and pressed position
        deltaX, deltaY = abs(self.tempMouseDown[0] - x), abs(self.tempMouseDown[1] - y)
        # if distance is less than mouseClickTolerance send mouse-click event to child where click occurred.
        if deltaX <= self.mouseClickTolerance and deltaY <= self.mouseClickTolerance:
            child = self.screen.childWindowAtLocation(x, y)
            if child:
                child.handleMouseClicked(x, y)

    def handleMouseMoved(self, x, y):
        pass
        
    def handleMouseDragged(self, x, y):
        pass
        
    def handleKeyPressed(self, char):
        pass
        
    
    
        
    
# Let's start your window system!
w = WindowSystem(800,600)