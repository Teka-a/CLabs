from equation import eq as solve_equation
from tabulate import tabulate

def double_dot (x1, y1, p, a):
    if (y1 != 0):
        lamup = (3 * (x1 ** 2)) + a
        lamdown = 2 * y1
        lam = solve_equation(lamdown, lamup, p)
        x3 = (lam ** 2 - 2 * x1) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return [x3, y3]
    else:
        return ["not"]


def sum_dots (x1, y1, x2, y2, p):
    if ((x2 - x1) != 0):
        lamup = y2 - y1
        lamdown = x2 - x1
        lam = solve_equation(lamdown, lamup, p)
        x3 = (lam ** 2 - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return [x3, y3]
    else:
        return ["not"]

def count_compositions(k, P, p, a):
    for i in range(2, k):
        if (i % 2 == 0):
            if (P[i // 2] == ['not']):
                P[i] = P[i // 2]
            else:
                P[i] = double_dot(P[i // 2][0], P[i // 2][1], p, a)
        else:
            if (P[1][0] != P[i - 1][0]):
                if (P[i - 1] == ['not']):
                    P[i] = P[1]
                else:
                    P[i] = sum_dots(P[1][0], P[1][1], P[i - 1][0], P[i - 1][1], p)
            elif ((P[1][0] == P[i - 1][0]) and (P[1][1] == (-P[i - 1][1]) % p)):
                P[i] = ['not']
            else:
                P[i] = double_dot(P[1][0], P[1][1], p, a)
    return P

def map_of_dots (a, p, group_of_dots):
    table = [[0]] * len(group_of_dots)
    for i in range(len(table)):
        table[i] = [0] * p
        table[i][1] = group_of_dots[i]
    dots_order = []
    for P in table:
        P = count_compositions(p, P, p, a)
        for i in range(len(group_of_dots)):
            if P[i] == ['not']:
                dots_order.append([P[1], i])
                break
            if i == len(P) - 1:
                dots_order.append([P[1], len(P)])
                break
    n_d = []
    n_d.append(dots_order)
    print(tabulate(n_d))

    return dots_order