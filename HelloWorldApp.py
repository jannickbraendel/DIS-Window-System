from functools import partial

from UITK import Label, Button, Container
from Window import Window, LayoutAnchor
from GraphicsEventSystem import *


class HelloWorldApp:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        # add app as top-level window to window system
        self.appWindow = Window(200, 200, self.windowSystem.width/2.5, self.windowSystem.height/2.5,
                                "Hello World - Graphical")
        self.appWindow.setBackgroundColor(COLOR_LIGHT_GRAY)
        self.windowSystem.screen.addChildWindow(self.appWindow)

        self.languages = ["German", "English", "French"]
        self.greeting = "Hello!"
        self.drawWidgets()

    def drawWidgets(self):
        # GREETING LABEL
        greetLabel = Label(20, 50, self.appWindow.width*0.3, 50, "GreetingLabel",
                           font=Font(family="Helvetica", size=20), fontColor=COLOR_ORANGE, text=self.greeting,
                           layoutAnchors=LayoutAnchor.top)
        self.appWindow.addChildWindow(greetLabel)

        # LANGUAGE BUTTONS
        buttons = []
        for i in range(3):
            button = Button(0, 0, 60, 40, "LanguageButton" + str(i), text=self.languages[i],
                            fontColor=COLOR_BLACK, font=Font(family="Helvetica", size=14),
                            layoutAnchors=LayoutAnchor.top | LayoutAnchor.left, hoverBackgroundColor=COLOR_LIGHT_BLUE,
                            pressedBackgroundColor=COLOR_ORANGE, action=partial(self.changeLanguage, self.languages[i]),
                            borderColor=COLOR_BLACK)
            buttons.append(button)
            button.setBackgroundColor(COLOR_CLEAR)
            self.appWindow.addChildWindow(button)

        buttonContainer = Container(40, greetLabel.y + 50, self.windowSystem.width - 80, 0, "ButtonContainer",
                                    layoutAnchors=LayoutAnchor.left | LayoutAnchor.right, horizontalDist=True,
                                    containerWindows=buttons, spacing=30)
        self.appWindow.addChildWindow(buttonContainer)

        # QUIT BUTTON
        quitButton = Button(self.appWindow.width - 80, self.appWindow.height - 80, 60, 40, "QuitButton",
                            layoutAnchors=LayoutAnchor.right | LayoutAnchor.bottom, text="Quit",
                            hoverBackgroundColor=COLOR_RED, pressedBackgroundColor="#8B0000", borderColor= COLOR_BLACK,
                            action=self.appWindow.removeFromParentWindow)
        quitButton.setBackgroundColor(COLOR_CLEAR)
        self.appWindow.addChildWindow(quitButton)

    def changeLanguage(self, language):
        # TODO: Label not redrawn correctly
        assert language in self.languages
        if language == "German":
            self.greeting = "Guten Tag!"
        elif language == "English":
            self.greeting = "Hello!"
        elif language == "French":
            self.greeting = "Bonjour!"
