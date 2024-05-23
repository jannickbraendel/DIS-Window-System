import decimal
from functools import partial

from GraphicsEventSystem import *
from Window import *
from UITK import *


def floatToString(num):
    return str(f"{num:.4f}")


def format_number(num):
    try:
        dec = decimal.Decimal(num)
    except:
        return 'bad'
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0' * zeros) + digits
    else:
        val = digits[:delta] + ('0' * tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val


class CalculatorApp:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem

        self.appWindow = Window(1200, 200, 220, 350, "Calculator")
        self.appWindow.setBackgroundColor("#3b3b3b")
        self.windowSystem.screen.addChildWindow(self.appWindow)

        self.inputLabel = None
        # temporarily stores the current result of the calculation
        self.currentResult = 0
        # boolean that is true if input should be overridden
        self.overrideInput = True
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

            buttonRowContainer = Container(10, 100 + i * 50, self.appWindow.width - 20, 40, "horContainer" + str(i),
                                           layoutAnchors=LayoutAnchor.left | LayoutAnchor.top, horizontalDist=True,
                                           containerWindows=buttonRow, spacing=10)
            self.appWindow.addChildWindow(buttonRowContainer)
            buttonRowContainers.append(buttonRowContainer)

        # TODO: Add vertical container for rowContainers

    def handleInput(self, char):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        inputText = self.inputLabel.text
        if char in numbers:
            if inputText == "0" or self.overrideInput:
                inputText = char
                self.overrideInput = False
            else:
                inputText += char
        elif char == "+":
            inputText = self.add()
            self.overrideInput = True
        elif char == "-":
            inputText = self.subtract()
            self.overrideInput = True
        elif char == "*":
            inputText = self.multiply()
            self.overrideInput = True
        elif char == "/":
            inputText = self.divide()
            self.overrideInput = True
        elif char == "%":
            inputText = self.percent()
        elif char == "AC":
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
            # display result
            inputText = floatToString(self.currentResult)
        inputText = format_number(round(float(inputText), 4))
        self.inputLabel.text = inputText

    def add(self):
        if "." in self.inputLabel.text:
            self.currentResult += float(self.inputLabel.text)
        else:
            self.currentResult += int(self.inputLabel.text)

        return floatToString(self.currentResult)

    def subtract(self):
        return 0

    def multiply(self):
        return 0

    def divide(self):
        return 0

    def percent(self):
        # divides current number by 100 and presents float with two
        res = float(self.inputLabel.text) / 100
        return floatToString(res)
