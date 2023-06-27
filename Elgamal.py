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
    k = []
    while True:
        try:
            num_k = int(input("Введите количество рандомизаторов: "))
            break
        except ValueError:
            print("Введите число!")

    while len(k) < num_k:
        while True:
            try:
                ki = int(input(f"Введите число, взаимно простое с φ(P) = {P - 1}: "))
                if f.gcd(ki, P - 1) == 1:
                    k.append(ki)
                    print(f"{len(k)}: {ki} было добавлено")
                    break
                else:
                    print("Введенное число не удовлетворяет условию!")
            except ValueError:
                print("Введите число!")
    return [P, x, g, y, k]



def encrypt(text: str, g: int, y: int, P: int, k: list) -> str:
    encrypted = ""
    l = len(k)
    for i in range(len(text)):
        ki = k[i%l]
        a = str(pow(g, ki, P))
        while len(a) < len(str(P)):
            a = "0" + a
        b = str((pow(y, ki, P) * (f.arr_ru.index(text[i])+1)) % P)
        while len(b) < len(str(P)):
            b = "0" + b
        encrypted += a + b
    return f.prepare_out(encrypted, 1)

def decrypt(text: str, P: int, x: int) -> str:
    decrypted = ""
    p = len(str(P))
    for i in range(0, len(text), p*2):
        a = text[i:i+p]
        b = text[i+p:i+2*p]
        M = solve_equation(int(a)**x, int(b), P)
        decrypted += f.arr_ru[M-1]
    return f.prepare_out(decrypted, 2)


def main():
    print("Выбран шифр Elgamal.")
    [P, x, g, y, k] = set_params()
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
            encrypted = encrypt(prepared, g, y, P, k)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared, P, x)

            f.write_to_file("result.txt", decrypted, 2)
