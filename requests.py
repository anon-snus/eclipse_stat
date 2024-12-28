from utils import async_get
import asyncio
from data.system_addresses import system_programs

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
		url = 'https://api.eclipsescan.xyz/v1/account/transaction'
		for i in range(5):
			try:
				bal = await async_get(url=url, proxy=self.proxy, params={'address': self.address, 'page_size': '40'})
				if bal['success']:
					programms = set()
					tx_count = 0
					while len(bal['data']['transactions']) == 40:
						tx_count += len(bal['data']['transactions'])
						for txn in bal['data']['transactions']:
							for program_id in txn['programIds']:
								if program_id not in system_programs:
									programms.add(program_id)
						params = {
							'address': self.address, 'page_size': '40',
							'before': bal['data']['transactions'][-1]['txHash'],
						}
						bal = await async_get(url=url, proxy=self.proxy, params=params)
						await asyncio.sleep(1)
					tx_count += len(bal['data']['transactions'])
					for txn in bal['data']['transactions']:
						for program_id in txn['programIds']:
							if program_id not in system_programs:
								programms.add(program_id)
					return {'programms': len(programms), 'tx_count': tx_count}
			except Exception as e:
				# print(f'ошибка {e}')
				await asyncio.sleep(5)
		print(f'error tx_count: {self.address}')
		return {'programms': 0, 'tx_count': 0}


	async def wallet_info(self):
		bal = await self.eth_balance()
		domain = await self.domain()
		tokens = await self.tokens()
		tx_count = await self.tx_count()
		return {'address':self.address,'bal':bal, 'domain':domain, 'tokens':tokens, 'tx_count':tx_count['tx_count'], 'dapps_count':tx_count['programms']}
