import os
import csv
from datetime import datetime

class BaseModel:
    """Базовый класс с базовой функциональностью"""
    def __repr__(self):
        return f"<{self.__class__.__name__} {vars(self)}>"

class BankVisit(BaseModel):
    """Класс для представления посещения банка"""
    def __init__(self, vid, full_name, date, visit_type):
        self.vid = vid
        self.full_name = full_name
        self.date = date
        self.visit_type = visit_type

    def __setattr__(self, name, value):
        """Валидация данных при установке свойств"""
        if name == 'vid':
            value = int(value)
        elif name == 'date':
            if isinstance(value, str):
                value = self._parse_date(value)
        super().__setattr__(name, value)

    @staticmethod
    def _parse_date(date_str):
        """Парсинг даты из строки"""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ")

class VisitCollection:
    """Коллекция для работы с посещениями"""
    def __init__(self):
        self._visits = []
        self._current = 0

    def __getitem__(self, index):
        return self._visits[index]

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < len(self._visits):
            result = self._visits[self._current]
            self._current += 1
            return result
        self._current = 0
        raise StopIteration

    def add(self, visit):
        """Добавление нового посещения"""
        if not isinstance(visit, BankVisit):
            raise TypeError("Только объекты BankVisit могут быть добавлены")
        self._visits.append(visit)

    @classmethod
    def from_csv(cls, filename):
        """Загрузка данных из CSV файла"""
        collection = cls()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        visit = BankVisit(
                            vid=row['№'],
                            full_name=row['ФИО'],
                            date=row['Дата и время'],
                            visit_type=row['Тип обращения']
                        )
                        collection.add(visit)
                    except (ValueError, KeyError) as e:
                        print(f"Ошибка в строке: {row} | {e}")
        except FileNotFoundError:
            print("Файл не найден. Будет создан новый при сохранении.")
        return collection

    def save_csv(self, filename):
        """Сохранение данных в CSV файл"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['№', 'ФИО', 'Дата и время', 'Тип обращения'])
            for visit in self._visits:
                writer.writerow([
                    visit.vid,
                    visit.full_name,
                    visit.date.strftime('%Y-%m-%d %H:%M'),
                    visit.visit_type
                ])

    def print_table(self):
        """Вывод данных в виде таблицы"""
        # Форматирование заголовков
        header = (
            f"{'№':<5} "
            f"{'ФИО':<25} "
            f"{'Дата и время':<20} "
            f"{'Тип обращения':<20}"
        )
        
        # Разделитель
        separator = "-" * 75
        
        # Вывод шапки
        print(f"\n{separator}")
        print(header)
        print(separator)

        # Вывод данных
        for visit in self._visits:
            full_name = visit.full_name[:22] + "..." if len(visit.full_name) > 25 else visit.full_name
            visit_type = visit.visit_type[:17] + "..." if len(visit.visit_type) > 20 else visit.visit_type
            
            row = (
                f"{visit.vid:<5} "
                f"{full_name:<25} "
                f"{visit.date.strftime('%Y-%m-%d %H:%M'):<20} "
                f"{visit_type:<20}"
            )
            print(row)
        
        print(separator)

def main_menu():
    """Интерактивное меню управления"""
    collection = VisitCollection.from_csv('data.csv')
    
    while True:
        print("\nМеню:")
        print("1. Показать все записи")
        print("2. Добавить новую запись")
        print("3. Сохранить изменения")
        print("4. Выйти")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            collection.print_table()
        
        elif choice == '2':
            try:
                vid = int(input("Номер записи: "))
                full_name = input("ФИО клиента: ").strip()
                date = input("Дата и время (ГГГГ-ММ-ДД ЧЧ:ММ): ").strip()
                visit_type = input("Тип обращения: ").strip()
                
                visit = BankVisit(vid, full_name, date, visit_type)
                collection.add(visit)
                print("\nЗапись успешно добавлена!")
            
            except ValueError as e:
                print(f"\nОшибка: {e}")
        
        elif choice == '3':
            collection.save_csv('data.csv')
            print("\nДанные успешно сохранены!")
        
        elif choice == '4':
            if input("\nСохранить изменения перед выходом? (да/нет): ").lower() == 'да':
                collection.save_csv('data.csv')
            print("Выход из программы.")
            break
        
        else:
            print("\nНеверный ввод. Попробуйте снова.")

if __name__ == '__main__':
    main_menu() # Комментарий для git commit
