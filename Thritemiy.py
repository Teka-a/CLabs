import format as f

#  Функция зашифрования
def encrypt(text: str) -> str:
    encrypted = ""
    start = 0
    for i in text:
        c = f.arr_ru[(f.arr_ru.index(i) + text.index(i, start)) % len(f.arr_ru)]
        encrypted += c
        start += 1
    return f.prepare_out(encrypted, 1)

#  Функция расшифрования
def decrypt(text: str) -> str:
    decrypted = ""
    start = 0
    for i in text:
        p = f.arr_ru[(f.arr_ru.index(i) - text.index(i, start)) % len(f.arr_ru)]
        decrypted += p
        start += 1
    return f.prepare_out(decrypted, 2)


def main():
    print("Выбран шифр Тритемия.")
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
            encrypted = encrypt(prepared)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:

            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared)

            f.write_to_file("result.txt", decrypted, 2)

