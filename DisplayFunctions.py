import tkinter
from MathLib import Math

class Display:

    global exitMainLoop
    exitMainLoop = False
    window = tkinter.Tk() # For some reason, this has to be done here

    global CANVAS_HEIGHT
    global CANVAS_WIDTH
    # Every other widget calls upon the canvas dimensions for their size. This scales everything within the window.
    CANVAS_HEIGHT = 250 # pixels
    CANVAS_WIDTH = 400 # pixels

    global NUMBER_SIZE_MULTIPLIER_WIDTH
    global NUMBER_SIZE_MULTIPLIER_HEIGHT
    # For the number buttons, these scale the window size so that the buttons aren't a fixed size.
    NUMBER_SIZE_MULTIPLIER_WIDTH = 0.04
    NUMBER_SIZE_MULTIPLIER_HEIGHT = 0.01

    # Not really a multiplier. Making this number bigger makes there be more cells total.
    global cellMultiplier
    cellMultiplier = 12

    global userInput
    userInput = []

    global lastText
    lastText = ""

    def __init__(self, window, exitMainLoop):
        """
        Initializes the class, makes window accessible to files importing DisplayFunctions if,
        for some reason, somebody ever wanted to make changes to the window in the importing file
        and not here in the library.
        """
        self.window = window
        self.exitMainLoop = exitMainLoop

    def getUserInput():
        """
        Returns an array containing numbers and Enums collected from user input.
        """
        return userInput
    
    def setUserInput(list):
        """
        Used to set the userInput variable.

        Parameter list: a list used to set the userInput variable with.
        """
        Display.userInput = list
    
    def getDisplayText():
        """
        Returns the text inside the entry widget.
        """
        return bannerTextDisplay.get()
    
    def getExitMainLoop():
        """
        Returns the boolean that decides when the main display loop should be exited.
        """
        return exitMainLoop

    def buildGUI():
        """
        Builds a preset GUI for Calculator.py.
        This includes buttons and the entry widget at the top of the calculator window.
        """
        canvas = tkinter.Canvas(Display.window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT).grid()
        Display.window.title("Calculator")

        global bannerTextDisplay
        # Interactive text display banner at top of window
        bannerTextDisplay = tkinter.Entry(Display.window, width=int(CANVAS_WIDTH*.2), justify="center", font="Bookman")
        bannerTextDisplay.grid(row=0, column=0, rowspan=1, columnspan=20)

        # Other functions that are separated for organization purposes.
        buildNumberButtons()
        buildOperationButtons()
        buildMiscButtons()

        # This defines exit behavior upon the user closing the calculator window.
        # More specifically, exitTask() defines what is done.
        Display.window.protocol("WM_DELETE_WINDOW", exitTask)

######################### LOCAL FUNCTIONS ############################        

Operations = Math.getOperationEnum()
MiscCalcOptions = Math.getMiscCalcOptionsEnum()
Grouping = Math.getGroupingEnum()

def buttonPressAction(appendable, updateDisplay = True):
    """
    To be used for button presses upon that event activating. This is used for most buttons to append the appendable
    variable to the global userInput list and optionally, update the display upon button press with the new button.

    Parameter appendable: the object to be appended. Usually an Enum or an integer.
    Parameter updateDisplay: True if the Entry widget should be updated after this button press with the new added character.
    """
    if updateDisplay == True:
        if appendable == MiscCalcOptions.BACKSPACE: # If the user backspaced...
            bannerTextDisplay.delete(len(userInput)-1, len(userInput)+1)
            userInput.pop()
        elif appendable == MiscCalcOptions.CLEAR: # If the user hit clear...
            bannerTextDisplay.delete(0, len(Display.getDisplayText()))
            userInput.clear()
        elif appendable == MiscCalcOptions.EQUALS: # If the user hit equals...
            answer = Math.orderOfOperations(userInput)
            Display.setUserInput(answer)
            bannerTextDisplay.delete(0, len(Display.getDisplayText()))
            bannerTextDisplay.insert(0, inputToString())
        else:
            userInput.append(appendable)
            bannerTextDisplay.delete(0, len(userInput))
            bannerTextDisplay.insert(0, inputToString())

