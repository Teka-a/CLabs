def gcd(m, a):
    a_first = a
    rs = []
    qs = []
    r = 1
    while r != 0:
        q = m // a
        qs.append(q)
        r = m - a*q
        rs.append(r)
        m, a = a, r
    if rs == [0]:
        qs.insert(0, a_first)
    else:
        qs.insert(0, rs[-2])
    return qs


def eq (a, b, m):
    p = m
    a %= m
    b %= m
    gcd_qs = gcd(m, a)
    d = gcd_qs[0]
    if d != 1:
        if b % d == 0:
            a //= d
            b //= d
            m //= d
            gcd(m, a)
        else:
            return ("Нет решений! b не кратно d")
    n = len(gcd_qs)-1
    gcd_qs[0] = "q"
    gcd_qs.insert(1, " ")
    P = ["P", 1]
    for t in range(n):
        if t == 0:
            P.append(gcd_qs[t + 2]*P[t + 1])
        else:
            P.append(gcd_qs[t + 2]*P[t + 1] + P[t])
    Pn = P[-2]
    xs = []
    x = ((-1) ** (n - 1) * b * Pn) % m

    for i in range(d):
        xn = (x + m * i) % p
        xs.append(xn)
    if len(xs) == 1:
        return xs[0]
    for x in range(len(xs)):
        xs[x] = str(xs[x])
    return xs