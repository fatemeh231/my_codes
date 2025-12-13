# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 22:03:45 2025

@author: fatemeh hosseininasab
"""
import telebot
import requests

bot = telebot.TeleBot("8330348056:AAHBa7nmGR137oFedRLoQBEYbvjihQ0vNsk")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "HELLO, WHICH SYMBOL ARE YOU GOING TO CHECK ITS PRICE?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "This bot gives you the live price of a cryptocurrency pair. Send a symbol like BTCUSDT or ETHUSDT the second pair must be in crypto stable part.")

@bot.message_handler(func=lambda m: True)
def show_price(message):
    symbol = message.text.upper()
    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        bot.reply_to(message,f"{symbol} price is: {data['price']}")
    else:
        print("Error fetching price: ")


bot.infinity_polling()