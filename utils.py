# -*- coding: utf-8 -*-

#request to constants.py
def get_question(dic):
	d=dict(question =dic['question'], answers = dic['answers'])
	return d

def get_button(dic):
	d=dict(message=dic['message'], button_text =dic['button text'], url = dic['url'] )
	return d


		



