
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import config
import utils
from constants import cons
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True)
	keyboard.row(telebot.types.KeyboardButton(cons['ru']['language']))
	keyboard.row(telebot.types.KeyboardButton(cons['eng']['language']))
	bot.send_message(chat_id=message.chat.id, text =cons['select_your_language'] , reply_markup= keyboard)
#rus part
@bot.message_handler(func = lambda message: message.text==cons['ru']['language'])	
def goal_of_request_ru(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True)
	for i in utils.get_question(cons['ru']['goal of request'])['answers']:
		keyboard.row(i)
	bot.send_message(chat_id=message.chat.id, text = utils.get_question(cons['ru']['goal of request'])['question'], reply_markup=keyboard)

@bot.message_handler(func = lambda message: message.text in cons['ru']['goal of request']['answers'])
def send_button(message):	
	for i in cons['ru'][message.text]:
		keyboard = telebot.types.InlineKeyboardMarkup()
		dic = utils.get_button(i)
		if dic['url']=='None':
			bot.send_message(chat_id=message.chat.id, text = dic['message'])
		elif dic['url']!='None':
			keyboard.add(telebot.types.InlineKeyboardButton(text=dic['button_text'], url=dic['url']))
			bot.send_message(chat_id = message.chat.id, text = dic['message'] ,reply_markup = keyboard )
#eng part
@bot.message_handler(func=  lambda message: message.text == cons['eng']['language'])
def send_button(message):
		keyboard = telebot.types.InlineKeyboardMarkup()
		dic = cons['eng']['contacts']
		keyboard.add(telebot.types.InlineKeyboardButton(text=dic['button text'], url=dic['url']))
		bot.send_message(chat_id = message.chat.id, text = dic['message'] ,reply_markup = keyboard )

if __name__ == '__main__':
	bot.polling(none_stop=True)
