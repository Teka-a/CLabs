import format as f

alphabet_30 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к',
          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
          'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'э', 'ю', 'я']

excluded = ["ь", "й", "ё"]


#  Ключевой параметр представляет собой слово/лозунг
def set_params():
    while True:
        key_word = input("Введите ключ (допустимы только буквы русского алфавита): ")
        key_word = key_word.lower()
        if f.is_rus_alphabet(key_word):
            same_chars = False
            mas = [0]
            for i in key_word:
                if i in mas or i in excluded:
                    same_chars = True
                    print("Ключ содержит повторяющиеся или исключенные буквы!")
                mas.append(i)
            if not same_chars:
                break
        else:
            print("Ключ содержит недопустимые символы!")
    return key_word

#  Формирование нового алфавита, в начале которого записано слово-ключ
def form_alphabet(word: str) -> list:
    alphabet = ""
    alphabet_blocks = []
    for char in word:
        alphabet += char
    for i in alphabet_30:
        if i not in alphabet:
            alphabet += i
    for block in range(0, 30, 6):
        alphabet_blocks += [alphabet[block:block+6]]
    return alphabet_blocks


#  Функция зашифрования
def encrypt(text: str, key: str) -> str:
    encrypted = ""
    new_pairs, pairs = [], []
    alphabet = form_alphabet(key)
    for s in range(0, len(text), 2):
        pairs += [text[s:s+2]]
    for pair in pairs:
        rows, cols = [], []
        for j in range(2):
            for line in alphabet:
                if pair[j] in line:
                    rows.append(alphabet.index(line))
                    cols.append(line.index(pair[j]))
        dif_by_col = abs(cols[0] - cols[1])
        x, y = "", ""
        if dif_by_col == 0:
            x += alphabet[(rows[0] + 1) % 5][cols[0]]
            y += alphabet[(rows[1] + 1) % 5][cols[1]]
        else:
            if cols[0] < cols[1] and rows[0] != rows[1]:
                x += alphabet[rows[0]][(cols[0] + dif_by_col) % 6]
                y += alphabet[rows[1]][(cols[1] - dif_by_col) % 6]
            elif cols[0] > cols[1] and rows[0] != rows[1]:
                x += alphabet[rows[0]][(cols[0] - dif_by_col) % 6]
                y += alphabet[rows[1]][(cols[1] + dif_by_col) % 6]
            elif rows[0] == rows[1]:
                x += alphabet[rows[0]][(cols[0] + 1) % 6]
                y += alphabet[rows[0]][(cols[1] + 1) % 6]
        new_pairs.append([x, y])
        encrypted += x + y
    return f.prepare_out(encrypted, 1)


#  Функция расшифрования
def decrypt(text: str, key: str) -> str:
    decrypted = ""
    new_pairs, pairs = [], []
    alphabet = form_alphabet(key)
    for s in range(0, len(text), 2):
        pairs += [text[s:s + 2]]
    for pair in pairs:
        rows, cols = [], []
        for j in range(2):
            for line in alphabet:
                if pair[j] in line:
                    rows.append(alphabet.index(line))
                    cols.append(line.index(pair[j]))
        dif_by_col = abs(cols[0] - cols[1])
        x, y = "", ""
        if dif_by_col == 0:
            x += alphabet[(rows[0] - 1) % 5][cols[0]]
            y += alphabet[(rows[1] - 1) % 5][cols[1]]
        else:
            if cols[0] < cols[1] and rows[0] != rows[1]:
                x += alphabet[rows[0]][(cols[0] + dif_by_col) % 6]
                y += alphabet[rows[1]][(cols[1] - dif_by_col) % 6]
            elif cols[0] > cols[1] and rows[0] != rows[1]:
                x += alphabet[rows[0]][(cols[0] - dif_by_col) % 6]
                y += alphabet[rows[1]][(cols[1] + dif_by_col) % 6]
            elif rows[0] == rows[1]:
                x += alphabet[rows[0]][(cols[0] - 1) % 6]
                y += alphabet[rows[0]][(cols[1] - 1) % 6]
        new_pairs.append([x, y])
        decrypted += x + y
    return f.prepare_out(decrypted, 2, 1)


def main():
    print("Выбран шифр Плэйфера.")
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
            prepared = f.prepare_in(text, 1, 1)
            #  Если подряд 2 одинаковые буквы - между нужно поставить ф
            mas = []
            for i in range(len(prepared) - 1):
                if prepared[i] == prepared[i + 1]:
                    mas += prepared[i] + "ф"
                else:
                    mas += prepared[i]
            mas.append(prepared[-1])
            #  Количество букв должно быть кратно 2
            if len(prepared) % 2 != 0:
                prepared += "ф"
            encrypted = encrypt(prepared, key)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            key = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared, key)

            f.write_to_file("result.txt", decrypted, 2)

