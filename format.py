import re
#словарь - индекс:пустой символ
spaces_indexes = {}
#хранит индексы в строке, на которых должны стоять заглавные буквы
upper_chars = []
hex_blocks = []

arr_ru_6 = [['а', 'б', 'в', 'г', 'д', 'е'],
        ['ж', 'з', 'и', 'й', 'к', 'л'],
        ['м', 'н', 'о', 'п', 'р', 'с'],
        ['т', 'у', 'ф', 'х', 'ц', 'ч'],
        ['ш', 'щ', 'ъ', 'ы', 'ь', 'э'],
        ['ю', 'я']]

arr_ru = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
          'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

arr_RU = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К',
          'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
          'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

arr_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'a', 'b', 'c', 'd', 'e', 'f']

def bigramm_list(str):
    result = []
    i = 0
    while i < len(str):
        result.append(str[i:i+2])
        i += 2
    return result

def is_prime(x):
    if x == 2:
        return True
    for i in range(2, (x//2)+1):
        if x % i == 0:
            return False
    return True

def MSB(text: str, n: int) -> str:
    return text[:n]


def LSB(text: str, n: int) -> str:
    return text[n:]


def XOR(a: str, b: str, size: int) -> str:
    c = ""
    for i in range(size//2):
        c += hex(int(a[2*i:2*i+2], 16) ^ int(b[2*i:2*i+2], 16))[2:].zfill(2)
    return c.zfill(size)

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def is_rus_alphabet(text: str) -> bool:
    flag = True
    for i in text:
        if i not in arr_ru:
            flag = False
            break
    return flag

def is_hex_alphabet(text: str) -> bool:
    flag = True
    for i in text:
        if i not in arr_hex:
            flag = False
            break
    return flag


def is_bin(text: str) -> bool:
    flag = True
    for i in text:
        if i not in {"0", "1"}:
            flag = False
            break
    return flag

def get_hash(text: str, p: int) -> int:
    hs = [0]
    for char in text:
        Mi = arr_ru.index(char) + 1
        h = hs[-1]
        hs.append(pow(h + Mi, 2, p))
    if hs[-1] == 0:
        hs.append(1)
    return hs[-1]


# Магма - 64 бита блок - 8 байт
# Кузненчик - 128 бит блок - 16 байт
def procedure2(text: str, block_size: int) -> str:
    add = "8"
    for i in range(block_size//8*2-1):
        add += "0"
    slice_end = abs(block_size//4 - (len(text) % (block_size//4)))
    text += add[:slice_end]
    return text


def unprocedure2(text: str) -> str:
    start_padding = ("0" + text[::-1]).index("8")
    text = text[:len(text) - start_padding]
    return text

def to_hex_array(text: str) -> list:
    hex_bytes = []
    start = 0
    for block in hex_blocks:
        byte_str = text[start:start+block]
        start += block
        hex_bytes.append(hex(int(byte_str, 16)))
    return hex_bytes


def to_hex(text: str) -> str:
    global hex_blocks
    in_hex = ""
    if hex_blocks != []:
        hex_blocks = []
    for i in text:
        hex_char = hex(arr_ru.index(i))[2:]
        hex_blocks.append(len(hex_char))
        in_hex += hex_char
    return in_hex

def from_hex(text: str) -> str:
    into_str = ""
    i = 0
    for s in hex_blocks:
        hex_present = text[i:i + s]
        char = arr_ru[int(hex_present, 16)]
        into_str += char
        i += s
    return into_str

"""
1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1
    text - строка, которую необходимо преобразовать
    option
        1 - заменить символы на буквенные обозначения
        2 - заменить буквенные обозначения на символы
"""
def replace_symbols(text: str, option: int) -> str:
    if option == 1:
        text = text.replace("ё", "е")
        text = text.replace(",", "зпт")
        text = text.replace(".", "тчк")
        text = text.replace("!", "звск")
        text = text.replace("?", "впрс")
        text = text.replace("-", "дфс")
        text = text.replace("—", "тире")
        text = text.replace(":", "двтч")


    elif option == 2:
        text = text.replace("зпт", ",")
        text = text.replace("тчк", ".")
        text = text.replace("звск", "!")
        text = text.replace("впрс", "?")
        text = text.replace("дфс", "-")
        text = text.replace("тире", "—")
        text = text.replace("двтч", ":")
    return text


"""
    text - строка, которую необходимо преобразовать
    option
        1 - заменить цифры на буквенные обозначения
        2 - заменить буквенные обозначения на цифры
"""
def replace_numbers(text: str, option: int) -> str:
    if option == 1:
        text = text.replace("0", "нольъ")
        text = text.replace("1", "одинъ")
        text = text.replace("2", "дваъ")
        text = text.replace("3", "триъ")
        text = text.replace("4", "четыреъ")
        text = text.replace("5", "пятьъ")
        text = text.replace("6", "шестьъ")
        text = text.replace("7", "семьъ")
        text = text.replace("8", "восемьъ")
        text = text.replace("9", "девятьъ")
    elif option == 2:
        text = text.replace("нольъ", "0")
        text = text.replace("одинъ", "1")
        text = text.replace("дваъ", "2")
        text = text.replace("триъ", "3")
        text = text.replace("четыреъ", "4")
        text = text.replace("пятьъ", "5")
        text = text.replace("шестьъ", "6")
        text = text.replace("семьъ", "7")
        text = text.replace("восемьъ", "8")
        text = text.replace("девятьъ", "9")
    return text



"""
    text - строка, которую необходимо преобразовать
    option
        1 - удалить пустые символы
        2 - создать строку, которая содержит пустые символы, согласно словарю spaces_indexes
"""
def replace_empty_symbols(text: str, option: int) -> str:
    if option == 1:
        text = re.sub("\s|\n|\r", '', text)
    elif option == 2:
        text_without_spaces = text
        text = ""
        i = 0
        j = 0
        while i < len(text_without_spaces):
            if j in spaces_indexes:
                space_char = spaces_indexes.get(j)
                if space_char == "space":
                    text += " "
                else:
                    text += space_char
                j += 1
            if j in upper_chars:
                text += text_without_spaces[i].upper()
            else:
                text += text_without_spaces[i]
            j += 1
            i += 1
    return text



"""

    text - строка, которую необходимо преобразовать
    option
        1 - подготовить строку для ШИФРОВАНИЯ
        2 - подготовить строку для РАСШИФРОВАНИЯ
    additional - указывает, необходимы ли дополнительные преобразования
        16 - перевести в 16-ричное представление
        1 - заменить й на и, ь на ъ (для шифра Плейфера)
"""
def prepare_in(text: str, option: int, additional: int = 0) -> str:
    global spaces_indexes, upper_chars
    if option == 1:
        spaces_indexes, upper_chars = {}, []
        text = replace_symbols(text, 1)
        text = replace_numbers(text, 1)
        for i in range(len(text)):
            if text[i] not in arr_RU and text[i] not in arr_ru:
                if text[i] == " ":
                    spaces_indexes[i] = "space"
                else:
                    spaces_indexes[i] = text[i]
            if text[i] in arr_RU:
                upper_chars.append(i)
        text = replace_empty_symbols(text.lower(), 1)

    elif option == 2:
        text = replace_empty_symbols(text.lower(), 1)

    if additional == 16:
        text = to_hex(text)
    elif additional == 1:
        text = text.replace("й", "и")
        text = text.replace("ь", "ъ")

    return text

"""

    text - строка, которую необходимо преобразовать
    option
        1 - подготовить строку после ШИФРОВАНИЯ
        2 - подготовить строку после РАСШИФРОВАНИЯ
    additional
        16 - из 16 ф
        1 - для Плэйфера
"""
def prepare_out(text: str, option: int, additional: int = 0) -> str:
    if additional == 16:
        text = from_hex(text)
    if additional == 1:
        text = text.replace("нолъъ", "нольъ")
        text = text.replace("пятъъ", "пятьъ")
        text = text.replace("шестъъ", "шестьъ")
        text = text.replace("семъъ", "семьъ")
        text = text.replace("восемъъ", "восемьъ")
        text = text.replace("девятъъ", "девятьъ")
    if option == 1:
        divided = ""
        count = 0
        for i in text:
            if count % 5 == 0 and count != 0:
                divided += " "
            divided += i
            count += 1
        text = divided
    elif option == 2:
        text = replace_empty_symbols(text, 2)
        text = replace_numbers(text, 2)
        text = replace_symbols(text, 2)

    return text


def read_from_file(name: str) -> str:
    file = open(name, "r", encoding="utf-8")
    text = file.read()
    text = text.replace("|\n", "")
    file.close()
    return text

"""
    1 - записать шифртекст по пять символов
    2 - записать расшифрованный текст
"""
def write_to_file(name: str, text: str, option: int):
    file = open(name, "w", encoding="utf-8")
    if option == 1:
        for i in range(len(text)//120 + 1):
            line = text[i * 120:i * 120 + 120] + "|\n"
            file.write(line)
    elif option == 2:
        file.write(text)
    file.close()
    print(f"Проверьте файл {name}")
