#! python
import os
import sys

# Класс строки Hex файла
class HexLine(object):
    EXTENSION_ADDR = '04'
    SEGMENT_ADDR = '02'
    DATA = '00'
    def __init__(self, line):
        self.Num = line[1:3]
        self.Adr = line[3:7]
        self.Type = line[7:9]
        self.Data = line[9:(9 + int(self.Num) * 2)]
        

# Проверка формата строки Hex файла
def CheckLine(input):
    return input.startswith(':')

# Старшая часть начального адреса прошивки
high_start_adr = ''
# Младшая часть начального адреса прошивки
low_start_part = ''

# Старшая часть конечного адреса прошивки
high_end_adr = ''
# Младшая часть конечного адреса прошивки
low_end_part = ''

# Получение имени файла
filename = sys.argv[1]

f = open(filename, 'r')
for line in f:
    if (not CheckLine(line)):
        print("Hex файл имеет неверный формат")
        break
    hexline = HexLine(line)
    # Обработка записи расширенного адреса
    if (hexline.Type == HexLine.EXTENSION_ADDR):
        if (high_start_adr == ''):
            high_start_adr = hexline.Data
        high_end_adr = hexline.Data
    # Обработка записи двоичных данных
    if (hexline.Type == HexLine.DATA):
        if (low_start_part == ''):
            low_start_part = hexline.Adr
        low_end_part = hexline.Adr

f.close()
# Компоновка начального адреса
start_adr = int(high_start_adr + low_start_part, 16)
# Компоновка конечного адреса
end_adr = int(high_end_adr + low_end_part, 16)

start_adr = hex(start_adr)
end_adr = end_adr + 4
end_adr = hex(end_adr)

# Вставка контрольной суммы в конец hex файла
cmd = f"..\\srec_cat.exe {filename} -Intel -fill 0xFF {start_adr} {end_adr} -crc16-big-endian {end_adr} -o {filename} -Intel"
os.system(cmd)

# Получение bin файла
binfilename = filename[:-3] + "bin"
cmd = f"arm-none-eabi-objcopy --input-target=ihex --output-target=binary {filename} {binfilename}"
os.system(cmd)