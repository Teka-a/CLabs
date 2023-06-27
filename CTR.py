import format as f
import Magma as m
import Kuznechik as h

#  ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff   12345678  Magma
#  8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef   1234567890abcef0  Kuznechik
#  Устанавливает ключ, инициализирующий вектор и алгоритм
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
    while True:
        IV = input("Введите инициализирующий вектор в 16-ом формате: ")
        IV = IV.lower()
        if f.is_hex_alphabet(IV):
            break
        else:
            print("Инициализирующий вектор содержит недопустимые символы!")
    while True:
        try:
            print("Доступные алгоритмы шифрования: \n\t1. Магма. "
                  "\n\t2. Кузнечик.")

            algo = int(input("Выберите алгоритм шифрования: "))
            break
        except ValueError:
            print("Введите число!")
    return [key, IV, algo]


#  Увеличение счетчика
def inc_ctr(ctr: str, size: int) -> str:
    internal = 0
    new_ctr = ""
    bit = "0"*(size - 1) + "1"
    for i in range(size//2):
        internal = int(ctr[2*i:2*i+2], 16) + int(bit[2*i:2*i+2], 16) + (internal << 8)
        new_ctr += hex(internal & 0xff)[2:].zfill(2)
    return new_ctr


#  Алгоритм Магма
def blocks_64(text: str, key: str, IV: str, do: str):
    output = ""
    IV = IV.ljust(16, "0")

    for start in range(0, len(text), 16):
        if do == "encrypt":
            P = text[start:start + 16]
            #  Сгенерировать гамму
            gamma = m.encrypt(IV, key)
            gamma = f.MSB(gamma, len(P))
            #  Наложение гаммы
            C = f.XOR(P, gamma, len(P))
            #  Увеличение счетчика
            IV = inc_ctr(IV, 16)
            output += C
        elif do == "decrypt":
            C = text[start:start + 16]
            #  Сгенерировать гамму
            gamma = m.encrypt(IV, key)
            gamma = f.MSB(gamma, len(C))
            #  Наложение гаммы
            P = f.XOR(C, gamma, len(C))
            #  Увеличение счетчика
            IV = inc_ctr(IV, 16)
            output += P
    return output


#  Алгоритм Кузнечик
def blocks_128(text: str, key: str, IV: str, do: str):
    output = ""
    IV = IV.ljust(32, "0")
    for start in range(0, len(text), 32):
        if do == "encrypt":
            P = text[start:start + 32]
            #  Сгенерировать гамму
            gamma = h.encrypt(IV, key)
            gamma = f.MSB(gamma, len(P))
            #  Наложение гаммы
            C = f.XOR(P, gamma, len(P))
            #  Увеличение счетчика
            IV = inc_ctr(IV, 32)
            output += C
        elif do == "decrypt":
            C = text[start:start + 32]
            #  Сгенерировать гамму
            gamma = h.encrypt(IV, key)
            gamma = f.MSB(gamma, len(C))
            #  Наложение гаммы
            P = f.XOR(C, gamma, len(C))
            #  Увеличение счетчика
            IV = inc_ctr(IV, 32)
            output += P
    return output


def main():
    print("Выбран Режим гаммирования")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            [key, IV, algo] = set_params()

            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            if algo == 1:
                key = bin(int(key, 16))[2:]
                encrypted = f.prepare_out(blocks_64(prepared, key, IV, "encrypt"), 1)
            else:
                encrypted = f.prepare_out(blocks_128(prepared, key, IV, "encrypt"), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            [key, IV, algo] = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            if algo == 1:
                key = bin(int(key, 16))[2:]
                decrypted = blocks_64(prepared, key, IV, "decrypt")
            else:
                decrypted = blocks_128(prepared, key, IV, "decrypt")

            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))

            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)
