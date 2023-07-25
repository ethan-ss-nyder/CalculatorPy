from enum import Enum

class Math:

    global operationArray
    global Operations
    global MiscCalcOptions
    global Grouping
    # These three objects are flags and strings that are collected during input and analyzed upon hitting "=".
    # opeartionArray will be composed of numbers and Enum objects from the Enums below.
    operationArray = []
    Operations = Enum('Operations', ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE']) # Flags for post-input processing
    MiscCalcOptions = Enum('CalcOptions', ['BACKSPACE', 'CLEAR', 'DECIMAL', 'EQUALS']) # More flags for non-operational inputs
    Grouping = Enum('Grouping', ['OPAREN', 'CLOPAREN', 'OBRACK', 'CLOBRACK'])

    def __init__(self, operationArray):
        self.operationArray = operationArray

    def getOperationArray():
        return operationArray

    def getOperationEnum():
        return Operations
    
    def getMiscCalcOptionsEnum():
        return MiscCalcOptions
    
    def getGroupingEnum():
        return Grouping
    
    def orderOfOperations(operationArray: list):
        """
        Breaks an input list down into the math that it represents. For elementary functions.

        orderOfOperations() assumes it's recieving perfect input, please validate operationArray before passing it in.
        """

        answerArray = []

        operationArray = convertOperators(operationArray) # orderofops > convertoperators > validateoperationarray

        i = 0

        while i < len(operationArray):
            if ((operationArray[i] == Grouping.OPAREN) or (operationArray[i] == Grouping.OBRACK)):
                answerArray.append(paranthesisHandler(operationArray, i))
            elif (type(operationArray[i]) == Operations):
                match operationArray[i]:
                    case Operations.MULTIPLY:
                        num1 = operationArray[i-1]
                        num2 = operationArray[i+1]
                        popper(operationArray, i-1, 3) #num1, operator, num3 are being popped
                        operationArray.insert(i-1, num1*num2)
                    case Operations.ADD:
                        num1 = operationArray[i-1]
                        num2 = operationArray[i+1]
                        popper(operationArray, i-1, 3) #num1, operator, num3 are being popped
                        operationArray.insert(i-1, num1+num2)
                i = 1 # If an operator was found, start iterating through everything again since the operationArray length has changed.
            else:
                i += 1

        return operationArray
    
        
################### LOCAL FUNCTIONS #####################

Operations = Math.getOperationEnum()

def paranthesisHandler(arrayWithParenthesis: list, indexOfOpener: int):
    """
    Handles paranthesis and everything in paranthesis, and returns the result of the math inside the paranthesis.

    Parameter arrayWithParenthesis: the array, including the paranthesis characters.
    Parameter index: Index that the first grouper is found at in arrayWithParenthesis.

    Returns the result of the math contained in the paranthesis.
    """
    # This match statement defines the index of the closing grouper based on the type of opening grouper.
    match arrayWithParenthesis[indexOfOpener]:
        case Grouping.OPAREN:
            indexOfCloser = arrayWithParenthesis.index(Grouping.CLOPAREN, indexOfOpener)
        case Grouping.OBRACK:
            indexOfCloser = arrayWithParenthesis.index(Grouping.CLOBRACK, indexOfOpener)

    tempArray = []
    for x in arrayWithParenthesis in range(indexOfOpener, indexOfCloser):
        tempArray.append(x)

    print(tempArray)


def convertOperators(operationArray: list):
    """
    Changes the subtraction and division operators to be addition and multiplication, for convenience.

    Parameter operationArray: the list that has subtraction and divison operator Enums in it.

    Returns the converted list.
    """

    operationArray = validateOperationArray(operationArray)

    i = 0

    while i < len(operationArray):
        if ((operationArray[i] == Operations.SUBTRACT) or (operationArray[i] == Operations.DIVIDE)):
            match operationArray[i]:
                case Operations.SUBTRACT:
                    operationArray[i+1] *= -1 # Make the number being subtracted negative
                    if i != 0: # If the first element in operationArray is -, don't replace with + (-x), just (-x)
                        operationArray.pop(i)
                        operationArray.insert(i, Operations.ADD)
                case Operations.DIVIDE:
                    operationArray[i+1] = (operationArray[i+1]**(-1))
                    operationArray.pop(i)
                    operationArray.insert(i, Operations.MULTIPLY)
        else:
            i += 1

    return operationArray


def validateOperationArray(operationArray: list):
    """
    Cleans up the operation array and makes it more useable. This function puts decimals together, removes double operators,
    removes leading operators (other than the minus sign).

    Parameter operationArray: the list to be cleaned up. Should be raw right from user input.

    Returns a validated, cleaned list.
    """

    # Useful for later when determining if there's an integer on either side of decimal
    numberOnRight = False
    numberOnLeft = False

    i = 0
    lastElement = False

    while i < len(operationArray):
        # Whitespace
        if (operationArray[i] == "" or operationArray[i] == " "):
            operationArray.pop()
        # Consecutive operators
        elif ((lastElement != True) and (type(operationArray[i]) == Operations) and (type(operationArray[i+1]) == Operations)):
                operationArray.pop(i)
        # Consecutive decimals
        elif ((operationArray[i] == MiscCalcOptions.DECIMAL) and (operationArray[i+1] == MiscCalcOptions.DECIMAL)):
            operationArray.pop(i)
        # Make sure that each open grouper has a closing grouper
        elif (operationArray[i] == Grouping.OPAREN or operationArray[i] == Grouping.OBRACK):
            immuneClosers = [] # When an opener finds a closer, the closer index becomes immune to popping
            match operationArray[i]:
                case Grouping.OPAREN:
                    try:
                        immuneClosers.append(operationArray.index(Grouping.CLOPAREN, i))
                    except:
                        operationArray.pop(i)
                case Grouping.OBRACK:
                    try:
                        immuneClosers.append(operationArray.index(Grouping.CLOBRACK, i))
                    except:
                        operationArray.pop(i)
                case __: # Default case will trigger for all closing groupers
                    if i not in immuneClosers: # But only not-immune closing groupers will perish.
                        operationArray.pop(i)
        # Decimal work
        elif operationArray[i] == MiscCalcOptions.DECIMAL:
            # This try/except is for flagging numbers on either side of the decimal
            try:
                operationArray[i-1] = int(operationArray[i-1])
                numberOnRight = True
                operationArray[i+1] = int(operationArray[i+1])
                numberOnLeft = True
            except:
                pass
            # These two statements handle the cases set by the booleans above that flag if there's numbers on either side of the decimal
            if numberOnRight and not(numberOnLeft):
                tempString = "0." + operationArray[i+1]
                popper(operationArray, i, 2)
                operationArray.insert(i, float(tempString))
            elif numberOnRight and numberOnLeft:
                tempString = str(operationArray[i-1]) + "." + str(operationArray[i+1])
                popper(operationArray, i-1, 3) # See popper. Pops 3 elements.
                operationArray.insert(i, float(tempString))
            elif (numberOnLeft and not numberOnRight):
                operationArray.pop(i) # If, for some reason, somebody ends a number with a decimal point
            elif ((not(numberOnLeft)) & (not(numberOnRight))):
                operationArray.pop(i) # For lone decimals surrounded by operators
        # Only good, clean, valid input deserves to move on. This is the result of the pop() function and the cascade effect
        # that it causes, because i will stay the same, but i+1 changes. By not adding 1 to i every run, then, I'm allowing the
        # function to sit and spin its wheels until the whole mess is taken care of.
        else:
            i += 1
            if i == (len(operationArray)-2): # This sets a flag for the next time around
                lastElement = True
            else:
                lastElement = False

    return operationArray

def popper(array: list, index: int, x: int):
    """
    For when an array needs a lot of popping. Only works for consecutive elements.

    Parameter array: the array.
    Parameter index: the index of the LOWEST element wanting to be popped. The rest will cascade and be popped on this index.
    Parameter x: the amount of pops.

    Returns the initial array, but popped.
    """
    i = 0
    while i < x:
        array.pop(index)
        i += 1