# Nama : Hizkya Firstadipa Hartoko
# NIM : 20/455447/PA/19662
# Kelas : KOMB Metode Numerik


def getInputEquation(equation):
    mEq = equation
    ops = ['^','-','+','*','/']
    seq = []
    cp = 0
    i = 0
    while i < len(mEq):
        if mEq[i] in ops:
            if i == 0:
                seq.append(mEq[i])
            else:
                seq.append(mEq[cp:i])
                seq.append(mEq[i])

            cp = i+1

        i += 1
    
    seq.append(mEq[cp:len(mEq)])
    seq.append('end')

    eq_data = []
    operation = {
        'coef': 0,
        'exp': 0,
        'const': 0,
        'base': ''
    }

    var_names = 'abcdefghijklmnopqrstuvwxyz'
    i = 0
    while i < len(seq):

        if seq[i] in ['-','+','end'] and i > 0:
            if operation['base'] == '':
                operation['const'] = operation['coef']
                operation['coef'] = 0

            eq_data.append(operation)
            operation = {
                    'coef': 0,
                    'exp': 0,
                    'const': 0,
                    'base': ''
            }

        if seq[i] in var_names:
            operation['base'] = seq[i]
            operation['exp'] = 1
            operation['coef'] = 1
        

        elif seq[i] == '-':

            if seq[i+1] in var_names:
                operation['base'] = seq[i+1]
                operation['exp'] = 1
                operation['coef'] = -1
            else:
                operation['coef'] = -int(seq[i+1])
            i += 1

        elif seq[i] == '+':

            if seq[i+1] in var_names:
                operation['base'] = seq[i+1]
                operation['exp'] = 1
                operation['coef'] = 1
            else:
                operation['coef'] = int(seq[i+1])
            i += 1

        elif seq[i] == '*':

            if seq[i+1] in var_names:
                operation['base'] = seq[i+1]
                operation['exp'] = 1
            else:
                operation['coef'] *= int(seq[i+1])
            i += 1

        elif seq[i] == '/':

            if seq[i+1] in var_names:
                operation['base'] = seq[i+1]
                operation['exp'] = -1
            else:
                operation['coef'] /= int(seq[i+1])
            i += 1

        elif seq[i] == '^':
            if seq[i-1] in var_names:
                operation['exp'] = int(seq[i+1])
            else:
                if operation['coef'] < 0:
                    operation['coef'] = -1*(operation['coef']**int(seq[i+1]))
                else:
                    operation['coef'] **=int(seq[i+1])
            i += 1

        elif seq[i] != 'end':
            operation['coef'] = int(seq[i])

        i += 1

        

    return eq_data

def getDerivativeEquation(eq_data):

    derivative_eq_data = []
    i = 0
    while i < len(eq_data):

        coef = eq_data[i]['coef']
        exp = eq_data[i]['exp']
        const = eq_data[i]['const']
        base = eq_data[i]['base']

        remove = False

        if exp == 1:
            const = coef
            exp = 0 
            coef = 0
            base = ''
        elif const != 0:
            remove = True
        else:
            coef = coef*exp
            exp -= 1
            

        if remove == False:
            operation = {
                'coef': coef,
                'exp': exp,
                'const': const,
                'base': base
            }
            derivative_eq_data.append(operation)

        
        i += 1

    return derivative_eq_data

def countEquation(eq_data, x):
    result = 0
    for i in range(len(eq_data)):
        coef = eq_data[i]['coef']
        exp = eq_data[i]['exp']
        const = eq_data[i]['const']
        base = eq_data[i]['base']

        if const != 0:
            result += const
        else:
            result += coef*pow(x,exp)

    return result

def countDerivative(d_eq_data, x):
    result = 0
    for i in range(len(d_eq_data)):
        coef = d_eq_data[i]['coef']
        exp = d_eq_data[i]['exp']
        const = d_eq_data[i]['const']
        base = d_eq_data[i]['base']

        if const != 0:
            result += const
        else:
            result += coef*pow(x,exp)

    return result

def getNextX(equation,derivative,x):
    y = equation
    m = derivative
    c = y - (m*x)

    x_new = -c / m
    return x_new

def rootSearch4thMethod(equation, x, iteration):
    
    eq_data = getInputEquation(equation)
    d_eq_data = getDerivativeEquation(eq_data)
    currentX = x

    for i in range(iteration):
        equation = countEquation(eq_data,currentX)
        derivative = countDerivative(d_eq_data, currentX)
        while derivative == 0:
            if currentX < 0:
                currentX -= 1
            else: 
                currentX += 1
            derivative = countDerivative(d_eq_data, currentX)
        currentX = getNextX(equation, derivative, currentX)
        
        if equation == 0:
            break
        
    if currentX == 0:
        currentX = abs(currentX)

    return currentX

equation_1 = 'x^3-2*x^2-5*x+6'
equation_2 = 'x^2-2*x-24'
equation_3 = 'x^3-10^2-25*x+250'
init_x = -8
iteration = 10

# NIU = 455447
# 455447 mod 3 = 2, 3rd Equation
# 455447 mod 4 = 3, 4th Method
# 455447 mod 6 = 5, initial x = -8 

root = rootSearch4thMethod(equation_3, init_x, iteration)
print("Root Searching result: " + str(root))
testRoot = countEquation(getInputEquation(equation_3), root)
print("Test Searched Root in the Equation Result: " + str(testRoot))








