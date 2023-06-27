import format as f
import s_block as s


#  Ключ в 16-ом формате должен быть длины 64 ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff
def set_params():
    while True:
        key = input("Введите ключ в 16-ом формате, длиной 64: ")
        key = key.lower()
        if f.is_hex_alphabet(key):
            if len(key) == 64:
                break
            else:
                print("Ключ должен быть длины 64!")
        else:
            print("Ключ содержит недопустимые символы!")
    return key


#  Образующая функция F
def F(left: str, key: str) -> str:
    res = str(hex((int(left, 2) + int(key, 2)) % (2 ** 32))[2:])
    while len(res) != 8:
        res = '0' + res
    res = s.encrypt(res)
    res = bin(int(res, 16))[2:].zfill(32)
    #  Циклический сдвиг на 11 бит
    res = res[11:] + res[:11]
    return res


#  Функция зашифрования
def encrypt(text: str, key: str) -> str:
    nkeys = []
    for start in range(0, 256, 32):
        nkeys.append(key[start:start+32])
    keys = nkeys * 3
    keys.extend(nkeys[::-1])
    #  Разбиваем на 2 "ветви"
    a1 = bin(int(text[:8], 16))[2:]
    a0 = bin(int(text[8:], 16))[2:]
    for i in range(32):
        #  Меняем местами
        prev_left = a1
        a1 = a0
        a0 = bin(int(F(a0, keys[i]), 2) ^ int(prev_left, 2))[2:]
    encrypted = hex(int(a0, 2))[2:].zfill(8) + hex(int(a1, 2))[2:].zfill(8)
    return encrypted


#  Функция расшифрования
def decrypt(text: str, key: str) -> str:
    nkeys = []
    for start in range(0, 256, 32):
        nkeys.append(key[start:start + 32])
    keys = nkeys * 3
    keys.extend(nkeys[::-1])
    keys = keys[::-1]
    #  Разбиваем на 2 "ветви"
    a1 = bin(int(text[:8], 16))[2:].zfill(32)
    a0 = bin(int(text[8:], 16))[2:].zfill(32)
    for i in range(32):
        #  Меняем местами
        prev_left = a1
        a1 = a0
        a0 = bin(int(F(a0, keys[i]), 2) ^ int(prev_left, 2))[2:]
    decrypted = hex(int(a0, 2))[2:].zfill(8) + hex(int(a1, 2))[2:].zfill(8)
    return decrypted


#  Функция разбивания на блоки
def blocks_64(text: str, key: str, do: str):
    output = ""
    if do == "encrypt":
        text = f.procedure2(text, 64)
    for start in range(0, len(text), 16):
        if do == "encrypt":
            output += encrypt(text[start:start + 16], key).zfill(16)
        elif do == "decrypt":
            output += decrypt(text[start:start + 16], key).ljust(16, "0")
    if do == "decrypt":
        output = f.unprocedure2(output)
    return output


def main():
    print("Выбрана сеть Фейстеля.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            key = set_params()
            key = bin(int(key, 16))[2:]
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            encrypted = f.prepare_out(blocks_64(prepared, key, "encrypt"), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            key = set_params()
            key = bin(int(key, 16))[2:]
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = blocks_64(prepared, key, "decrypt")
            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))

            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)
