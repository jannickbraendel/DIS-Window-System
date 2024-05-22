from functools import partial

from GraphicsEventSystem import *
from Window import *
from UITK import *


class CalculatorApp:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem

        self.appWindow = Window(1200, 200, 220, 350, "Calculator")
        self.appWindow.setBackgroundColor("#3b3b3b")
        self.windowSystem.screen.addChildWindow(self.appWindow)

        self.inputLabel = None
        self.drawWidgets()

    def drawWidgets(self):
        # INPUT LABEL
        self.inputLabel = Label(0, 20, self.appWindow.width, 80,
                                "CalcInputLabel", layoutAnchors=LayoutAnchor.top, fontColor="#C07F00",
                                font=Font(family="Helvetica", size=20, weight=BOLD), text="0")
        self.appWindow.addChildWindow(self.inputLabel)

        # BUTTONS
        # array of arrays storing button labels in order of button grid layout
        buttonLabels = [["AC", "C", "?", "/"], ["7", "8", "9", "x"], ["4", "5", "6", "-"],["1", "2", "3", "+"],
                        ["+/-", "0", ".", "="]]
        buttonRowContainers = []

        # Create Button rows
        for i in range(5):
            buttonRow = []
            # create 4 buttons for each row
            for j in range(4):
                button = Button(0, 0, 40, 40, "button" + str(i) + str(j), LayoutAnchor.top | LayoutAnchor.left,
                                text=buttonLabels[i][j], hoverBackgroundColor=COLOR_BLACK, pressedBackgroundColor=COLOR_ORANGE,
                                fontColor=COLOR_WHITE, font=Font(family="Helvetica", size=14, weight=BOLD), borderColor=COLOR_BLACK)
                button.action = partial(self.handleInput, button.text)
                if i == 0:
                    # first row
                    if not j == 3:
                        # first three buttons in row
                        button.setBackgroundColor("#B4B4B8")
                    else:
                        # last button in row
                        button.setBackgroundColor("#FFC100")
                else:
                    # other rows
                    if not j == 3:
                        # first three buttons in row
                        button.setBackgroundColor("#C07F00")
                    else:
                        # last button in row
                        button.setBackgroundColor("#FFC100")
                self.appWindow.addChildWindow(button)
                buttonRow.append(button)

            buttonRowContainer = Container(10, 100 + i*50, self.appWindow.width - 20, 40, "horContainer" + str(i),
                                        layoutAnchors=LayoutAnchor.left | LayoutAnchor.top, horizontalDist=True,
                                        containerWindows=buttonRow, spacing=10)
            self.appWindow.addChildWindow(buttonRowContainer)
            buttonRowContainers.append(buttonRowContainer)

        # TODO: Add vertical container for rowContainers

    def handleInput(self, char):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        inputText = self.inputLabel.text
        if char in numbers:
            if inputText == "0":
                inputText = char
            else:
                inputText += char
        elif char == "AC":
            inputText = "0"
        elif char == "C":
            if not inputText == "0":
                if len(inputText) == 1:
                    inputText = "0"
                else:
                    inputText = inputText[:-1]
        elif char == "=":
            self.solve()

        self.inputLabel.text = inputText

    def solve(self):
        pass