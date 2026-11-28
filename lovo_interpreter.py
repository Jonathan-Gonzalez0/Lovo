variables = {}
functions = {}
scopes = [variables]


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


def evaluate(node):

    if isinstance(node, (int, float, bool)):
        return node

    if isinstance(node, str):
        return node[1:-1]

    kind = node[0]

    if kind == "identifier":
        name = node[1]

        if name not in scopes[-1]:
            raise NameError(f"Undefined variable: {name}")

        return scopes[-1][name]

    if kind == "negate":
        return -evaluate(node[1])

    if kind == "+":
        return evaluate(node[1]) + evaluate(node[2])

    if kind == "-":
        return evaluate(node[1]) - evaluate(node[2])

    if kind == "*":
        return evaluate(node[1]) * evaluate(node[2])

    if kind == "/":
        right = evaluate(node[2])

        if right == 0:
            raise ZeroDivisionError("Division by zero")

        return evaluate(node[1]) / right

    if kind == "%":
        right = evaluate(node[2])

        if right == 0:
            raise ZeroDivisionError("Division by zero")

        return evaluate(node[1]) % right

    if kind == "==":
        return evaluate(node[1]) == evaluate(node[2])

    if kind == "!=":
        return evaluate(node[1]) != evaluate(node[2])

    if kind == "<":
        return evaluate(node[1]) < evaluate(node[2])

    if kind == ">":
        return evaluate(node[1]) > evaluate(node[2])

    if kind == "<=":
        return evaluate(node[1]) <= evaluate(node[2])

    if kind == ">=":
        return evaluate(node[1]) >= evaluate(node[2])

    if kind == "function_call":
        name = node[1]
        arguments = [evaluate(arg) for arg in node[2]]

        if name not in functions:
            raise NameError(f"Undefined function: {name}")

        parameters, body = functions[name]

        if len(arguments) != len(parameters):
            raise TypeError(f"Wrong number of arguments for {name}")

        local_variables = dict(zip(parameters, arguments))
        scopes.append(local_variables)

        try:
            for statement in body:
                execute(statement)

        except ReturnSignal as result:
            return result.value

        finally:
            scopes.pop()

        return None

    raise ValueError(f"Unsupported expression: {node}")


def execute(node):

    kind = node[0]

    if kind == "program":
        for statement in node[1]:
            execute(statement)

    elif kind == "declare":
        name = node[1]
        value = evaluate(node[2])
        scopes[-1][name] = value

    elif kind == "assign":
        name = node[1]

        if name not in scopes[-1]:
            raise NameError(f"Undefined variable: {name}")

        scopes[-1][name] = evaluate(node[2])

    elif kind == "print":
        value = evaluate(node[1])

        if isinstance(value, bool):
            print(str(value).lower())
        else:
            print(value)

    elif kind == "if":
        if evaluate(node[1]):
            for statement in node[2]:
                execute(statement)

        elif node[3] is not None:
            for statement in node[3]:
                execute(statement)

    elif kind == "while":
        while evaluate(node[1]):
            for statement in node[2]:
                execute(statement)

    elif kind == "for":
        execute(node[1])

        while evaluate(node[2]):
            for statement in node[4]:
                execute(statement)

            execute(node[3])

    elif kind == "function":
        name = node[1]
        parameters = node[2]
        body = node[3]

        functions[name] = (parameters, body)

    elif kind == "return":
        raise ReturnSignal(evaluate(node[1]))

    else:
        evaluate(node)
