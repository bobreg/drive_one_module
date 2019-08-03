import tkinter
from threading import Thread
import opros
import time

flag_umi = False

opros.find_port()  # поиск сом-порта


def vkl_umi():
    global flag_umi
    flag_umi = not flag_umi
    if flag_umi is True:
        opros.vkl_vikl_module = ['01', '01', '01']
        button_onOff_umi['bg'] = 'green yellow'
        button_onOff_umi['text'] = 'ВЫКЛ'
    else:
        opros.vkl_vikl_module = ['00', '00', '00']
        button_onOff_umi['bg'] = 'snow3'
        button_onOff_umi['text'] = 'ВКЛ'


def sbros_avarii():
    opros.flag_sbros_avarii = True


def stop_obmen():
    opros.flag_start_stop_obmen = not opros.flag_start_stop_obmen


def avaria_umi(ks):
    ksb1 = list(bin(int(ks[:2], 16))[2:])  # превращение НЕХ значений в BIN значения
    ksb2 = list(bin(int(ks[2:], 16))[2:])  # превращение НЕХ значений в BIN значения
    ksb1 = ['0' for i in range(8 - len(ksb1))] + ksb1  # превращение BIN значений в массив из 8 битов
    ksb2 = ['0' for i in range(8 - len(ksb2))] + ksb2  # превращение BIN значений в массив из 8 битов
    for i in range(-1, -4, -1):
        if ksb2[i] == '1':
            globals()['state{}'.format(-i - 1)]['bg'] = 'green'
        else:
            globals()['state{}'.format(-i - 1)]['bg'] = 'blue'
    for i in range(-4, -9, -1):
        if ksb2[i] == '0':
            globals()['state{}'.format(-i - 1)]['bg'] = 'green'
        else:
            globals()['state{}'.format(-i - 1)]['bg'] = 'Red'
    for i in range(-9, -13, -1):
        if ksb1[i + 8] == '0':
            globals()['state{}'.format(-i - 1)]['bg'] = 'green'
        else:
            globals()['state{}'.format(-i - 1)]['bg'] = 'Red'


def update_window():
    global otvet
    while True:
        otvet = opros.return_dannie_moduls_to_window()
        if len(list(otvet)) < 10:
            text_Pin['text'] = 'обмена\nнет'
            text_Pin['font'] = 'arial 11 bold'
            text_Pin['fg'] = 'red'
        else:
            text_Pin['font'] = 'arial 9 bold'
            text_Pin['fg'] = 'black'
            text_Pin['text'] = int(otvet[8:10], 16)
            text_Pout['text'] = int(otvet[10:12], 16)
            text_Potr['text'] = int(otvet[12:14], 16)
            text_temperature['text'] = int(otvet[14:16], 16)
            text_supply_voltage['text'] = int(otvet[16:18], 16)
            avaria_umi(otvet[18:22])
        time.sleep(0.1)


thread_obmen = Thread(target=opros.obmen, daemon=True)
thread_update_window = Thread(target=update_window, daemon=True)

'''Создание окна'''
window = tkinter.Tk()
window.title("УМХ 9,6-400")
window.geometry("600x270")

button_onOff_umi = tkinter.Button(window, text='ВКЛ', width=10, heigh=1, command=vkl_umi, font='arial 11')
sbros_avarii_button = tkinter.Button(window, text='Сброс аварии', width=10, heigh=1, command=sbros_avarii,
                                     font='arial 11')
stop_obmen = tkinter.Checkbutton(window, text='стоп обмен', command=stop_obmen)

label_state_umi = tkinter.Label(window, text='Состояние модуля', font='Verdana 8 bold')
label_electrical_network = tkinter.Label(window, text='Сеть')
label_power_supply = tkinter.Label(window, text='ИП')
label_microwave_path = tkinter.Label(window, text='СВЧ\nВКЛ')
label_Pin_low = tkinter.Label(window, text='Рвх\nlow')
label_Pin_high = tkinter.Label(window, text='Рвх\nhigh')
label_Pout_low = tkinter.Label(window, text='Рвых\nlow')
label_Potr_high = tkinter.Label(window, text='Ротр\nhigh')
label_overheat = tkinter.Label(window, text='Перегр')
label_overload_TQ = tkinter.Label(window, text='T/Q')
label_not_modulation_pulses = tkinter.Label(window, text='Нет\nИМ')
label_power_failure = tkinter.Label(window, text='Авар\nпит')
label_temperature_sensor_broken = tkinter.Label(window, text='ДТ\nнеис.')

for i in range(12):
    globals()['state{}'.format(i)]= tkinter.Canvas(window, width=20, height=20, bg='blue')

c = tkinter.Canvas(window, width=590, height=3, bg='black')

label_Pin = tkinter.Label(window, text='Рвх, у.е.:')
label_Pout = tkinter.Label(window, text='Рвых, у.е.:')
label_Potr = tkinter.Label(window, text='Ротр, у.е.:')
label_temperature = tkinter.Label(window, text='Температура, ºC:')
label_supply_voltage = tkinter.Label(window, text='Напряжение\nпитания, В:')

text_Pin = tkinter.Label(window, text='FF', font='arial 9 bold')
text_Pout = tkinter.Label(window, text='FF', font='arial 9 bold')
text_Potr = tkinter.Label(window, text='FF', font='arial 9 bold')
text_temperature = tkinter.Label(window, text='FF')
text_supply_voltage = tkinter.Label(window, text='FF')

# Размещение элементов
button_onOff_umi.place(x=100,y=200)
sbros_avarii_button.place(x=250,y=200)
stop_obmen.place(x=400,y=200)

label_state_umi.place(x=240,y=5)
label_electrical_network.place(x=10,y=30)
label_power_supply.place(x=60,y=30)
label_microwave_path.place(x=110,y=30)
label_Pin_low.place(x=160,y=30)
label_Pin_high.place(x=210,y=30)
label_Pout_low.place(x=260,y=30)
label_Potr_high.place(x=310,y=30)
label_overheat.place(x=360,y=30)
label_overload_TQ.place(x=410,y=30)
label_not_modulation_pulses.place(x=460,y=30)
label_power_failure.place(x=510,y=30)
label_temperature_sensor_broken.place(x=560,y=30)

for i in range(12):
    globals()['state{}'.format(i)].place(x=15+i*50,y=70)

c.place(x=0,y=120)

label_Pin.place(x=20,y=150)
label_Pout.place(x=120,y=150)
label_Potr.place(x=220,y=150)
label_temperature.place(x=320,y=150)
label_supply_voltage.place(x=470,y=135)

text_Pin.place(x=70,y=150)
text_Pout.place(x=180,y=150)
text_Potr.place(x=280,y=150)
text_temperature.place(x=420,y=150)
text_supply_voltage.place(x=540,y=150)

thread_update_window.start()
thread_obmen.start()

window.mainloop()