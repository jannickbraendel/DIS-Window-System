from functools import partial

from UITK import Label, Button, Container
from Window import Window, LayoutAnchor
from GraphicsEventSystem import *


class HelloWorldApp:
    def __init__(self, windowSystem, x, y):
        self.windowSystem = windowSystem
        # add app as top-level window to window system
        identifier = "HelloWorld"
        self.appWindow = Window(x, y, self.windowSystem.width/2.5, self.windowSystem.height/2.5,
                                self.windowSystem.getInstanceNumber(identifier) + " " + identifier,
                                backgroundColor=COLOR_LIGHT_GRAY)
        self.windowSystem.screen.addChildWindow(self.appWindow)
        self.greetLabel = None
        self.languages = ["German", "English", "French"]
        self.drawWidgets()

    def drawWidgets(self):
        # GREETING LABEL
        self.greetLabel = Label(20, 50, self.appWindow.width * 0.3, 50, "GreetingLabel",
                           font=Font(family="Helvetica", size=20), fontColor=COLOR_ORANGE, text="Hello!",
                           layoutAnchors=LayoutAnchor.top)
        self.appWindow.addChildWindow(self.greetLabel)

        # LANGUAGE BUTTONS
        buttons = []
        for i in range(3):
            button = Button(0, 0, 60, 40, "LanguageButton" + str(i), text=self.languages[i],
                            fontColor=COLOR_BLACK, font=Font(family="Helvetica", size=14),
                            layoutAnchors=LayoutAnchor.top | LayoutAnchor.left, hoverBackgroundColor=COLOR_LIGHT_BLUE,
                            pressedBackgroundColor=COLOR_ORANGE, action=partial(self.changeLanguage, self.languages[i]),
                            borderColor=COLOR_BLACK)
            buttons.append(button)
            self.appWindow.addChildWindow(button)

        # language buttons are put into horizontal container
        buttonContainer = Container(40, 100, self.appWindow.width - 80, 40, "ButtonContainer",
                                    layoutAnchors=LayoutAnchor.left | LayoutAnchor.right, horizontalDist=True,
                                    containerWindows=buttons, spacing=30)
        self.appWindow.addChildWindow(buttonContainer)

        # QUIT BUTTON
        quitButton = Button(self.appWindow.width - 80, self.appWindow.height - 80, 60, 40, "QuitButton",
                            layoutAnchors=LayoutAnchor.right | LayoutAnchor.bottom, text="Quit",
                            hoverBackgroundColor=COLOR_RED, pressedBackgroundColor="#8B0000", borderColor=COLOR_BLACK,
                            action=partial(self.windowSystem.windowManager.closeWindow, self.appWindow))
        self.appWindow.addChildWindow(quitButton)
        """
        # VERTICAL CONTAINER
        contWindows = [self.greetLabel, buttonContainer]
        verticalContainer = Container(20, 40, self.appWindow.width, 190, "VerticalContainer",
                                      layoutAnchors=0, horizontalDist=False, containerWindows=contWindows, spacing=100)
        self.appWindow.addChildWindow(verticalContainer)
        """

    def changeLanguage(self, language):
        assert language in self.languages
        if language == "German":
            self.greetLabel.text = "Guten Tag!"
        elif language == "English":
            self.greetLabel.text = "Hello!"
        elif language == "French":
            self.greetLabel.text = "Bonjour!"
