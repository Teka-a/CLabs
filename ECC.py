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


    R = [[0]] * (k)
    R[1] = G
    D = [[0]] * (u)
    D[1] = G
    P = [[0]] * (k)
    R = EC.count_compositions(k, R, p, a)
    R = R[-1]
    D = EC.count_compositions(u, D, p, a)
    D = D[-1]
    P[1] = D
    P = EC.count_compositions(k, P, p, a)
    x = P[-1][0]
    print(f"R = {R}")
    return [R, x, p, u, a]


def encrypt(text: str, R: list, x: int, p: int) -> list:
    encrypted = []
    for i in text:
        e = str((f.arr_ru.index(i) * x) % p)
        while len(e) < len(str(p)):
            e = "0" + e
        encrypted.append(e)
    encrypted = "".join(encrypted)
    return [R, encrypted]


def decrypt(R: list, encrypted: list, p: int, u: int, a: int) -> str:
    decrypted = ""
    Q = [[0]] * (u)
    Q[1] = R
    Q = EC.count_compositions(u, Q, p, a)
    Q = Q[-1]
    x = Q[0]
    x = pow(x, -1, p)
    for e in encrypted:
        decrypted += f.arr_ru[(int(e)*x) % p]
    return f.prepare_out(decrypted, 2)

def main():
    print("Выбран шифр ECC.")
    [R, x, p, u, a] = set_params()
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.prepare_in(text, 1)
            encrypted = encrypt(prepared, R, x, p)
            R = encrypted[0]
            encrypted = f.prepare_out(encrypted[1], 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(R, f.bigramm_list(prepared), p, u, a)

            f.write_to_file("result.txt", decrypted, 2)