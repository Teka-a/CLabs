import format as f

def set_params():
    while True:
        try:
            p = int(input("Введите p, простое число: "))
            if f.is_prime(p):
                break
            else:
                print("Ожидается простое число!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            q = int(input(f"Введите q, простой сомножитель числа {p-1}: "))
            if f.is_prime(q):
                if (p - 1) % q == 0:
                    break
                else:
                    print(f"Введенное число не является простым сомножителем числа {p - 1}!")
            else:
                print("Ожидается простое число!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            a = int(input(f"Введите a, больше 1 и меньше {p - 1}, причем такое что а в степени {q} по модулю {p} = 1: "))
            if a >= 1 and a <= p-1:
                if pow(a, q, p) == 1:
                    break
                else:
                    print(f"Введенное число не удовлетворяет условию!")
            else:
                print("Введенное число вне указанного диапазона!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            x = int(input(f"Введите x, меньше {q}: "))
            if x > q:
                print("Введенное число вне указанного диапазона!")
            else:
                break
        except ValueError:
            print("Введите число!")
    y = pow(a, x, p)
    return [a, p, q, x, y]


def get_sign(text: str, a: int, p: int, q: int, x: int) -> list:
    hash = f.get_hash(text, p)

    while True:
        k = int(input(f"Введите k, меньше {q}: "))
        if k > q:
            print("Введенное число вне указанного диапазона!")
        r = pow(pow(a, k, p), 1, q)
        s = pow(x * r + k * hash, 1, q)
        if r != 0 and k < q:
            break
    return [r, s]


def check(text: str, r:  int, s: int, p: int, q: int, a: int, y: int) -> bool:
    hash = f.get_hash(text, p)
    v = pow(hash, q-2, q)
    z1 = pow(s*v, 1, q)
    z2 = pow((q-r)*v, 1, q)
    u = pow(pow(pow(a, z1) * pow(y, z2), 1, p), 1, q)
    print(u, r)
    if u == r:
        return True
    return False


def main():
    print("Выбран алгоритм ЭЦП ГОСТ 34.10-94.")
    [a, p, q, x, y] = set_params()
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
            [r, s] = get_sign(prepared, a, p, q, x)
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
            sign_flag = check(prepared,  r, s, p, q, a, y)
            if sign_flag:
                print("Подпись верна!")
            else:
                print("Подпись неверна!")


