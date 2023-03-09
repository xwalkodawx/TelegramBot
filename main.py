import telebot

from configs import bot_token, values
from extensions import Converter, APIException

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def bot_welcome(message: telebot.types.Message):
	text = 'привет\nДля получение списка всех команд, введи команду /commands'
	bot.send_message(message.chat.id, f'{message.from_user.first_name}, {text}')


@bot.message_handler(commands=['commands'])
def bot_commands(message: telebot.types.Message):
	text = 'Список всех доступных команд:\n/help - справка по использованию' \
		   '\n/values - информация о всех доступных валютах'
	bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def bot_help(message: telebot.types.Message):
	text = 'Для конвертирования валюты введи:\n<имя первой валюты> <имя второй валюты> <количество первой валюты>\n' \
		   'Пример: Доллар рубли 1000'
	bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def bot_values(message: telebot.types.Message):
	text = 'Доступные валюты\n'
	for key in values.keys():
		text = '\n'.join((text, key,))
	bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
	try:

		count = message.text.lower().split(' ')

		if len(count) != 3:
			raise APIException('Неверное количество параметров')

		base, quote, amount = count
		result = Converter.get_price(quote, base, amount)
	except APIException as e:
		bot.reply_to(message, f'Ошибка пользователя\n{e}')

	except Exception as e:
		bot.reply_to(message, f'Не удалось обработать команду\n{e}')

	else:
		text = f'Цена {amount} {base} в {quote} - {result}'
		bot.send_message(message.chat.id, text)


bot.infinity_polling()
