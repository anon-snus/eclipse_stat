import asyncio
import csv
from data.requests import Request
from data.utils import check_ip, open_proxies


async def fetch_data(addresses, proxies, full_info: bool = False):
    """Асинхронно получает информацию о кошельках."""
    data = []
    for i, address in enumerate(addresses):
        try:
            # Проверяем прокси
            proxy = proxies[i] if proxies and await check_ip(proxy=proxies[i]) else None

            # Если прокси не работает и она обязательна, пропускаем адрес
            if proxies and proxy is None:
                print(f"Skipping address {address}: Invalid proxy.")
                data.append({'address': address, 'domain':proxies[i], 'balance_eth':proxies[i], 'tx_count':proxies[i],
                'volume_eth':proxies[i], 'unique_dapps':proxies[i],'turbo_taps':proxies[i], 'unique_days':proxies[i],
                             'unique_months':proxies[i], 'total_fee':proxies[i]
                            })
                continue

            # Создаём запрос
            req = Request(address=address, proxy=proxy)
            # req = Request(address=address)
            inf = await req.wallet_info(full_inf=full_info)
            print(inf)
            data.append(inf)

        except Exception as e:
            print(f"Error processing address {address}: {e}")
            continue
        print()
        if full_info:
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(0.1)

    return data


def write_to_csv(data, output_file='output.csv', full_info:bool=False):
    """Записывает данные в CSV файл."""
    tokens = list(set().union(*(entry['tokens'].keys() for entry in data)))
    if full_info:
        headers = ['address', 'domain',  'balance_eth', 'tx_count', 'volume_eth', 'unique_dapps','turbo_taps', 'unique_days', 'unique_months', 'total_fee'] + tokens
    else:
        headers = ['address', 'balance_eth', 'domain', 'tx_count', 'unique_days', 'unique_months'] + tokens

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        for entry in data:
            if full_info:
                row = [
                    entry['address'],  entry['domain'],entry['bal'],
                    entry['tx_count'], entry['volume_eth'], entry['unique_dapps'], entry['turbo_taps'],
                    entry['unique_days'], entry['unique_months'], entry['total_fee']
                ]
            else:
                row = [entry['address'], entry['domain'],  entry['bal'],entry['tx_count'], entry['unique_days'],
                    entry['unique_months'], ]
            row.extend(entry['tokens'].get(token, 0) for token in tokens)
            csvwriter.writerow(row)
        print('Info is saved to output.csv')


async def main():
    with open('addresses.txt') as f:
        addresses = f.read().splitlines()

    proxies = open_proxies(path='proxies.txt', addresses_count=len(addresses))
    print(f'Do you want to get full wallet info? the difference is in unique dapps count, volume_eth, fee counter, turbo tap. It is better to use proxies with full info. \nChoose option:\n1 - full info\n2 - small info (faster)\n3 - exit')
    user_input = int(input())
    if user_input == 1:
        print(f'Searching for full wallet info 🔍, it may take some time... (it is better to use proxies now)')
        data = await fetch_data(addresses, proxies, full_info=True)
        write_to_csv(data, full_info=True)
    elif user_input == 2:
        print(f'Searching for small wallet info 🔍, it may take some time... ')
        data = await fetch_data(addresses, proxies, full_info=False)
        write_to_csv(data, full_info=False)
    else:
        print(f'Exiting...')
        exit()



if __name__ == "__main__":
    asyncio.run(main())
    
