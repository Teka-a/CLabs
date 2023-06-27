import format as f


def set_params():
    while True:
        try:
            #  Введенное значение должно является числом
            mod = int(input("Ввведите модуль: "))
            break
        except ValueError:
            print("Введите число!")
    while True:
        try:
            a = int(input("Введите нечетное число а (будет преобразовано по модулю): "))
            a = a % mod
            if a % 2 == 0:
                print("Введенное а является четным! Выберите нечетное число.")
            else:
                break
        except ValueError:
            print("Введите число!")
    while True:
        try:
            c = int(input(f"Введите число c(будет преобразовано по модулю), взаимно простое с модулем {mod}: "))
            c = c % mod
            if f.gcd(c, mod) != 1:
                print("Введенное c не является взаимно простым с модулем.")
            else:
                break
        except ValueError:
            print("Введите число!")
    while True:
        try:
            To = int(input("Введите исходную величину To(будет преобразовано по модулю), выбранную в качестве порождающего числа: "))
            To = To % mod
            break
        except ValueError:
            print("Введите число!")
    return [abs(mod), a, c, To]


def generator_T(m: int, a: int, c: int, To: int, text_len: int) -> list:
    Ts = [To]
    for i in range(1, text_len):
        Ts.append((Ts[i-1] * a + c) % m)
    return Ts


def encrypt(text: str, key: list, mod: int) -> str:
    text_mas = []
    cipher = []
    for char in text:
        text_mas.append(f.arr_ru.index(char)+1)
    for i in range(len(text_mas)):
        #  Сложение по модулю с гаммой
        c = (text_mas[i] + key[i]) % mod
        if c == 0:
            c = 32
        c = str(c)
        if len(c) < 2:
            c = "0" + c
        cipher.append(c)
    encrypted = "".join(cipher)
    return f.prepare_out(encrypted, 1)


def decrypt(text: str, key: list, mod: int) -> str:
    cipher, plain = [], []
    for start in range(0, len(text), 2):
        cipher.append(int(text[start:start+2]))
    for i in range(len(cipher)):
        #  Вычитание гаммы по модулю
        c = (cipher[i] - key[i]) % mod
        plain.append(f.arr_ru[c-1])
    decrypted = "".join(plain)
    return f.prepare_out(decrypted, 2)




def main():
    print("Выбран шифр одноразовый блокнот Шеннона.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            [mod, a, c, To] = set_params()
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.prepare_in(text, 1)

            key = generator_T(mod, a, c, To, len(prepared))
            encrypted = encrypt(prepared, key, mod)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            [mod, a, c, To] = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            key = generator_T(mod, a, c, To, len(prepared))
            decrypted = decrypt(prepared, key, mod)

            f.write_to_file("result.txt", decrypted, 2)