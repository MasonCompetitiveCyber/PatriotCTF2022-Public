from string import ascii_lowercase
from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import parse_expr

from pwn import remote, context

context.log_level = 'error'
p = remote("localhost", 8000)

def math():
    main = []
    p.recvline()
    main.append(p.recvline().decode().strip().replace(" ", ""))
    main.append(p.recvline().decode().strip().replace(" ", ""))
    main.append(p.recvline().decode().strip().replace(" ", ""))
    main.append(p.recvline().decode().strip().replace(" ", ""))
    main.append(p.recvline().decode().strip().replace(" ", ""))
    p.recvline()
    # print(main)

    vars = iter(ascii_lowercase)

    eqs = {}
    mapping = {}
    n = 5

    for i in range(n):
        eq = main[i]
        answer = eq.split("=")[1]
        tokens = eq.split("=")[0].split("+")
        
        for token in tokens:
            token = token
            if token not in mapping.keys():
                mapping[token] = next(vars)

        sympy_eq = mapping[tokens[0]]
        for token in tokens[1:]:
            sympy_eq += " + " + mapping[token]

        eqs[i] = (sympy_eq, answer)

    syms = symbols(tuple(mapping.values()))

    solution = solve((Eq(parse_expr(eqs[0][0]), int(eqs[0][1])), Eq(parse_expr(eqs[1][0]), int(eqs[1][1])), Eq(parse_expr(eqs[2][0]), int(eqs[2][1])), Eq(parse_expr(eqs[3][0]), int(eqs[3][1])), Eq(parse_expr(eqs[4][0]), int(eqs[4][1]))), syms)

    total = str(sum(solution.values()))
    print(total)
    p.send(total.encode())
    p.recvline()
    print(p.recvline())

for _ in range(5):
    math()

p.recvline()
print(p.recvline())