class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__


class Stack:
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return 'Top:{}\nStack:\n{}'.format(self.top, out)

    __repr__ = __str__

    def isEmpty(self):
        return self.top is None

    def __len__(self): 
        length = 0
        current = self.top
        while current:
            length += 1
            current = current.next
        return length

    def push(self, value):
        newnode = Node(value)
        newnode.next = self.top
        self.top = newnode

    def pop(self):
        if self.isEmpty():
            return None
        temp = self.top
        self.top = self.top.next
        temp.next = None
        return temp.value

    def peek(self):
        if self.isEmpty():
            return None
        return self.top.value


#Handles conversion from infix to postfix notation for expression evaluations
class Calculator:
    def __init__(self):
        self.__expr = None

    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr = new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        try:
            float(txt)
            return True
        except:
            return False

    #Converts infix expressions to postfix notation
    def _getPostfix(self, txt):
        if not self.__expr:
            return None
        postfixStack = Stack()
        postfix = []
        order = {'+' : 1, '-' : 1, '*' : 2, '/' : 2, '^' : 3}
        tokens = txt.split()
        for token in tokens:
            if self._isNumber(token):
                postfix.append(float(token))
            elif token == '(':
                postfixStack.push(token)
            elif token == ')':
                while not postfixStack.isEmpty() and postfixStack.peek() != '(':
                    postfix.append(postfixStack.pop())
                if postfixStack.isEmpty() or postfixStack.peek() != '(':
                    return None
                postfixStack.pop()
            elif token in order:
                while not postfixStack.isEmpty() and postfixStack.peek() != '(' and order[token] <= order[postfixStack.peek()]:
                    postfix.append(postfixStack.pop())
                postfixStack.push(token)
            else:
                return None
        while not postfixStack.isEmpty():
            if postfixStack.peek() == '(':
                return None
            postfix.append(postfixStack.pop())
        return postfix

    @property
    def calculate(self):
        if not isinstance(self.__expr, str) or len(self.__expr) <= 0:
            print("Argument error in calculate")
            return None
        calcStack = Stack()
        postfix = self._getPostfix(self.getExpr)
        if postfix is None:
            return None
        for token in postfix:
            if self._isNumber(token):
                calcStack.push(float(token))
            else:
                token1 = calcStack.pop()
                token2 = calcStack.pop()
                if token == '+':
                    result = token2 + token1
                elif token == '-':
                    result = token2 - token1
                elif token == '*':
                    result = token2 * token1
                elif token == '/':
                    if token1 == 0:
                        return None  # Handle division by zero
                    result = token2 / token1
                elif token == '^':
                    result = token2 ** token1
                calcStack.push(float(result))
        return calcStack.pop()


#Manages multiple expressions with variables
class AdvancedCalculator:
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        return word.isalnum() and word[0].isalpha()

    #Replaces variables in expressions with their values from the state dictionary
    def _replaceVariables(self, expr):
        tokens = expr.split(' ')
        newtokens = []
        for token in tokens:
            if self._isVariable(token):
                if token not in self.states:
                    return None
                newtokens.append(str(self.states[token]))
            else:
                newtokens.append(token)
        newexpr = ' '.join(newtokens)
        return newexpr

    #Evaluates expressions, and updating + using variables as needed
    def calculateExpressions(self):
        exprs = self.expressions.strip().split(';')
        for expr in exprs:
            tokens = expr.strip().split()
            variable = tokens[0]
            operator = tokens[1]
            expr = self._replaceVariables(' '.join(tokens[2:]))
            if expr is None:
                return None
            calcObj = Calculator()
            calcObj.setExpr(expr)
            value = calcObj.calculate
            if operator == '=':
                self.states[variable] = value
            else:
                return None
        expr = self._replaceVariables(exprs[-1].strip())
        calcObj.setExpr(expr)
        value = calcObj.calculate
        return value