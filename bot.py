
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import config
import utils
from constants import cons
import cherrypy
from cherryserver import WebhookServer
WEBHOOK_HOST = '185.173.94.116'
WEBHOOK_PORT = 443  # 443, 80, 88, 8443
WEBHOOK_LISTEN = '0.0.0.0'  

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # certificate path
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

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

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

