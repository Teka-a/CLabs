import format as f
import math


#  Ключевой параметр представляет собой слово
def set_params():
    while True:
        key_word = input("Введите ключ (допустимы только буквы русского алфавита): ")
        key_word = key_word.lower()
        if f.is_rus_alphabet(key_word):
            break
        else:
            print("Ключ содержит недопустимые символы!")
    return key_word


#  Преобразование ключевого слова в индексы(столбцы)
def word_into_ind(word: str) -> list:
    order = [0] * len(word)
    inds = []
    correlation = {}
    for char in word:
        inds.append(f.arr_ru.index(char))
    for j in range(len(word)):
        m = min(inds)
        order[inds.index(m)] = j
        correlation[j + 1] = f.arr_ru[m]
        inds[inds.index(m)] = 100
    return order


#  Функция зашифрования
def encrypt(text: str, key: str) -> str:
    encrypted = ""
    count = 0
    table = []
    order = word_into_ind(key)
    cols = len(key)
    for block in range(0, len(text), cols):
        row = [text[block:block + cols]]
        table.append(row)
    enc_mas = [0]*len(key)
    mas_by_word = []
    for j in range(cols):
        chars_from_col = []
        for r in range(len(table)):
            if j < len(table[r][0]):
                chars_from_col.append(table[r][0][j])
        mas_by_word.append(chars_from_col)
    for ind in order:
        enc_mas[ind] = mas_by_word[count]
        count += 1
    for enc in enc_mas:
        encrypted += "".join(enc)
    return f.prepare_out(encrypted, 1)


#  Функция расшифрования
def decrypt(text: str, key: str) -> str:
    decrypted = ""
    count = 0
    start = 0
    order = word_into_ind(key)
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    long_rows = len(text) % cols

    for k in range(cols):
        pos_in_ord = order.index(count)
        if pos_in_ord < long_rows:
            order[pos_in_ord] = [text[start:start+rows]]
            start += rows
        elif len(text) % cols == 0:
            order[pos_in_ord] = [text[start:start + rows]]
            start += rows
        else:
            order[pos_in_ord] = [text[start:start + rows-1]]
            start += rows-1
        count += 1
    s = ""
    for p in order:
        s += p[0]
    for col in range(rows):
        for i in range(cols):
            if len(s) % cols == 0:
                decrypted += order[i][0][col]
            else:
                if i > long_rows-1 and col == rows-1:
                    break
                decrypted += order[i][0][col]
    return f.prepare_out(decrypted, 2)

def main():
    print("Выбран шифр вертикальная перестановка.")
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
