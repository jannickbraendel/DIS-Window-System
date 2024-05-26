from UITK import Label, Slider, Button, Container
from Window import Window, LayoutAnchor
from GraphicsEventSystem import *


def rgb_to_hex(red, green, blue):
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
        self.appWindow = Window(x,y, 300, 500, self.windowSystem.getInstanceNumber(identifier) + " " + identifier)
        self.appWindow.setBackgroundColor(COLOR_WHITE)
        self.windowSystem.screen.addChildWindow(self.appWindow)
        self.hexLabel = None

        self.sliders = []
        self.drawWidgets()


    def drawWidgets(self):
        # Sliders
        for i in range(3):
            slider = Slider(0, 0, self.appWindow.width*0.8, 20, "Slider" + str(i+1),
                        LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.right, 0, self.updateColors)
            self.sliders.append(slider)
            self.appWindow.addChildWindow(slider)

        slidersAndLabels = []

        for i in range(3):
            text = ""
            if i == 0:
                text = "RED"
            elif i == 1:
                text = "GREEN"
            elif i == 2:
                text = "BLUE"
            label = Label(0, 0, self.appWindow.width * 0.8, 20, "Label" + str(i + 1), LayoutAnchor.top, text)
            slidersAndLabels.append(label)
            slidersAndLabels.append(self.sliders[i])
            self.appWindow.addChildWindow(label)

        # Label for displaying color hex value
        self.hexLabel = Label(0, 350, self.appWindow.width * 0.8, 100, "HexLabel", font=Font(family="Helvetica", size=20),
                              fontColor=COLOR_WHITE, text="#000000", layoutAnchors=LayoutAnchor.bottom)
        self.appWindow.addChildWindow(self.hexLabel)
        self.updateColors()

        # Container
        sliderContainer = Container(50, 50, self.appWindow.width * 0.8, 0, "sliderContainer",
                                    layoutAnchors=LayoutAnchor.top, horizontalDist=False, containerWindows=slidersAndLabels,
                                    spacing=10)
        self.appWindow.addChildWindow(sliderContainer)

        # Container Wrapper for Sliders and label
        elements = [sliderContainer, self.hexLabel]
        wrapperContainer = Container(50, 50, self.appWindow.width * 0.8, self.appWindow.height*0.8, "wrapperContainer",
                                     layoutAnchors=LayoutAnchor.top, horizontalDist=False,containerWindows=elements, spacing=30)
        self.appWindow.addChildWindow(wrapperContainer)

        # TODO (opt): another vert. container with sliders and hexLabel inside to avoid that label crosses sliders while resizing

    def updateColors(self):
        color = rgb_to_hex(self.sliders[0].sliderValue, self.sliders[1].sliderValue, self.sliders[2].sliderValue)
        self.hexLabel.text = color
        self.hexLabel.setBackgroundColor(color)