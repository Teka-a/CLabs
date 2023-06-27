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
            Q = int(input("Введите Q, простое число: "))
            if f.is_prime(Q):
                break
            else:
                print("Ожидается простое число!")
        except ValueError:
            print("Введите число!")
    N = int(P) * int(Q)
    M = (int(P) - 1) * (int(Q) - 1)
    print(f"φ(N) = ({P} - 1)*({Q} - 1) = {int(P) - 1}*{int(Q) - 1} = {M}")
    while True:
        try:
            E = int(input("Введите E, взаимно простое с φ(N): "))
            if f.gcd(int(E), M) == 1:
                break
            else:
                print("Введенное число не является взаимно простым с φ(N)!")
        except ValueError:
            print("Введите число!")
    D = solve_equation(int(E), 1, M)
    return [N, D, E]


def get_sign(text: str, D: int, N: int) -> int:
    hash = f.get_hash(text, N)
    sign = pow(hash, D, N)
    return sign

def check(text: str, E:  int, s: int, N: int) -> bool:
    hash = f.get_hash(text, N)
    m = pow(s, E, N)
    if m == hash:
        return True
    return False


def main():
    print("Выбран алгоритм ЭЦП RSA.")
    [N, D, E] = set_params()
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
            s = get_sign(prepared, D, N)
            print("Sign: ", s)


        elif do == 2:
            while True:
                try:
                    s = int(input("Введите подпись: "))
                    break
                except ValueError:
                    print("Введите число!")
            sign_flag = check(prepared, E, s, N)
            if sign_flag:
                print("Подпись верна!")
            else:
                print("Подпись неверна!")


