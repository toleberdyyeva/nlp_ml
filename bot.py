
import config
from bs4 import BeautifulSoup
import telebot
import json
from Predict import predict, get_reviews_from_array
from telebot import types
import os

bot = telebot.TeleBot(config.token)
import requests

LOCATION = ''



# Message Handler
@bot.message_handler(commands=['set_location'])
def handle_location(message):
    
    result_message = 'Giving to you a button with location 😉'
    markup = types.ReplyKeyboardMarkup()
    loc_button = types.KeyboardButton('My location', request_location=True)
    markup.add(loc_button)
    bot.send_message(message.chat.id, result_message, reply_markup=markup , parse_mode='HTML')



@bot.message_handler(commands=["start"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    result_message = '🚀 To access my service to finding \nplaces with cognative reviews :D \n, just type ... \n/place Macdondals'
    bot.send_message(message.chat.id, result_message , parse_mode='HTML')


@bot.message_handler(commands=['place'])
def handle_location(message):
    if (message.text.strip() == '/place') :
        bot.send_message(message.chat.id, 'okay there is  example :<br>"<b>\n/place Macdondals in centre of London </b> "', parse_mode='HTML')
    else: 
        file =  open('data.txt', 'r')
        print(file.read())
        if (len(file.read()) > 0 ):
            result_message = '<b>Sorry , Dude.</b>\nFirstlu you should\nshare location with me.\n📍 /set_location'
        else:
            file = open('data.txt', 'r')
            result_message = '🔮loading ... '
            bot.send_message(message.chat.id, result_message, parse_mode='HTML')
            keyword = message.text[7:]
            language = 'en'
            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?&query={0}&language={1}&key={2}'.format(
                 keyword, language, config.gogole_map_api_key)
            req = requests.get(url)
            # print(req.json()['results'])
            if req.json()['status'] == 'ZERO_RESULTS' :
                bot.send_message(message.chat.id, '<b>Not found </b> 🤬' ,parse_mode='HTML')
            else:
                for result in req.json()['results'][::6]:
                    vin = '<b>'+ result['name'] +'</b>\n📍'+ result['formatted_address']
                    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={0}&key={1}'.format(result['place_id'], config.gogole_map_api_key)
                    detail_req = requests.get(url)
                    # print(detail_req.json()['status'])
                    if detail_req.json()['status'] == 'OK' :
                        # print(detail_req.json()['result']['reviews'])
                        if ( 'reviews' in detail_req.json()['result']):
                            reviews = []
                            for review in detail_req.json()['result']['reviews']:
                                if (review['language'] == 'en'):
                                    reviews.append(review['text'])
                            predicteds = predict(reviews)
                            if (len(predicteds) > 0):
                                vin += '\nThere are <b>' + str(len(predicteds)) + '</b> review(s).'
                                bot.send_message(message.chat.id, vin, parse_mode='HTML')
                                print('===========')
                                print(predicteds)
                                print('===========')
                    else :
                        vin += '\nSorry , this venue has no any reviews.'
                        bot.send_message(message.chat.id, vin, parse_mode='HTML')

            # bot.send_message(message.chat.id, '', parse_mode='HTML')
             
                    # for review in detail_req.json()['reviews']:
                    #     print(review['text'])



@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    print(message)
    result_message = 'Yo-Yo 😎 <b>'+ message.from_user.username +'</b>🔥\nkeep hot-man and type\n/place to start of course.'
    # result_message = message.text
    bot.send_message(message.chat.id, result_message, parse_mode='HTML')


@bot.message_handler(content_types=['location'])
def handle_location(message):
    file = open('data.txt','w')
    file.write('{0},{1}'.format(str(message.location.latitude), str(message.location.longitude)))
    file.close()
    result_message = 'Your Location is Setted ✅ :\n <b>{0}'.format('{0},{1}'.format(str(message.location.latitude), str(message.location.longitude)))+"</b>"
    bot.send_message(message.chat.id, result_message,  parse_mode='HTML')





# Bot INIT run
if __name__ == '__main__':
    bot.polling(none_stop=True)


