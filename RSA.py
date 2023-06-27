import format as f
from equation import eq as solve_equation

def set_decrypt_params():
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
    return [N, D]



def set_encrypt_params():
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
    return [N, E]

def encrypt(text: str, E: int, N: int) -> str:
    encrypted = ""
    for i in text:
        c = str(pow(f.arr_ru.index(i) + 1, E, N))
        while len(c) < len(str(N)):
            c = "0" + c
        encrypted += c
    return f.prepare_out(encrypted, 1)

def decrypt(text: str, D: int, N: int) -> str:
    decrypted = ""
    n = len(str(N))
    for i in range(0, len(text), n):
        decrypted += f.arr_ru[pow(int(text[i:i+n]), D, N) - 1]
    return f.prepare_out(decrypted, 2)


def main():
    print("Выбран шифр RSA.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            [N, E] = set_encrypt_params()
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.prepare_in(text, 1)
            encrypted = encrypt(prepared, E, N)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            [N, D] = set_decrypt_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared, D, N)

            f.write_to_file("result.txt", decrypted, 2)
