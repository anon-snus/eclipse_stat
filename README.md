# Чекер статистики Eclipse 

## Subscribe to https://t.me/degen_statistics 🤫

## Описание
Этот проект проверяет статистику для заданных публичных адресов. Для каждого адреса анализируются следующие параметры:
- Наличие домена Turbo
- Баланс в нативной монете
- Количество транзакций
- Количество уникальных приложений
- Количество уникальных месяцев и дней
- Объем в эфире и уплаченную комиссию в эфире
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
   
2. По желанию создайте или заполните файл `proxies.txt`, указав в нем прокси формата логин:пароль@айпи:порт, каждый с новой строки. Пример:
   ```
   log:pass@ip:port
   log:pass@ip:port
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


# Statistics Checker Eclipse

## Subscribe to https://t.me/degen_statistics 🤫

## Description
This project checks statistics for specified public addresses. For each address, the following parameters are analyzed:
- Presence of a Turbo domain
- Balance in the native currency
- Number of transactions
- Number of unique applications
- Number of tokens
- Number of unique months and days
- Ethereum volume and eth fees

The results are saved to the `output.csv` file in the same directory.

## Installation
1. Ensure that Python (version 3.7 or higher) is installed on your system.
2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Create or fill in the `addresses.txt` file with public addresses, each on a new line. Example:
   ```
   7jtuen1N95bBNyAV5dbcx6enYT24qKqHobyHQZnyRoTD
   8t2XBEjM7db1Fv24FhNaayPx32daDZ95L5xTETKCk2pK
   ```
2. Optionally, create or fill in the file `proxies.txt`, specifying in it proxies of the format login:password@ip:port, each on a new line. Example:
   ```
   log:pass@ip:port
   log:pass@ip:port
   ```


## Usage
1. Run the script using the command:
   ```bash
   python main.py
   ```

## Results
- After the script finishes execution, all results will be saved in the `output.csv` file in CSV format.

## Notes
- Ensure that your public addresses are correct to avoid errors during execution.
- If errors occur, check the `addresses.txt` file and the installed dependencies for correctness.


