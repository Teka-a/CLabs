import format as f
from equation import eq as solve_equation
import dots as d
import EC

def set_params():
    while True:
        try:
            a = int(input("Введите а: "))
            break
        except ValueError:
            print("Введите число!")
    while True:
        try:
            b = int(input("Введите b: "))
            break
        except ValueError:
            print("Введите число!")
    while True:
        try:
            p = int(input("Введите p, простое число: "))
            if f.is_prime(p):
                break
            else:
                print("Ожидается простое число!")
        except ValueError:
            print("Введите число!")

    print("Ваше уравнение: E" + str(p) + "(" + str(a) + "," + str(b) + "): y^2 ≡ x^3 +", a, "x +", b, "( mod", p, ")")

    check_up = ((4 * (a ** 3)) + (27 * (b ** 2)))
    check = solve_equation(108, check_up, p)

    invariant = solve_equation(check_up, 1728 * 4 * (a ** 3), p)

    print(f"\nДискриминант D = (4a^3 + 27b^2)/108 (mod p) = {check} (mod {p}) ≠ 0")
    print(f"\nИнвариант j = (1728*4a^3)/(4a^3 + 27b^2) (mod p) = {invariant}")

    if (check == 0):
        print("Это особая кривая! Она не представляет интереса для криптографии(")
        raise SystemExit


    dots = d.find_dots(a, b, p)
    dots_order = EC.map_of_dots(a, p, dots)
    q = 0
    G = [0, 0]
    while True:
        print("Выберите точку G: ")
        while True:
            try:
                x1 = int(input("Введите x1: "))
                break
            except ValueError:
                print("Введите число!")
        while True:
            try:
                y1 = int(input("Введите y1: "))
                break
            except ValueError:
                print("Введите число!")
        G = [x1, y1]
        if G not in dots:
            print("Данной точки не существует!")
        else:
            for dot in dots_order:
                if G == dot[0]:
                    order = dot[1]
                    if f.is_prime(order):
                        q = order
                        break
                    else:
                        print("Порядок точки не является простым!")
                else:
                    continue
            if q != 0:
                break

    while True:
        try:
            k = int(input(f"Введите k, 0 < k < {q}: "))
            if abs(k) >= q:
                print("Введенное число не удовлетворяет условию!")
            else:
                k = abs(k) + 1
                break
        except ValueError:
            print("Введите число!")
    while True:
        try:
            u = int(input(f"Введите u, 0 < k < {q}: "))
            if abs(u) >= q:
                print("Введенное число не удовлетворяет условию!")
            else:
                u = abs(u) + 1
                break
        except ValueError:
            print("Введите число!")

    P = [[0]] * (k)
    P[1] = G
    Y = [[0]] * (u)
    Y[1] = G

    P = EC.count_compositions(k, P, p, a)


    Y = EC.count_compositions(u, Y, p, a)

    x = P[-1][0]
    return [x, q, k-1, u-1, Y[-1], G, p, a]

def get_sign(text: str, x: int, k: int, q: int, u: int, p: int) -> list:
    hash = f.get_hash(text, p)
    r = x % q
    if r == 0:
        print("r = 0, необходимо изменить k")
        raise SystemExit
    s = ((k * hash) + (r * u)) % q
    if s == 0:
        print("s = 0, необходимо изменить k")
        raise SystemExit
    return [r, s]

def check(text: str, r: int, s: int, q: int, Y: list, G: list, p: int, a: int) -> bool:
    hash = f.get_hash(text, p)
    if r < 0 or s > q or r > q or s < 0:
        return False
    u1 = (s * pow(hash, -1, q)) % q
    u2 = (-r * pow(hash, -1, q)) % q
    P1 = [[0]] * (u1+1)
    P1[1] = G
    P1 = EC.count_compositions(u1+1, P1, p, a)
    P2 = [[0]] * (u2+1)
    P2[1] = Y
    P2 = EC.count_compositions(u2+1, P2, p, a)
    P = EC.sum_dots(P1[-1][0], P1[-1][1], P2[-1][0], P2[-1][1], p)
    print(f"u1 = {u1}, u2 = {u2}, P1 = {P1}, P2 = {P2}, res = {P}")
    if (P[0] % q) == r:
        return True
    return False


def main():
    print("Выбран алгоритм ЭЦП ГОСТ 34.10-2012.")
    [x, q, k, u, Y, G, p, a] = set_params()
    text = f.read_from_file("to-encrypt.txt")
    prepared = f.prepare_in(text, 1)
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Подписать. "
              "\n\t2. Проверить подпись. ")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            [r, s] = get_sign(prepared, x, k, q, u, p)
            print("Sign: ", r, s)


        elif do == 2:
            while True:
                try:
                    r = int(input("Введите параметр r: "))
                    break
                except ValueError:
                    print("Введите число!")
            while True:
                try:
                    s = int(input("Введите параметр s: "))
                    break
                except ValueError:
                    print("Введите число!")
            sign_flag = check(prepared,  r, s, q, Y, G, p, a)
            if sign_flag:
                print("Подпись верна!")
            else:
                print("Подпись неверна!")



