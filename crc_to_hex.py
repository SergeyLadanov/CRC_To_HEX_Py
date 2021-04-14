#! python

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

# Старшая 
high_start_adr = ''
low_start_part = ''

high_end_adr = ''
low_end_part = ''

f = open('ATKUE.hex', 'r')
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
start_adr = '0x' + high_start_adr + low_start_part
# Компоновка конечного адреса
end_adr = '0x' + high_end_adr + low_end_part

# Вывод результатов
print(start_adr)
print(end_adr)