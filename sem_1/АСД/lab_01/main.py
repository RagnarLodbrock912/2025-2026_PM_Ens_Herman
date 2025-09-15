brackets = input("Введите строку")

start_brakets = ['(', '[', '{']
finish_brakets = [')', ']', '}']

stack = list()
flag = False

for bracket in brackets:
    if len(stack) == 0 and bracket in finish_brakets:
        flag = True
        break
    if bracket in finish_brakets:
        if start_brakets.index(stack[-1]) == finish_brakets.index(bracket):
            stack.pop()
        else:
            flag = True
            break
    else:
        stack.append(bracket)

if len(stack) != 0 or flag:
    print("Строка не существует")
else:
    print("Строка существует")
