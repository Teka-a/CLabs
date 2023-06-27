import Magma as m
import Kuznechik as h
import CTR, OFB, CBC, CFB, MAC

def print_options():
    print("0. Exit.")
    print("    1. Режим простой замены. ")
    print("    2. Режим гаммирования. ")
    print("    3. Режим гаммирования с обратной связью по выходу. ")
    print("    4. Режим простой замены с зацеплением. ")
    print("    5. Режим гаммирования с обратной связью по шифртексту. ")
    print("    6. Режим выработки имитовставки. ")


def main():
    print("Выбран ГОСТ 34.13-2015")
    while True:
        print_options()

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            while True:
                try:
                    print("Доступные алгоритмы шифрования: \n\t1. Магма. "
                          "\n\t2. Кузнечик.")

                    algo = int(input("Выберите алгоритм шифрования: "))
                    break
                except ValueError:
                    print("Введите число!")
            if algo == 1:
                m.main()
            else:
                h.main()

        elif do == 2:
            CTR.main()
        elif do == 3:
            OFB.main()
        elif do == 4:
            CBC.main()
        elif do == 5:
            CFB.main()
        elif do == 6:
            MAC.main()