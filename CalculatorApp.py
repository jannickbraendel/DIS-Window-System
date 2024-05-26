import decimal
from enum import Enum
from functools import partial
from GraphicsEventSystem import *
from Window import *
from UITK import *


def floatToString(num):
    num = round(num, 4)
    return f'{num:g}'


# enum for arithmetic operations
# Operation = Enum('Operation', ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE'])
class Operation(Enum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4


class CalculatorApp:
    def __init__(self, windowSystem, x, y):
        self.windowSystem = windowSystem
        identifier = "Calculator"
        self.appWindow = Window(x, y, 220, 350, self.windowSystem.getInstanceNumber(identifier) + " " + identifier,
                                backgroundColor="#3b3b3b")
        self.windowSystem.screen.addChildWindow(self.appWindow)

        self.buttons = []

        self.inputLabel = None
        # temporarily stores the current result of the calculation
        self.currentResult = 0
        # boolean that is true if input should be overridden
        self.overrideInput = False
        # store previous operation, which is executed after next function call
        self.prevOperation = None
        # store previous input to check edge cases
        self.prevInput = None
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
                button = Button(0, 0, 40, 40, "button" + str(i) + str(j),
                                text=buttonLabels[i][j], hoverBackgroundColor=COLOR_BLACK,
                                pressedBackgroundColor=COLOR_ORANGE, layoutAnchors=LayoutAnchor.top | LayoutAnchor.left,
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
        # todo: Jannick fix resizing
        buttonContainer = Container(10, 100, self.appWindow.width - 20, self.appWindow.height - 110, "vertContainer",
                                    layoutAnchors=LayoutAnchor.bottom, horizontalDist=False,
                                    containerWindows=buttonRowContainers, spacing=10)
        self.appWindow.addChildWindow(buttonContainer)

    def handleInput(self, char):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        operations = ["+", "-", "x", "/"]
        # temporarily store string value which is displayed
        inputText = self.inputLabel.text

        # check if ERROR is displayed and don't do anything except if AC is pressed
        if inputText == "ERROR" and char != "AC":
            return

        if char in numbers:
            if (inputText == "0" and char != ".") or self.overrideInput:
                # override input text after operation button or reset
                inputText = char
                self.overrideInput = False
            else:
                inputText += char

        elif char in operations:
            if self.prevInput not in ["+", "-", "x", "/"]:
                # perform previous Operation, BUT if the user clicked on another operation button before,
                # only update but not perform operation
                inputText = self.performPreviousOperation()
            # store current operation to last operation variable and color it
            if char == "+":
                self.prevOperation = Operation.ADD
                self.changeOperationColor(Operation.ADD.value)
            elif char == "-":
                self.prevOperation = Operation.SUBTRACT
                self.changeOperationColor(Operation.SUBTRACT.value)
            elif char == "x":
                self.prevOperation = Operation.MULTIPLY
                self.changeOperationColor(Operation.MULTIPLY.value)
            elif char == "/":
                self.prevOperation = Operation.DIVIDE
                self.changeOperationColor(Operation.DIVIDE.value)

            # lets user override label with next input
            self.overrideInput = True
        elif char == "%":
            inputText = self.percent()
        elif char == "+/-":
            inputText = self.negate()
        elif char == "=":
            # remove marking of operation buttons
            self.changeOperationColor()
            # display result
            inputText = self.performPreviousOperation()
            # reset prevOperation
            self.prevOperation = None
        elif char == "C":
            if not inputText == "0":
                if len(inputText) == 1:
                    inputText = "0"
                else:
                    inputText = inputText[:-1]
        elif char == "AC":
            # remove marking of operation buttons
            self.changeOperationColor()
            # reset calculator
            inputText = "0"
            self.currentResult = 0.0
            self.prevOperation = None
            self.prevInput = None

        # set label text to updated inputText
        self.inputLabel.text = inputText
        # update previous input
        self.prevInput = char

    def performPreviousOperation(self):
        # perform last operation on current result or set current result (if last operation is None)
        fInputText = float(self.inputLabel.text)
        if self.prevOperation is None:
            self.currentResult = fInputText
        elif self.prevOperation.name == 'ADD':
            self.currentResult += fInputText
        elif self.prevOperation.name == 'SUBTRACT':
            self.currentResult -= fInputText
        elif self.prevOperation.name == 'MULTIPLY':
            self.currentResult *= fInputText
        elif self.prevOperation.name == 'DIVIDE':
            if fInputText == 0.0:
                return "ERROR"
            self.currentResult /= fInputText

        # set input label to temporary result
        return floatToString(self.currentResult)

    def percent(self):
        # divides current number by 100
        res = float(self.inputLabel.text) / 100
        return floatToString(res)

    def negate(self):
        # switch positive number to negative number and vice versa
        fInputText = float(self.inputLabel.text)
        if fInputText == 0:
            res = 0
        else:
            res = -fInputText
        return floatToString(res)

    def changeOperationColor(self, opNum=None):
        # operation numbers: 1 - Add, 2 - Subtract, 3 - Multiply, 4 - Divide, None - No operation
        operationButtons = [self.buttons[15], self.buttons[11], self.buttons[7], self.buttons[3]]
        # reset background colors for all op buttons:
        for button in operationButtons:
            button.setBackgroundColor("#FFC100")

        # all buttons reset to old bg color
        if opNum is None:
            return

        # mark selected operation
        operationButtons[opNum-1].setBackgroundColor(COLOR_ORANGE)
