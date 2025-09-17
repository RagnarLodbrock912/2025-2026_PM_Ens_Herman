eq = "2+7*(3/9+(7-8)*(8-28))-5*(8-9+7/8)="

operands = ['/', '*', '-', '+']
start_brakets = ['(', '[', '{']
finish_brakets = [')', ']', '}']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def check_eq(eq):
    if eq[-1] != '=':
        raise SyntaxError
    
    if eq[0] not in numbers and eq[0] not in start_brakets:
        raise SyntaxError
    
    stack = list()
    breackets_pos = dict()
    i = 0

    for el in eq:
        if len(stack) == 0 and el in finish_brakets:
            raise SyntaxError
        if el in finish_brakets:
            if start_brakets.index(stack[-1][0]) == finish_brakets.index(el):
                breackets_pos[stack[-1][1]] = i
                stack.pop()
            else:
                raise SyntaxError
        elif el in start_brakets:
            stack.append((el, i))

        i += 1
        
    if len(stack) != 0:
        raise SyntaxError

    return breackets_pos


def represent_eq(eq, brackets_pos):
    rep_eq = list()
    cur_num = ''
    i = 0

    while i < len(eq):
        if i in brackets_pos.keys():
            cur_num = ''
            new_brackets_pos = dict()
            for key, value in brackets_pos.items():
                if key > i and key < brackets_pos[i]:
                    new_brackets_pos[key - i -1] = value - i - 1
            rep_eq.append(represent_eq(eq[i+1:brackets_pos[i]], new_brackets_pos))
            i = brackets_pos[i]

        else:
            if eq[i] in operands:
                if cur_num != '':
                    rep_eq.append(float(cur_num))
                rep_eq.append(eq[i])
                cur_num = ''
            else:
                cur_num += eq[i]
        i += 1

    if cur_num != '':
        rep_eq.append(float(cur_num))
        

    return rep_eq

def calc_rep_eq(rep_eq):
    i = 0

    for elem in rep_eq:
        if isinstance(elem, list):
            rep_eq[i] = calc_rep_eq(rep_eq[i])
        
        i += 1

    new_rep_eq = list()

    i = 0
    while i < len(rep_eq):
        if rep_eq[i] == '*':
            new_rep_eq[-1] = new_rep_eq[-1] * rep_eq[i + 1]
            i += 1
        if rep_eq[i] == '/':
            if rep_eq[i + 1] == 0:
                raise SyntaxError
            new_rep_eq[-1] = new_rep_eq[-1] / rep_eq[i + 1]
            i += 1
        else:
            new_rep_eq.append(rep_eq[i])

        i+= 1


    res = new_rep_eq[0]

    i = 1
    while i < len(new_rep_eq):
        if new_rep_eq[i] == '+':
            res += new_rep_eq[i + 1]
            i += 1
        if new_rep_eq[i] == '-':
            res -= new_rep_eq[i + 1]
            i += 1

        i+= 1

    return res

print(calc_rep_eq(represent_eq(eq[:len(eq) - 1], check_eq(eq))))