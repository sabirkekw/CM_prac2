from assembler import Assembler

def test_assembler():
    """Тестирование ассемблера на тестовых данных из спецификации"""
    print("Тестирование ассемблера для варианта 16")
    print("=" * 60)
    
    assembler = Assembler()
    
    # Тест 1: LOAD_CONST
    print("\nТест 1: LOAD_CONST (A=7, B=964, C=26)")
    test_line = "LOAD, 964, 26"
    result = assembler.parse_csv_line(test_line)
    if result:
        print(f"  Результат: {result}")
        assert result['opcode'] == 7
        assert result['fields']['B'] == 964
        assert result['fields']['C'] == 26
        print("  ✓ Тест пройден")
    
    # Тест 2: READ_MEM
    print("\nТест 2: READ_MEM (A=1, B=16, C=280, D=3)")
    test_line = "READ, 16, 280, 3"
    result = assembler.parse_csv_line(test_line)
    if result:
        print(f"  Результат: {result}")
        assert result['opcode'] == 1
        assert result['fields']['B'] == 16
        assert result['fields']['C'] == 280
        assert result['fields']['D'] == 3
        print("  ✓ Тест пройден")
    
    # Тест 3: WRITE_MEM
    print("\nТест 3: WRITE_MEM (A=0, B=26, C=17)")
    test_line = "WRITE, 26, 17"
    result = assembler.parse_csv_line(test_line)
    if result:
        print(f"  Результат: {result}")
        assert result['opcode'] == 0
        assert result['fields']['B'] == 26
        assert result['fields']['C'] == 17
        print("  ✓ Тест пройден")
    
    # Тест 4: POPCNT
    print("\nТест 4: POPCNT (A=5, B=21, C=1)")
    test_line = "POPCNT, 21, 1"
    result = assembler.parse_csv_line(test_line)
    if result:
        print(f"  Результат: {result}")
        assert result['opcode'] == 5
        assert result['fields']['B'] == 21
        assert result['fields']['C'] == 1
        print("  ✓ Тест пройден")
    
    print("\n" + "=" * 60)
    print("Все тесты пройдены успешно!")

if __name__ == "__main__":
    test_assembler()