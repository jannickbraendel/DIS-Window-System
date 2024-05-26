from Window import Window, LayoutAnchor
from GraphicsEventSystem import *


class ResizingApp:
    def __init__(self, windowSystem, x, y):
        self.windowSystem = windowSystem
        identifier = "Resizing"
        self.appWindow = Window(x, y, 300, 300, self.windowSystem.getInstanceNumber(identifier) + " " + identifier,
                                backgroundColor=COLOR_WHITE)
        self.windowSystem.screen.addChildWindow(self.appWindow)
        self.drawWindows()

    def drawWindows(self):
        top_left = Window(15, 25, 70, 40, "top-left", backgroundColor=COLOR_GREEN)
        top = Window(115, 25, 70, 40, "top", LayoutAnchor.top, backgroundColor=COLOR_ORANGE)
        top_right = Window(215, 25, 70, 40, "top-right", LayoutAnchor.top | LayoutAnchor.right,
                           backgroundColor=COLOR_GREEN)
        right = Window(215, 135, 70, 40, "right", LayoutAnchor.right, backgroundColor=COLOR_PURPLE)
        bottom_right = Window(215, 245, 70, 40, "bottom-right", LayoutAnchor.bottom | LayoutAnchor.right,
                              backgroundColor=COLOR_PINK)
        bottom = Window(115, 245, 70, 40, "bottom", LayoutAnchor.bottom, backgroundColor=COLOR_BLACK)
        bottom_left = Window(15, 245, 70, 40, "bottom-left", LayoutAnchor.bottom | LayoutAnchor.left,
                             backgroundColor=COLOR_BROWN)
        left = Window(15, 135, 70, 40, "left", LayoutAnchor.left, backgroundColor=COLOR_PURPLE)
        allAnchors = Window(115, 135, 70, 40, "all",
                            LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right,
                            backgroundColor=COLOR_RED)
        grandchild = Window(20, 30, 40, 40, "grandchild", LayoutAnchor.top | LayoutAnchor.bottom,
                            backgroundColor=COLOR_GREEN)

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