def buildNumberButtons():
    """
    Builds number buttons 0-9 and assigns them their respective commands when pressed.
    """
    # This mess creates buttons 1-9 and the associated commands. This absolute mess works, so never look at this ever again.
    i = 1
    k = 1
    while i <= 3:
        j = 1
        while j <= 3:
            tkinter.Button(Display.window, text=str(k), command=lambda k=k: buttonPressAction(k),
                           height=int(NUMBER_SIZE_MULTIPLIER_HEIGHT*CANVAS_HEIGHT),
                           width=int(NUMBER_SIZE_MULTIPLIER_WIDTH*CANVAS_WIDTH)).grid(column=j+cellMultiplier, row=i+cellMultiplier)
            j += 1
            k += 1
        i += 1
    # Creates 0 because it has a special placement that wasn't possible to do through iteration.
    tkinter.Button(Display.window, text="0",
                   command=lambda: buttonPressAction(0, True),
                   height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT),
                   width=int(CANVAS_WIDTH*NUMBER_SIZE_MULTIPLIER_WIDTH)).grid(row=4+cellMultiplier, column=2+cellMultiplier)

def buildOperationButtons():
    """
    Builds the addition, subtract, multiplication, and division buttons.
    """
    operatorText = ["+", "-", "*", "/"]
    operators = [Operations.ADD, Operations.SUBTRACT, Operations.MULTIPLY, Operations.DIVIDE]
    i = 1
    while i <= 4:
        if (i % 2 == 0):
            columnNumber = 5
        else:
            columnNumber = 4
        if (i == 1 or i == 2):
            rowNumber = 1
        else:
            rowNumber = 2
        tkinter.Button(Display.window, text=operatorText[i-1], 
                       command=lambda i=i: buttonPressAction(operators[i-1]),
                       height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT),
                       width=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_WIDTH*.3)).grid(row=rowNumber+cellMultiplier, column=columnNumber+cellMultiplier)
        i += 1

def buildMiscButtons():
    """
    Builds miscellaneous buttons, like backspace, equals, the decimal key. More to come.
    """
    # I'm so sorry for this mess. Just copy and paste a similar button's line and modify it a bit to get what and where you want.
    tkinter.Button(Display.window, text="=", command=lambda: buttonPressAction(MiscCalcOptions.EQUALS), height=int(CANVAS_WIDTH*NUMBER_SIZE_MULTIPLIER_HEIGHT*1.3), width=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_WIDTH)).grid(row=3+cellMultiplier, column=4+cellMultiplier, rowspan=2, columnspan=2)
    tkinter.Button(Display.window, text="<--", command=lambda: buttonPressAction(MiscCalcOptions.BACKSPACE), height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT), width=int(CANVAS_WIDTH*NUMBER_SIZE_MULTIPLIER_WIDTH)).grid(row=4+cellMultiplier, column=1+cellMultiplier)
    tkinter.Button(Display.window, text=".", command=lambda: buttonPressAction(MiscCalcOptions.DECIMAL), height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT), width=int(CANVAS_WIDTH*NUMBER_SIZE_MULTIPLIER_WIDTH)).grid(row=4+cellMultiplier, column=3+cellMultiplier)
    tkinter.Button(Display.window, text="(", command=lambda: buttonPressAction(Grouping.OPAREN), height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT), width=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_WIDTH*0.5)).grid(row=1+cellMultiplier, column=-1+cellMultiplier)
    tkinter.Button(Display.window, text=")", command=lambda: buttonPressAction(Grouping.CLOPAREN), height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT), width=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_WIDTH*0.5)).grid(row=1+cellMultiplier, column=0+cellMultiplier)
    tkinter.Button(Display.window, text="Clear", command=lambda: buttonPressAction(MiscCalcOptions.CLEAR), height=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_HEIGHT), width=int(CANVAS_HEIGHT*NUMBER_SIZE_MULTIPLIER_WIDTH*0.5)).grid(row=0, column=4+cellMultiplier, columnspan=2)

def inputToString(input = userInput):
    """
    Converts lists of math symbols and such into readable strings.

    Parameter input: list to be decoded. If not specified, will use the global userInput list.

    Returns a nice, readable string.
    """
    string = ""
    # This will need to be updated with every Enum term that's ever added. Good luck.
    for x in input:
        match x:
            case Operations.ADD:
                string += "+"
            case Operations.MULTIPLY:
                string += "*"
            case Operations.SUBTRACT:
                string += "-"
            case Operations.DIVIDE:
                string += "/"
            case MiscCalcOptions.DECIMAL:
                string += "."
            case Grouping.OPAREN:
                string += "("
            case Grouping.CLOPAREN:
                string += ")"
            case Grouping.OBRACK:
                string += "["
            case Grouping.CLOBRACK:
                string += "]"
            case __:
                string += str(x)
    return string

def exitTask():
    """
    Exit behavior upon closing the calculator window.
    Closes the window and sets exitMainLoop to True.

    NOTE: information can NOT be retrieved from the window after exitTask() is called.
    """
    Display.window.destroy()
    global exitMainLoop
    exitMainLoop = True