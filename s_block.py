import format as f


#  Фиксированный набор подстановок (по ГОСТ Р 34.12-2015)
S_blocks = [
    ["c", "4", "6", "2", "a", "5", "b", "9", "e", "8", "d", "7", "0", "3", "f", "1"],
    ["6", "8", "2", "3", "9", "a", "5", "c", "1", "e", "4", "7", "b", "d", "0", "f"],
    ["b", "3", "5", "8", "2", "f", "a", "d", "e", "1", "7", "4", "c", "9", "6", "0"],
    ["c", "8", "2", "1", "d", "4", "f", "6", "7", "0", "a", "5", "3", "e", "9", "b"],
    ["7", "f", "5", "a", "8", "1", "6", "d", "0", "9", "3", "e", "b", "4", "2", "c"],
    ["5", "d", "f", "6", "9", "2", "c", "a", "b", "7", "8", "1", "4", "3", "e", "0"],
    ["8", "e", "2", "5", "6", "9", "1", "c", "f", "4", "b", "0", "d", "a", "3", "7"],
    ["1", "7", "e", "d", "0", "5", "8", "3", "4", "f", "a", "6", "9", "c", "b", "2"]
]


#  Функция зашифрования
def encrypt(text: str) -> str:
    encrypted = ""
    text = text[::-1]
    for i in range(len(text)):
        #  Замена
        c = S_blocks[i % 8][int(text[i], 16)]
        encrypted += c
    return encrypted[::-1]


#  Функция расшифрования
def decrypt(text: str) -> str:
    decrypted = ""
    text = text[::-1]
    for i in range(len(text)):
        #  Обратная замена
        p = hex(S_blocks[i % 8].index(text[i]))[2:]
        decrypted += p
    return decrypted[::-1]


def main():
    print("Выбран S-блок замены.")
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
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            encrypted = f.prepare_out(encrypt(prepared), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared)
            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))
            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)

