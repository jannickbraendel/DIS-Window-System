from UITK import Label, Slider, Button, Container
from Window import Window, LayoutAnchor
from GraphicsEventSystem import *

class ResizingApp:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        identifier = "Resizing"
        self.appWindow = Window(400, 120, 300, 300, self.windowSystem.getInstanceNumber(identifier) + " " + identifier)
        self.appWindow.setBackgroundColor(COLOR_WHITE)
        self.windowSystem.screen.addChildWindow(self.appWindow)
        self.drawWindows()

    def drawWindows(self):
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
        allAnchors = Window(115, 135, 70, 40, "all",
                            LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right)
        allAnchors.setBackgroundColor(COLOR_RED)
        grandchild = Window(20, 30, 40, 40, "grandchild", LayoutAnchor.top | LayoutAnchor.bottom)
        grandchild.setBackgroundColor(COLOR_GREEN)

        self.appWindow.addChildWindow(top_left)
        self.appWindow.addChildWindow(top)
        self.appWindow.addChildWindow(top_right)
        self.appWindow.addChildWindow(right)
        self.appWindow.addChildWindow(bottom_right)
        self.appWindow.addChildWindow(bottom)
        self.appWindow.addChildWindow(bottom_left)
        self.appWindow.addChildWindow(left)
        self.appWindow.addChildWindow(allAnchors)

        allAnchors.addChildWindow(grandchild)