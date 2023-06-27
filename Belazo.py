import format as f

#  Ключевой параметр представляет собой слово, по буквам которого будет сформирован "полиалфавит"
def set_params():
    while True:
        key = input("Введите ключ (допустимы только буквы русского алфавита): ")
        key = key.lower()
        if f.is_rus_alphabet(key):
            break
        else:
            print("Ключ содержит недопустимые символы!")
    return key

#  Функция зашифрования
def encrypt(text: str, key: str) -> str:
    encrypted = ""
    start = 0
    for i in text:
        key_char = text.index(i, start) % len(key)
        #  Замена
        c = f.arr_ru[(f.arr_ru.index(i) + f.arr_ru.index(key[key_char])) % len(f.arr_ru)]
        encrypted += c
        start += 1
    return f.prepare_out(encrypted, 1)

#  Функция расшифрования
def decrypt(text: str, key: str) -> str:
    decrypted = ""
    start = 0
    for i in text:
        key_char = text.index(i, start) % len(key)
        #  Замена
        p = f.arr_ru[(f.arr_ru.index(i) - f.arr_ru.index(key[key_char])) % len(f.arr_ru)]
        decrypted += p
        start += 1
    return f.prepare_out(decrypted, 2)


def main():
    print("Выбран шифр Белазо.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            key = set_params()
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.prepare_in(text, 1)
            encrypted = encrypt(prepared, key)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            key = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared, key)

            f.write_to_file("result.txt", decrypted, 2)

