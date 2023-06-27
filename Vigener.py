import format as f

def set_mode():
    while True:
        try:
            #  Введенное значение должно является числом
            print("\n\t1. Шифр Виженера с ключом шифртекстом. "
                  "\n\t2. Шифр Виженера с самоключом.")
            mode = int(input("Выберите опцию: "))
            break
        except ValueError:
            print("Введите число!")
    return mode


def set_params():
    while True:
        #  В качестве ключа допустимы только буквы русского алфавита
        print("При введении нескольких букв будет использована только первая!")
        key = input("Введите букву (допустимы только буквы русского алфавита): ")
        key = key.lower()
        if len(key) > 1:
            key = key[0]
        if f.is_rus_alphabet(key):
            break
        else:
            print("Ключ содержит недопустимые символы!")
    return key

#  Функция зашифрования
"""
    1 - cipher
    2 - self
"""
def encrypt(text: str, key_char: str, mode: int) -> str:
    encrypted = f.arr_ru[(f.arr_ru.index(text[0]) + f.arr_ru.index(key_char[0])) % len(f.arr_ru)]
    if mode == 1:
        for i in range(1, len(text)):
            c = f.arr_ru[(f.arr_ru.index(text[i]) + f.arr_ru.index(encrypted[i - 1])) % len(f.arr_ru)]
            encrypted += c
    else:
        for i in range(1, len(text)):
            c = f.arr_ru[(f.arr_ru.index(text[i]) + f.arr_ru.index(text[i - 1])) % len(f.arr_ru)]
            encrypted += c
    return f.prepare_out(encrypted, 1)

#  Функция расшифрования
"""
    1 - cipher
    2 - self
"""
def decrypt(text: str, key_char: str, mode: int) -> str:
    decrypted = f.arr_ru[(f.arr_ru.index(text[0]) - f.arr_ru.index(key_char[0])) % len(f.arr_ru)]
    if mode == 1:
        for i in range(1, len(text)):
            p = f.arr_ru[(f.arr_ru.index(text[i]) - f.arr_ru.index(text[i - 1])) % len(f.arr_ru)]
            decrypted += p
    else:
        for i in range(1, len(text)):
            p = f.arr_ru[(f.arr_ru.index(text[i]) - f.arr_ru.index(decrypted[i - 1])) % len(f.arr_ru)]
            decrypted += p
    return f.prepare_out(decrypted, 2)



def main():
    print("Выбран шифр Виженера.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            mode = set_mode()
            key = set_params()
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.prepare_in(text, 1)
            encrypted = encrypt(prepared, key, mode)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            mode = set_mode()
            key = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared, key, mode)

            f.write_to_file("result.txt", decrypted, 2)