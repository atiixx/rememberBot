#ReminderBot
#
#Bot um Erinnerung für die HS einzustellen
#author: Jonas Hauenstein
#Date last edited: 10.12.2021
#To-Do to prod.: 
#Automatische Reminder 5 Tage vorher + 1 Tag vorher (evtl cron?)
#Error handling
#Mehrere Assignements löschen


import os
import datetime
import pickle
import time

from discord.ext import commands
from dotenv import load_dotenv

assignements = list()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FIRSTREMINDER_DAYS = 5
SECONDREMINDER_DAYS = 2
LASTREMINDER_DAYS = 1

bot = commands.Bot(command_prefix='!')

@bot.command(name='neu', help='Legt ein neues Assignement an !neu <TT-MM-JJJJ> <HH:MM> <Text>')
async def add_new(ctx, date_text, time_text, *texte):
    day, month, year = map(int, date_text.split('-'))
    hour, minute = map(int, time_text.split(':'))
    date_and_time = datetime.datetime(year, month, day, hour, minute)
    text = ''
    for worte in texte:
        text += worte + ' '
    await load_list() 
    items = [text.strip(), date_and_time]
    assignements.append(items)
    await save_list()

@bot.command(name='show', help='Zeigt alle Asses')
async def show_ass(ctx):
    await load_list() 
    test_channel = bot.get_channel(918127437068533770)
    assignementString = ''
    counter = 1
    for i in assignements:
        assignementString += f'{counter} - \'{i[0]}\' ist fällig bis zum {i[1].strftime("%d-%m-%Y %H:%M")} Uhr \n'
        counter += 1
    await test_channel.send(assignementString)
    await test_channel.send("Now we wait to see if checktime works..")
    time.sleep(2)
    await send_remember()


@bot.command(name='del', help='Löscht bestimmtes Assignement !del <index> - Um den Index zu sehen !show')
async def delete_ass(ctx, index):
    #TO-DO: Mehrere löschen zB !del 2-4 (löscht 2,3 und 4)
    await load_list()
    del assignements[int(index)-1]
    await save_list()

async def send_remember():
    await load_list()
    test_channel = bot.get_channel(918127437068533770)
    now = datetime.datetime.now()
    for i in range(len(assignements)):
        if assignements[i][1] < now:
            await load_list()
            del assignements[i]
            await save_list()
        elif now > assignements[i][1] - datetime.timedelta(days = FIRSTREMINDER_DAYS) and now < assignements[i][1] - datetime.timedelta(days = SECONDREMINDER_DAYS):
            await test_channel.send(f'Abgabe in 5 Tagen fällig: "{assignements[i][0]}"')
        elif now > assignements[i][1] - datetime.timedelta(days = SECONDREMINDER_DAYS) and now < assignements[i][1] - datetime.timedelta(days = LASTREMINDER_DAYS):
            await test_channel.send(f'Abgabe in 2 Tagen fällig: "{assignements[i][0]}"') 
        elif now > assignements[i][1]- datetime.timedelta(days = LASTREMINDER_DAYS):
            await test_channel.send(f'!!Abgabe morgen fällig: "{assignements[i][0]}"!!')    


async def save_list():
    pickle.dump(assignements, open('assignement_list.obj', 'wb'))


async def load_list():
    global assignements 
    assignements = pickle.load(open('assignement_list.obj', 'rb'))

bot.run(TOKEN)