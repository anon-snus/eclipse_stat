from data.requests import Request
import asyncio
import csv


async def main():
	with open('addresses.txt') as f:
		addresses = f.read().splitlines()
	data = []
	print(f'Subscribe to https://t.me/degen_statistics 🤫')
	for i in addresses:
		req = Request(address=i)
		inf = await req.wallet_info()
		print(inf)
		data.append(inf)
		await asyncio.sleep(5)
	tokens = []
	for i in data:
		tokens.append(i['tokens'].keys())
	tokens = list(set().union(*tokens))
	with open('output.csv', 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		headers = ['address', 'balance_eth', 'domain', 'tx_count', 'dapps_count', 'unique_days', 'unique_months'] + tokens
		csvwriter.writerow(headers)
		for entry in data:
			row = [entry['address'], entry['bal'], entry['domain'], entry['tx_count'], entry['dapps_count'], entry['unique_days'], entry['unique_months']]
			for token in tokens:
				row.append(entry['tokens'].get(token, 0))
			csvwriter.writerow(row)

if __name__ == "__main__":
	asyncio.run(main())
