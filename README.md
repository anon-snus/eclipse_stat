# Чекер статистики Eclipse 

## Описание
Этот проект проверяет статистику для заданных публичных адресов. Для каждого адреса анализируются следующие параметры:
- Наличие домена Turbo
- Баланс в нативной монете
- Количество транзакций
- Количество уникальных приложений
- Количество токенов

Результаты сохраняются в файл `output.csv` в той же директории.

## Установка
1. Убедитесь, что у вас установлен Python (версия 3.7 или выше).
2. Установите необходимые зависимости, выполнив команду:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка
1. Создайте или заполните файл `addresses.txt`, указав в нем публичные адреса, каждый с новой строки. Пример:
   ```
   7jtuen1N95bBNyAV5dbcx6enYT24qKqHobyHQZnyRoTD
   8t2XBEjM7db1Fv24FhNaayPx32daDZ95L5xTETKCk2pK
   ```

## Запуск
1. Запустите скрипт с помощью команды:
   ```bash
   python main.py
   ```

## Результаты
- После выполнения скрипта, все результаты будут сохранены в файл `output.csv` в формате CSV.

## Замечания
- Убедитесь, что ваши публичные адреса корректны, чтобы избежать ошибок в процессе выполнения.
- В случае возникновения ошибок проверьте правильность заполнения `addresses.txt` и установленных зависимостей.

