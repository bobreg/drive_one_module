import serial
import minimalmodbus
from tkinter import messagebox
import time

adress = '85'
vkl_vikl_module = ['00', '00', '00']
otvet = ['b', "'", "'"]
flag_sbros_avarii = False
flag_start_stop_obmen = True


def find_port():
    global port_open
    port = 0
    ports = dict()
    for number_port in range(10):
        try:
            i = serial.Serial('com{}'.format(number_port), 115200, timeout=1, stopbits=2, bytesize=7)
            ports[number_port] = ('com{}'.format(number_port))
            i.close()
        except serial.serialutil.SerialException:
            pass
    if len(ports) == 0:
        messagebox.showinfo('Ахтунг!', message='Отсутствуют сом-порты')
        exit()
    elif len(ports) > 1:
        print(ports)
        port = int(input('Выберите нужный порт:'))
    elif len(ports) == 1:
        port = str(ports.keys())[11:12]  # port.keys возвращает что-то типа (dict_keys([2])).
        # это надо перевести в строку, затем извлечь слайсом двойку
        # и передать двойку в port
    port_open = serial.Serial('com{}'.format(port), 115200, timeout=0.2, stopbits=2, bytesize=7)


def obmen():
    global otvet
    global vkl_vikl_module
    global adress
    global port_open
    global flag_sbros_avarii
    global flag_start_stop_obmen
    while True:
        if flag_start_stop_obmen is True:
            LRC = hex(ord(minimalmodbus._calculateLrcString(adress + '44' + '47' +
                                                            ''.join(map(str, vkl_vikl_module)))))[2:]
            message = ':' + adress + '44' + '47' + \
                      ''.join(map(str, vkl_vikl_module)) + LRC.upper() + '\r\n'
            print(message)
            port_open.write(message.encode('ascii'))
            answer = repr(port_open.read(50))[1:]
            if answer[1] == ':' and answer[-2] == 'n' and answer[-4] == 'r':
                if int(hex(ord(minimalmodbus._calculateLrcString(answer[2:-7])))[2:].upper(), 16) == int(answer[-7:-5], 16):
                    otvet = answer
                else:
                    otvet = ''
            else:
                otvet = ''
            print(otvet)
        if flag_sbros_avarii is True:
            sbros_avarii()
            flag_sbros_avarii = False
        else:
            time.sleep(0.1)  # чтобы не зависало окно


def sbros_avarii():
    global port_open
    LRC = hex(ord(minimalmodbus._calculateLrcString(adress + '050201FF00')))[2:]
    port_open.write((':' + adress + '050201FF00' + LRC + '\r\n').encode('ascii'))
    print(repr(port_open.read(100)))
    print(':' + adress + '050201FF00' + LRC + '\r\n')


def return_dannie_moduls_to_window():
    global otvet
    return otvet


if __name__ == '__main__':
    pass