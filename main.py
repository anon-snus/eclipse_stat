import asyncio
import csv
from data.requests import Request
from data.utils import check_ip, open_proxies
import sys

async def fetch_data(addresses, proxies):
    """Асинхронно получает информацию о кошельках."""
    data = []
    for i, address in enumerate(addresses):
        try:
            # Проверяем прокси
            proxy = proxies[i] if proxies and await check_ip(proxy=proxies[i]) else None

            # Если прокси не работает и она обязательна, пропускаем адрес
            if proxies and proxy is None:
                print(f"Skipping address {address}: Invalid proxy.")
                data.append({'address': address, 'bal':f'invalid Proxy {proxies[i]}','domain':f'invalid Proxy {proxies[i]}',
                             'tokens':{}, 'tx_count':f'invalid Proxy {proxies[i]}', 
                             'unique_months':f'invalid Proxy {proxies[i]}', 'unique_days':f'invalid Proxy {proxies[i]}',
                            })
                continue

            # Создаём запрос
            # req = Request(address=address, proxy=proxy)
            req = Request(address=address)
            inf = await req.wallet_info()
            print(inf)
            data.append(inf)

        except Exception as e:
            # Логируем ошибки и пропускаем адрес
            print(f"Error processing address {address}: {e}")
            continue

        # Пауза между запросами
        await asyncio.sleep(5)

    return data


def write_to_csv(data, output_file='output.csv'):
    """Записывает данные в CSV файл."""
    tokens = list(set().union(*(entry['tokens'].keys() for entry in data)))
    headers = ['address', 'balance_eth', 'domain', 'tx_count', 'unique_days', 'unique_months'] + tokens

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        for entry in data:
            row = [
                entry['address'], entry['bal'], entry['domain'], 
                entry['tx_count'],
                entry['unique_days'], entry['unique_months'],
            ]
            row.extend(entry['tokens'].get(token, 0) for token in tokens)
            csvwriter.writerow(row)
        print('Info is saved to output.csv')


async def main():
    with open('addresses.txt') as f:
        addresses = f.read().splitlines()

    proxies = open_proxies(path='proxies.txt', addresses_count=len(addresses))
    data = await fetch_data(addresses, proxies)
    write_to_csv(data)


if __name__ == "__main__":
    asyncio.run(main())
    
