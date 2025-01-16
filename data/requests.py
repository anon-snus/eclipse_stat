from data.utils import async_get
import asyncio
from data.system_addresses import system_programs
from datetime import datetime
from decimal import Decimal
from fake_useragent import UserAgent

class Request:
	def __init__(self,
		proxy : str | None = None,
		address : str | None = None
	):
		self.proxy = proxy if proxy else None
		self.address = address
		self.headers ={
		    'sec-ch-ua-platform': '"macOS"',
		    'Referer': 'https://eclipsescan.xyz/',
		    'User-Agent': UserAgent().random,
		    'Accept': 'application/json, text/plain, */*',
		    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
		    'sec-ch-ua-mobile': '?0',
		}

	async def eth_balance(self):
		url = 'https://api.eclipsescan.xyz/v1/account'
		for i in range(10):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params = {'address':self.address}, headers=self.headers)
				if bal['success'] == True:
					if len(bal['data']) <3:
						return 0.0
					return int(bal['data']['lamports'])/10**9
			except Exception as e:
				print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error eth_balance: {self.address}')
		return 0.0

	async def domain(self):
		url = 'https://api.eclipsescan.xyz/v1/account/domain'
		for i in range(10):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params = {'address':self.address}, headers=self.headers)
				if bal['success'] == True:
					if bal['data']:
						return bal['data']['favorite']
					return 0.0
			except Exception as e:
				print(f'ошибка  domain {e}')
				await asyncio.sleep(5)
		print(f'error domain: {self.address}')
		return 0.0

	async def tokens(self):
		url = 'https://api.eclipsescan.xyz/v1/account/tokens'
		tokens = {}
		for i in range(10):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params = {'address':self.address}, headers=self.headers)
				if bal['success'] == True:
					if bal['data']:
						for i in bal['data']['tokens']:
							tokens[i['tokenName']] = i['balance']
						return tokens
					return {}
			except Exception as e:
				print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error tokens: {self.address}')
		return {}

	async def tx_count(self):
		url = 'https://api.eclipsescan.xyz/v1/account/transfer'
		for i in range(10):
			try:
				page = 1
				bal = await async_get(url=url, proxy=self.proxy,
				                      params={
					                      'address': self.address,
					                      'page': page,
					                      'page_size': '100',
					                      'remove_spam': 'false',
					                      'exclude_amount_zero': 'false',
				                      },
				                      headers=self.headers
				                      )
				# print(bal)
				if bal['success']:
					transactions = set()
					unique_days = set()
					unique_months = set()

					# programms = set()
					# volume = 0
					# fee = 0
					while len(bal['data']) == 100:
						for txn in bal['data']:
							transactions.add(txn['trans_id'])
							dt_object = datetime.fromtimestamp(txn['block_time'])
							# print(dt_object)
							# Добавляем месяц и год для уникальности месяца
							unique_months.add((dt_object.year, dt_object.month))
							# Добавляем полный день для уникальности дня
							unique_days.add((dt_object.year, dt_object.month, dt_object.day))
							# volume += int(txn['sol_value'])
							# fee += int(txn['fee'])
							# for program_id in txn['programIds']:
							# 	if program_id not in system_programs:
							# 		programms.add(program_id)
						page += 1
						bal = await async_get(url=url, proxy=self.proxy, params={
							'address': self.address, 'page': page, 'page_size': '100', 'remove_spam': 'false',
							'exclude_amount_zero': 'false',
						}, headers=self.headers)
						await asyncio.sleep(1)
					for txn in bal['data']:
						transactions.add(txn['trans_id'])
						# print(transactions)
						dt_object = datetime.fromtimestamp(txn['block_time'])
						# print(dt_object)
						# Добавляем месяц и год для уникальности месяца
						unique_months.add((dt_object.year, dt_object.month))
						# Добавляем полный день для уникальности дня
						unique_days.add((dt_object.year, dt_object.month, dt_object.day))
						# volume += int(txn['sol_value'])
						# fee += int(txn['fee'])
						# for program_id in txn['programIds']:
							# if program_id not in system_programs:
							# 	programms.add(program_id)
					return {'tx_count': len(transactions), 'unique_days': len(unique_days),
					        'unique_months': len(unique_months), 'transactions': transactions}
			except Exception as e:
				print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error tx_count: {self.address}')
		return {'tx_count': 0, 'unique_days': 0, 'unique_months': 0}

	async def get_tx_info(self, tx_id:str):
		url = 'https://api.eclipsescan.xyz/v1/transaction/detail'
		programs = set()
		turbo_tap_id = 'turboe9kMc3mSR8BosPkVzoHUfn5RVNzZhkrT2hdGxN'
		turbo_address = None
		for i in range(10):
			try:
				transaction_info = await async_get(url=url, proxy=self.proxy, params={'tx':tx_id}, headers=self.headers)
				# print(transaction_info)
				if transaction_info['success'] == True:
					transaction_info = transaction_info['data']
					fee = transaction_info['fee']
					for pr in transaction_info['programs_involved']:

						if pr not in system_programs:
							programs.add(pr)
							if pr == turbo_tap_id and len(transaction_info['programs_involved']) == 2:
								turbo_address = transaction_info['sol_bal_change'][1]['address']

					for n in transaction_info['sol_bal_change']:
						if n['address']==self.address:
							sol_bal_change = abs(n['change_amount'])
					# print({'fee':fee, 'programs':programs, 'sol_bal_change':sol_bal_change, 'turbo_address':turbo_address})


					return {'fee':fee, 'programs':programs, 'sol_bal_change':sol_bal_change, 'turbo_address':turbo_address}
			except Exception as e:
				print('tx_info',e)
				await asyncio.sleep(0.1)

		print(f'error get_tx_info: {tx_id}')
		return {{'fee':0, 'programs':[]}}

	async def count_turbo_taps(self, address:str):
		url = 'https://api.eclipsescan.xyz/v1/account/balance_change/total'
		for i in range(10):
			try:
				count = await async_get(url=url, proxy=self.proxy, params={'address': address}, headers=self.headers)
				# print(count)
				if count['success'] == True:
					count = count['data']
					return count
			except Exception as e:

				print(e)
				await asyncio.sleep(0.1)
		print(f'error count_turbo_taps: {self.address}')
		return 0


	async def all_tx_info(self, transactions:set|list|None=None):
		fee = 0
		count = 0
		programs = set()
		sol_bal_change = 0
		turbo_address = None
		if transactions is None:
			await self.tx_count()['transactions']
		for tx in transactions:
			info = await self.get_tx_info(tx)

			fee += info['fee']
			sol_bal_change += info['sol_bal_change']
			programs = programs.union(info['programs'])

			if info['turbo_address']:
				turbo_address = info['turbo_address']
			if turbo_address:
				count = await self.count_turbo_taps(address=turbo_address)
			await asyncio.sleep(0.01)
		# print(f'total fee: {Decimal(fee)/10**9}, turbo {turbo_tap}, count {len(programs)}')
		return {'volume_eth':Decimal(sol_bal_change)/10**9,'fee': Decimal(fee)/10**9, 'programs': len(programs), 'turbo_taps': count}


	async def wallet_info(self, full_inf:bool=False):
		bal = await self.eth_balance()
		domain = await self.domain()
		tokens = await self.tokens()
		tx_count = await self.tx_count()
		if full_inf:

			tx_info = await self.all_tx_info(transactions=tx_count['transactions'])
			return {
				'address': self.address, 'domain': domain, 'bal': bal, 'tx_count': tx_count['tx_count'], 'volume_eth': tx_info['volume_eth'],
				'unique_dapps': tx_info['programs'], 'turbo_taps': tx_info['turbo_taps'],
				'unique_months': tx_count['unique_months'], 'unique_days': tx_count['unique_days'], 'total_fee': tx_info['fee'], 'tokens': tokens
			}
		return {'address':self.address,'bal':bal, 'domain':domain, 'tx_count':tx_count['tx_count'],'unique_months':tx_count['unique_months'], 'unique_days':tx_count['unique_days'], 'tokens':tokens}
