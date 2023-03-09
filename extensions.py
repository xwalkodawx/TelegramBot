import requests
import json

from configs import values, headers


class APIException(Exception):
	pass


class Converter:
	@staticmethod
	def get_price(quote: str, base: str, amount: str):

		if base == quote:
			raise APIException(f'Нельзя конвертировать одинаковые валюты {base}')

		try:
			amount = float(amount)
		except ValueError:
			raise APIException(f'Неверное количество "{amount}"')

		try:
			url_pars = (
				f'https://api.apilayer.com/currency_data/convert?to={values[quote]}&from={values[base]}&amount={amount}')
		except Exception:
			raise APIException('Неверный ввод')

		payload = {}
		response = requests.get(url_pars, headers=headers, data=payload)

		result = json.loads(response.content)['result']

		return result
