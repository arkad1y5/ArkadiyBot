import telebot  #підключаю бібліотеку
from telebot import types

name = "" #початкові значення зміних
age = 0 #початкові значення змінних


bot = telebot.TeleBot("1675284822:AAG8IsYm4rkiCYusZJ1tLNHLjxPyeuJzfo4") #підєднуєм токен бота

@bot.message_handler(commands=['start'])  #бот відповідає на команди
def send_welcome(message):
	bot.reply_to(message, "Welcome to ArkadiyBot!!")

@bot.message_handler(commands=['help'])  #бот відповідає на команди
def send_welcome(message):
	bot.reply_to(message, "Comand ArkadiyBot \n\n /reg - регистрация пользователя" )

@bot.message_handler(func=lambda message: True)    #ехо
def echo_all(message):
	if message.text == 'Привет': # як смс == привіт то виводиться слід
		bot.reply_to(message, 'Привет создатель')
	elif message.text == 'Как дела?':
		bot.reply_to(message, 'Бывало и по круче')
	elif message.text == '/reg':
		bot.send_message(message.from_user.id, "Давай знакомиться! \nКак тебя зовут?")
		bot.register_next_step_handler(message, reg_name) #перекидаєм на функцію яка зберігає дані

def reg_name(message): #функція яка зберігає імя корестувача
	global name
	name = message.text
	bot.send_message(message.from_user.id, "Сколька лет?")
	bot.register_next_step_handler(message, reg_age)

def reg_age(message): #функція яка зберігає год корестувача
	global age
	#age = message.text
	while age == 0:			#перевірка на то чи користовач ввів число а не текст
		try:
			age = int(message.text)
		except Exception:
			bot.send_message(message.from_user.id, "Ввадите цыфрами!!!")

	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text = 'Да', callback_data = 'yes')
	keyboard.add(key_yes)
	key_no = types.InlineKeyboardButton(text='Не', callback_data='no')
	keyboard.add(key_no)
	question = "Тебя зовут " + name + ". Тебе " + str(age) + " лет. Верно?"
	bot.send_message(message.from_user.id, text = question, reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)		#кнопки до знайомства
def callback_data(call):
	if call.data == 'yes':  #кнопка да
		bot.send_message(call.message.chat.id, "Приятно познакомится! Тепер запишу ето в базу даних")
	elif call.data == 'no':		#кнопка не
		bot.send_message(call.message.chat.id, "Попробуем еще")
		bot.send_message(call.message.chat.id, "Давай знакомиться! \nКак тебя зовут?")
		bot.register_next_step_handler(call.message, reg_name)


bot.polling() #щоб бот не завершував роботу

