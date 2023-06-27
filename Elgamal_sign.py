import format as f
from equation import eq as solve_equation

def set_params():
    while True:
        try:
            P = int(input("Введите P, простое число: "))
            if f.is_prime(P):
                break
            else:
                print("Ожидается простое число!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            x = int(input("Введите x, 1 < x < p : "))
            if x > 1 and x < P:
                break
            else:
                print("Введенное число не удовлетворяет условию!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            g = int(input("Введите g, 1 < g < p : "))
            if g > 1 and g < P:
                break
            else:
                print("Введенное число не удовлетворяет условию!")
        except ValueError:
            print("Введите число!")
    y = pow(g, x, P)

    while True:
        try:
            k = int(input("Введите k, взаимно простое с P: "))
            if f.gcd(k, P) == 1:
                break
            else:
                print("Введенное число не является взаимно простым с Р!")
        except ValueError:
            print("Введите число!")
    return [P, x, g, y, k]


def get_sign(text: str, k: int, g: int, P: int, x: int) -> list:
    hash = f.get_hash(text, P)
    a = pow(g, k, P)
    b = solve_equation(k, hash-x*a, P-1)
    return [a, b]

def check(text: str, y:  int, a: int, b: int, P: int, g: int) -> bool:
    hash = f.get_hash(text, P)
    a1 = pow((y**a)*(a**b), 1, P)
    a2 = pow(g, hash, P)
    if a1 == a2:
        return True
    return False


def main():
    print("Выбран алгоритм ЭЦП Elgamal.")
    [P, x, g, y, k] = set_params()
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
            [a, b] = get_sign(prepared, k, g, P, x)
            print("Sign: ", a, b)


        elif do == 2:
            while True:
                try:
                    a = int(input("Введите параметр a: "))
                    break
                except ValueError:
                    print("Введите число!")
            while True:
                try:
                    b = int(input("Введите параметр b: "))
                    break
                except ValueError:
                    print("Введите число!")
            sign_flag = check(prepared, y, a, b, P, g)
            if sign_flag:
                print("Подпись верна!")
            else:
                print("Подпись неверна!")




