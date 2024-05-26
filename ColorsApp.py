"""
Window System - Submission
by Felix Umland (#406886)
and Jannick Brändel (#405391)
"""

from UITK import Label, Slider, Container
from Window import Window, LayoutAnchor
from GraphicsEventSystem import *


def rgbToHex(red, green, blue):
    # Ensure the values are within the valid range
    if not (0 <= red <= 1 and 0 <= green <= 1 and 0 <= blue <= 1):
        raise ValueError("RGB values must be in the range [0, 1]")

    # Convert each component to an integer in the range [0, 255]
    r = int(red * 255)
    g = int(green * 255)
    b = int(blue * 255)

    # Format as a hexadecimal string
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return hex_color


class ColorsApp:
    def __init__(self, windowSystem, x, y):
        self.windowSystem = windowSystem
        identifier = "Colors"
        # create app window
        self.appWindow = Window(x,y, 300, 500, self.windowSystem.getInstanceNumber(identifier) + " " + identifier,
                                backgroundColor=COLOR_WHITE)
        # append window as top level window
        self.windowSystem.screen.addChildWindow(self.appWindow)
        # the label that shows the color
        self.hexLabel = None
        # array for the three sliders
        self.sliders = []
        self.drawWidgets()


    def drawWidgets(self):
        # create the three sliders
        for i in range(3):
            slider = Slider(0, 0, self.appWindow.width*0.8, 20, "Slider" + str(i+1),
                            0, self.updateColors,
                            layoutAnchors=LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.right)
            self.sliders.append(slider)
            self.appWindow.addChildWindow(slider)

        slidersAndLabels = []

        # create the three labels and add them to the slidersAndLabels array
        for i in range(3):
            text = ""
            if i == 0:
                text = "RED"
            elif i == 1:
                text = "GREEN"
            elif i == 2:
                text = "BLUE"
            label = Label(0, 0, self.appWindow.width * 0.8, 20, "Label" + str(i + 1), text=text,
                          layoutAnchors=LayoutAnchor.top)
            slidersAndLabels.append(label)
            slidersAndLabels.append(self.sliders[i])
            self.appWindow.addChildWindow(label)

        # Label for displaying color hex value
        self.hexLabel = Label(0, 350, self.appWindow.width * 0.8, 100, "HexLabel", font=Font(family="Helvetica", size=20),
                              fontColor=COLOR_WHITE, text="#000000", layoutAnchors=LayoutAnchor.bottom)
        self.appWindow.addChildWindow(self.hexLabel)
        self.updateColors()

        # Container for the sliders and Labels
        sliderContainer = Container(50, 50, self.appWindow.width * 0.8, 0, "sliderContainer",
                                    layoutAnchors=LayoutAnchor.top, horizontalDist=False, containerWindows=slidersAndLabels,
                                    spacing=10)
        self.appWindow.addChildWindow(sliderContainer)

        # Container Wrapper for sliderContainer and the hexLabel
        elements = [sliderContainer, self.hexLabel]
        wrapperContainer = Container(50, 50, self.appWindow.width * 0.8, self.appWindow.height*0.8, "wrapperContainer",
                                     layoutAnchors=LayoutAnchor.top, horizontalDist=False, containerWindows=elements, spacing=30)
        self.appWindow.addChildWindow(wrapperContainer)


    def updateColors(self):
        # get the current slider values and convert them to a hexadecimal string
        color = rgbToHex(self.sliders[0].sliderValue, self.sliders[1].sliderValue, self.sliders[2].sliderValue)
        # set the text of the label to that string
        self.hexLabel.text = color
        # set the background color of the label accordingly
        self.hexLabel.setBackgroundColor(color)