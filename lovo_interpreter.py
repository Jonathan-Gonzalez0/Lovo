variables = {}
  
def evaluate(node):
    if isinstance(node, (int,float)):
        return node

    if isinstance(node, (str)):
        return node[1:-1]

    kind = node[0]

    if kind == "identifier":
        name = node[1]

        if name not in variables:
            raise NameError(f"Undefined variable: {name}")

        return variables[name]

    if kind == "+":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left + right

    if kind == "-":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left - right
    
    if kind == "*":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left * right

    if kind == "%":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left % right

    if kind == "/":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left / right

    if kind == "==":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left == right

    if kind == "!=":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left != right

    if kind == "<":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left < right

    if kind == ">":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left > right

    if kind == "<=":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left <= right

    if kind == ">=":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left >= right


    raise ValueError(f"Unsupported expression: {node}")

def execute(node):
    kind = node[0]

    if kind == "program":
        for statement in node[1]:
            execute(statement)

    elif kind == "declare":
        name = node[1]
        value = evaluate(node[2])
        variables[name] = value

    elif kind == "print":
        print(evaluate(node[1]))

    elif kind == "if":
        if(evaluate(node[1])):
            for statement in node[2]:
                execute(statement)
        else:
            if(node[3] == None):
                return
            for statement in node[3]:
                execute(statement)

    elif kind == "assign":
        name = node[1]
        variables[name] = evaluate(node[2])

    elif kind == "while":
        while(evaluate(node[1])):
            for statement in node[2]:
                execute(statement)