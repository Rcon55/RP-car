import os
import sys
import curses
import time
import RPi.GPIO as GPIO

# Установим номера пинов GPIO, с которыми будем работать
M1_RIGHT = 4
M1_LEFT = 17
M2_RIGHT = 27
M2_LEFT = 22

# Функция для подготовки пинов GPIO
def setup(*ports):
    GPIO.cleanup()
    # Режим именования пинов по названию, а не по номеру на плате 
    GPIO.setmode(GPIO.BCM)
    for port in ports:
        # Установка пина на вывод + низкий уровень "0"
        GPIO.setup(port, GPIO.OUT)
        GPIO.output(port, GPIO.LOW)

# Функция для установки низкого уровня на всех пинах (выключение)
def stop_all():
    GPIO.output(M1_LEFT, GPIO.LOW)
    GPIO.output(M1_RIGHT, GPIO.LOW)
    GPIO.output(M2_LEFT, GPIO.LOW)
    GPIO.output(M2_RIGHT, GPIO.LOW)

# Функция для управления вращением движков
def rotate(motor=1, mode='s'):
    # Выключаем все пины
    stop_all()
    # Для мотора 1
    if motor == 1:
        if mode == 'r':
            GPIO.output(M1_RIGHT, GPIO.HIGH)
        elif mode == 'l':
            GPIO.output(M1_LEFT, GPIO.HIGH)
    # Для мотора 2
    elif motor == 2:
        if mode == 'r':
            GPIO.output(M2_RIGHT, GPIO.HIGH)
        elif mode == 'l':
            GPIO.output(M2_LEFT, GPIO.HIGH)

# Выполним инициализацию пинов GPIO
setup(M1_RIGHT, M1_LEFT, M2_RIGHT, M2_LEFT)

# Инициализация экрана (модуль curses)
stdscr = curses.initscr()
# Реагировать на нажатие клавиш без подтверждения при помощи ENTER
curses.cbreak()
# Разрешить использование стрелочек на клавиатуре
stdscr.keypad(1)
# Не блокировать программу по времени при опросе событий
stdscr.nodelay(1)

# Отобразим на экране данные по умолчанию
stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.addstr(2, 10, "A - M1 Left, D - M1 Right")
stdscr.addstr(3, 10, "< - M2 Left, > - M2 Right")
stdscr.addstr(4, 10, "S - stop")
stdscr.refresh()


stopped = True

# Главный цикл
while True:
    # Получаем код нажатия клавиши и проверяем его
    key = stdscr.getch()
    if key != -1:
        # Если клавиша "стрелка влево" то вращаем движок 2 влево
        if key == curses.KEY_LEFT:
            rotate(1, 'l')
            rotate(2, 'l')
            stopped = False
        elif key == curses.KEY_RIGHT:
            rotate(1, 'r')
            rotate(2, 'r')
            stopped = False
        elif key == curses.KEY_UP:
            rotate(1, 'l')
            rotate(2, 'l')
            stopped = False
        elif key == curses.KEY_DOWN:
            rotate(1, 'r')
            rotate(2, 'r')
            stopped = False
        elif key == ord('s'):
            stop_all()
            stopped = True
        elif key == ord('q'):
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
            os.system('clear')
            sys.exit()
        stdscr.refresh()
        time.sleep(0.01)
    else:
        if stopped:
            pass
        else:
            stop_all()
            stopped = True
