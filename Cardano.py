import format as f
import cardanos as template


def encrypt(text: str) -> str:
    cardano = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    encrypted = ""
    count = 0
    templates = [template.a, template.b, template.c, template.d]

    for i in templates:
        for line in range(len(i)):
            for ind in i[line]:
                if count < len(text):
                    cardano[line][ind] = text[count]
                count += 1
    mas = []
    for card in cardano:
        for c in card:
            mas.append(c)
    encrypted += "".join(mas)
    return encrypted

def decrypt(text: str) -> str:
    decrypted = ""
    card = []
    position = 0
    templates = [template.a, template.b, template.c, template.d]
    for line in range(6):
        l = []
        for i in range(10):
            l.append(text[position])
            position += 1
        card.append(l)

    for temp in templates:
        for line in range(len(temp)):
            for ind in temp[line]:
                decrypted += card[line][ind]
    return decrypted


def blocks(text: str, do: str):
    output = ""
    if len(text) % 60 != 0 and do == "encrypt":
        text += "ф" * (60 - (len(text) % 60))
    for start in range(0, len(text), 60):
        if do == "encrypt":
            output += encrypt(text[start:start + 60])
        elif do == "decrypt":
            output += decrypt(text[start:start + 60])
    if do == "decrypt":
        count = 0
        for i in range(60):
            if output[-i] == "ф":
                count += 1
        output = output[0:-count]
    return output


def main():
    print("Выбран шифр решетка Кардано.")
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
            encrypted = blocks(prepared, "encrypt")
            prepared_after_enc = f.prepare_out(encrypted, 1)
            f.write_to_file("to-decrypt.txt", prepared_after_enc, 1)

        elif do == 2:
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = blocks(prepared, "decrypt")
            prepared_after_dec = f.prepare_out(decrypted, 2)
            f.write_to_file("result.txt", prepared_after_dec, 2)
