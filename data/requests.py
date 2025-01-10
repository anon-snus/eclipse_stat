from data.utils import async_get
import asyncio
from data.system_addresses import system_programs
from datetime import datetime
from decimal import Decimal


class Request:
	def __init__(self,
		proxy : str | None = None,
		address : str | None = None
	):
		self.proxy = proxy if proxy else None
		self.address = address

	async def eth_balance(self):
		url = 'https://api.eclipsescan.xyz/v1/account'
		for i in range(5):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params = {'address':self.address})
				if bal['success'] == True:
					if len(bal['data']) <3:
						return 0.0
					return int(bal['data']['lamports'])/10**9
			except Exception as e:
				# print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error eth_balance: {self.address}')
		return 0.0

	async def domain(self):
		url = 'https://api.eclipsescan.xyz/v1/account/domain'
		for i in range(5):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params = {'address':self.address})
				if bal['success'] == True:
					if bal['data']:
						return bal['data']['favorite']
					return 0.0
			except Exception as e:
				# print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error domain: {self.address}')
		return 0.0

	async def tokens(self):
		url = 'https://api.eclipsescan.xyz/v1/account/tokens'
		tokens = {}
		for i in range(5):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params = {'address':self.address})
				if bal['success'] == True:
					if bal['data']:
						for i in bal['data']['tokens']:
							tokens[i['tokenName']] = i['balance']
						return tokens
					return {}
			except Exception as e:
				# print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error tokens: {self.address}')
		return {}

	async def tx_count(self):
		url = 'https://api.eclipsescan.xyz/v1/account/transfer'
		for i in range(5):
			try:
				page = 1
				bal = await async_get(url=url, proxy=self.proxy,
				                      params={
					                      'address': self.address,
					                      'page': page,
					                      'page_size': '100',
					                      'remove_spam': 'false',
					                      'exclude_amount_zero': 'false',
				                      }
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
						})
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
					        'unique_months': len(unique_months)}
			except Exception as e:
				print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error tx_count: {self.address}')
		return {'tx_count': 0, 'unique_days': 0, 'unique_months': 0}


	async def wallet_info(self):
		bal = await self.eth_balance()
		domain = await self.domain()
		tokens = await self.tokens()
		tx_count = await self.tx_count()
		return {'address':self.address,'bal':bal, 'domain':domain, 'tx_count':tx_count['tx_count'],'unique_months':tx_count['unique_months'], 'unique_days':tx_count['unique_days'], 'tokens':tokens}
