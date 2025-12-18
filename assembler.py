import csv
import sys
import struct
from pathlib import Path
from vm_spec import COMMANDS, COMMAND_BY_MNEMONIC, get_command_by_opcode

class Assembler:
    def __init__(self):
        self.intermediate_rep = []  # Промежуточное представление
        
    def parse_csv_line(self, line):
        """Разбор строки CSV в промежуточное представление"""
        if not line or line.startswith('#'):
            return None
            
        parts = line.strip().split(',')
        if len(parts) < 2:
            return None
            
        mnemonic = parts[0].strip().upper()
        if mnemonic not in COMMAND_BY_MNEMONIC:
            raise ValueError(f"Неизвестная мнемоника: {mnemonic}")
            
        cmd_name = COMMAND_BY_MNEMONIC[mnemonic]
        cmd_info = COMMANDS[cmd_name]
        
        # Преобразуем аргументы в числа
        args = []
        for i in range(1, len(parts)):
            arg = parts[i].strip()
            if arg.startswith('0x'):
                args.append(int(arg[2:], 16))
            else:
                args.append(int(arg))
                
        # Создаем запись промежуточного представления
        intermediate = {
            'cmd_name': cmd_name,
            'opcode': cmd_info['opcode'],
            'fields': {}
        }
        
        # Заполняем поля
        if cmd_name == 'LOAD_CONST':
            intermediate['fields']['B'] = args[0]  # Константа
            intermediate['fields']['C'] = args[1]  # Адрес регистра
        elif cmd_name == 'READ_MEM':
            intermediate['fields']['B'] = args[0]  # Адрес регистра
            intermediate['fields']['C'] = args[1]  # Смещение
            intermediate['fields']['D'] = args[2]  # Адрес регистра результата
        elif cmd_name == 'WRITE_MEM':
            intermediate['fields']['B'] = args[0]  # Адрес регистра источника
            intermediate['fields']['C'] = args[1]  # Адрес регистра назначения
        elif cmd_name == 'POPCNT':
            intermediate['fields']['B'] = args[0]  # Адрес регистра источника
            intermediate['fields']['C'] = args[1]  # Адрес регистра результата
            
        return intermediate
    
    def assemble_from_csv(self, input_file, test_mode=False):
        """Ассемблирование из CSV файла"""
        self.intermediate_rep = []
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            intermediate = self.parse_csv_line(line)
            if intermediate:
                self.intermediate_rep.append(intermediate)
                
        if test_mode:
            self.print_intermediate_representation()
            
        return self.intermediate_rep
    
    def print_intermediate_representation(self):
        """Вывод промежуточного представления на экран"""
        print("Промежуточное представление программы:")
        print("=" * 60)
        
        for i, instr in enumerate(self.intermediate_rep):
            print(f"Инструкция {i}:")
            print(f"  Команда: {instr['cmd_name']}")
            print(f"  Код операции (A): {instr['opcode']}")
            
            for field_name, value in instr['fields'].items():
                print(f"  Поле {field_name}: {value} (0x{value:X})")
            
            # Вывод в формате тестов из спецификации
            fields_str = ", ".join([f"{field_name}={value}" 
                                   for field_name, value in instr['fields'].items()])
            print(f"  Формат: A={instr['opcode']}, {fields_str}")
            print()
    
    def save_to_file(self, output_file):
        """Сохранение промежуточного представления в файл (для отладки)"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for instr in self.intermediate_rep:
                f.write(f"{instr['cmd_name']}: A={instr['opcode']}")
                for field_name, value in instr['fields'].items():
                    f.write(f", {field_name}={value}")
                f.write("\n")

def main():
    """Основная функция ассемблера"""
    if len(sys.argv) < 4:
        print("Использование: python assembler.py <input.csv> <output.bin> <test_mode>")
        print("  test_mode: 0 - обычный режим, 1 - режим тестирования")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = sys.argv[3] == '1'
    
    assembler = Assembler()
    
    try:
        # 1. Парсинг CSV и создание промежуточного представления
        intermediate = assembler.assemble_from_csv(input_file, test_mode)
        
        if test_mode:
            print(f"\nУспешно ассемблировано {len(intermediate)} инструкций")
        
        # 2. Сохранение промежуточного представления для отладки
        debug_file = Path(input_file).stem + "_intermediate.txt"
        assembler.save_to_file(debug_file)
        
        print(f"\nРезультат сохранен в {debug_file}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()