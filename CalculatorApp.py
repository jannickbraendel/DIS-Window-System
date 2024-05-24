import decimal
from functools import partial

from GraphicsEventSystem import *
from Window import *
from UITK import *


def floatToString(num):
    num = round(num, 4)
    return f'{num:g}'


class CalculatorApp:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem

        self.appWindow = Window(1200, 200, 220, 350, "Calculator")
        self.appWindow.setBackgroundColor("#3b3b3b")
        self.windowSystem.screen.addChildWindow(self.appWindow)

        self.buttons = []

        self.inputLabel = None
        # temporarily stores the current result of the calculation
        self.currentResult = 0
        # boolean that is true if input should be overridden
        self.overrideInput = True
        # boolean that is true if arithmetic operation is running -> e.g. "=" button can not be pressed
        self.inOperation = False
        self.drawWidgets()

    def drawWidgets(self):
        # INPUT LABEL
        self.inputLabel = Label(0, 20, self.appWindow.width, 80,
                                "CalcInputLabel", layoutAnchors=LayoutAnchor.top, fontColor="#C07F00",
                                font=Font(family="Helvetica", size=20, weight=BOLD), text="0")
        self.appWindow.addChildWindow(self.inputLabel)

        # BUTTONS
        # array of arrays storing button labels in order of button grid layout
        buttonLabels = [["AC", "C", "%", "/"], ["7", "8", "9", "x"], ["4", "5", "6", "-"], ["1", "2", "3", "+"],
                        ["+/-", "0", ".", "="]]
        buttonRowContainers = []

        # Create Button rows
        for i in range(5):
            buttonRow = []
            # create 4 buttons for each row
            for j in range(4):
                button = Button(0, 0, 40, 40, "button" + str(i) + str(j), LayoutAnchor.top | LayoutAnchor.left,
                                text=buttonLabels[i][j], hoverBackgroundColor=COLOR_BLACK,
                                pressedBackgroundColor=COLOR_ORANGE,
                                fontColor=COLOR_WHITE, font=Font(family="Helvetica", size=14, weight=BOLD),
                                borderColor=COLOR_BLACK)
                button.action = partial(self.handleInput, button.text)
                if i == 0 and j != 3:
                    # First row, first three buttons
                    button.setBackgroundColor("#B4B4B8")
                elif j == 3:
                    # operation buttons
                    button.setBackgroundColor("#FFC100")
                else:
                    # First three buttons in rows 2 to
                    button.setBackgroundColor("#C07F00")
                self.buttons.append(button)
                self.appWindow.addChildWindow(button)
                buttonRow.append(button)

            buttonRowContainer = Container(10, 100 + i * 50, self.appWindow.width - 20, 40, "horContainer" + str(i),
                                           layoutAnchors=LayoutAnchor.top | LayoutAnchor.left, horizontalDist=True,
                                           containerWindows=buttonRow, spacing=10)
            self.appWindow.addChildWindow(buttonRowContainer)
            buttonRowContainers.append(buttonRowContainer)

        # Add vertical container for rowContainers
        buttonContainer = Container(10, 100, self.appWindow.width - 20, self.appWindow.height - 110, "vertContainer",
                                    layoutAnchors=LayoutAnchor.bottom, horizontalDist=False, containerWindows=buttonRowContainers, spacing=10)
        self.appWindow.addChildWindow(buttonContainer)

    def handleInput(self, char):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        operations = ["+", "-", "*", "/"]
        # string value which is displayed
        inputText = self.inputLabel.text
        if char in numbers:
            if inputText == "0" or self.overrideInput:
                inputText = char
                self.overrideInput = False
            else:
                inputText += char
        elif char in operations:
            if char == "+":
                inputText = self.add()
            elif char == "-":
                inputText = self.subtract()
            elif char == "*":
                inputText = self.multiply()
            elif char == "/":
                inputText = self.divide()
            self.overrideInput = True
        elif char == "%":
            inputText = self.percent()
        elif char == "AC":
            # remove marking of operation buttons
            self.changeOperationColor()
            # reset calculator to 0
            inputText = "0"
            self.currentResult = 0
        elif char == "C":
            if not inputText == "0":
                if len(inputText) == 1:
                    inputText = "0"
                else:
                    inputText = inputText[:-1]
        elif char == "=":
            # remove marking of operation buttons
            self.changeOperationColor()
            if not self.overrideInput:
                # display result
                # TODO: Not working correctly
                inputText = floatToString(self.currentResult)

        self.inputLabel.text = inputText

    def add(self):
        self.changeOperationColor(0)
        self.currentResult += float(self.inputLabel.text)
        return floatToString(self.currentResult)

    def subtract(self):
        self.changeOperationColor(1)
        self.currentResult -= float(self.inputLabel.text)
        return floatToString(self.currentResult)

    def multiply(self):
        self.changeOperationColor(2)
        self.currentResult *= float(self.inputLabel.text)
        return floatToString(self.currentResult)

    def divide(self):
        self.changeOperationColor(3)
        self.currentResult /= float(self.inputLabel.text)
        return floatToString(self.currentResult)

    def percent(self):
        # divides current number by 100
        res = float(self.inputLabel.text) / 100
        return floatToString(res)

    def changeOperationColor(self, opNum=None):
        # TODO: Background color is overridden somewhere..
        # operation numbers: 3 - Add, 2 - Subtract, 1 - Multiply, 0 - Divide, None - No operation
        operationButtons = [self.buttons[15], self.buttons[11], self.buttons[7], self.buttons[3]]
        # reset background colors for all op buttons:
        for button in operationButtons:
            button.setBackgroundColor("#FFC100")

        if opNum is None:
            return

        # mark selected operation
        operationButtons[opNum].setBackgroundColor(COLOR_ORANGE)
