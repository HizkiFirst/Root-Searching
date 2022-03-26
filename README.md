# Root-Searching
Numeric Method Assignment, program to approximate roots of an equations

## Methods inside the program
<details><summary>Preprocessing Equation</summary>
<p>

#### Parsing the equation

This function read equation input and turn them into equation data
```python
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
```

</p>
</details>

<details><summary>Get Derivative Equation (f'(x))</summary>
<p>
  
#### Find f'(x)
This function get derivative of the equation, the derivative will be used later to count the gradient (m) in y = mx + c

  The input arguments is the equation data which obtained in the preprocessing equation
  
```python
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
```
</p>
</details>


<details><summary> Count Equation </summary>
<p>

### Calculate equation

This function calculate the equation with equation data and x as the arguments

```python
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
```
</p>
</details>

<details><summary> Count Derivative  </summary>
<p>

### Calculate Derivative

This function calculate the derivative equation with derivative equation data and x as the arguments

```python
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
```
</p>
</details>

<details><summary> Approach Next Point (New X)  </summary>
<p>

### Get New X
Using Linear Regression equation y = mx + c to obtain new initial point (x')

y = the value of the equation

m = the value of derivative

x = the initial point

```python
def getNextX(equation,derivative,x):
    y = equation
    m = derivative
    c = y - (m*x)

    x_new = -c / m
    return x_new
```
</p>
</details>

<details><summary> Main Function  </summary>
<p>

### Main Function
This function arrange above functions into steps to get new x on every iterations

The input arguments takes the equation, initial x, and target of the iterations count

Steps:

1) The function start with parsing the equation

2) After that, it find derivative of the equation

3) In n iterations it begins to obtain new X in order to gain equation value of approaching zero

4) The iteration stops if n iterations are complete or if the value of x has made the equation zero

```python
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

    return 
```
</p>
</details>

    


## License
MIT

 
