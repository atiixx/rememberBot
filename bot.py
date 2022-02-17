#ReminderBot

#Bot um Erinnerung für die HS einzustellen
#author: Jonas Hauenstein
#Date last edited: 12.12.2021
#To-Do: 
#Mehrere Assignements löschen
#Feedback wenn erfolgreich
#check if sender is bot not working

import os
import pickle

from datetime import datetime, timedelta
from discord.ext import commands
from dotenv import load_dotenv

assignements = list()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TEST_CHANNEL = 918127437068533770
PROD_CHANNEL = 943960532875104266
FIRSTREMINDER_DAYS = 5
SECONDREMINDER_DAYS = 2
LASTREMINDER_DAYS = 1

bot = commands.Bot(command_prefix='!')

@bot.command(name='neu', help='Legt ein neues Assignement an\n!neu <TT-MM-JJ> <HH:MM> <Text>')
async def add_ass(ctx, date_text, time_text, *texte):
    try:
        date_time_string = date_text + " " + time_text

        date_and_time = datetime.strptime(date_time_string, '%d-%m-%y %H:%M')

        text = ''

        for worte in texte:
            text += worte + ' '

        if assignements:
            await load_list() 

        items = [text.strip(), date_and_time]
        assignements.append(items)
        await save_list()
        await send_remember()
        await bot.get_channel(PROD_CHANNEL).send("Ass hinzugefügt")
        #await bot.get_channel(TEST_CHANNEL).send("Ass hinzugefügt")
    except ValueError:
        await bot.get_channel(PROD_CHANNEL).send("Datum oder Datumsformat ungültig. Format: dd-mm-yy hh:mm")
        #await bot.get_channel(TEST_CHANNEL).send("Datum oder Datumsformat ungültig. Format: dd-mm-yy hh:mm")



@bot.command(name='show', help='Zeigt alle Asses')
async def show_ass(ctx):
        if(assignements):
            await load_list()
        else:
            await bot.get_channel(PROD_CHANNEL).send("Alles erledigt :)")
            #await bot.get_channel(TEST_CHANNEL).send("Alles erledigt :)")
            return ""
        assignementString = ''
        counter = 1
        for i in assignements:
            assignementString += f'{counter} - \'{i[0]}\' ist fällig bis zum {i[1].strftime("%d-%m-%Y %H:%M")} Uhr\n'
            counter += 1
        await bot.get_channel(PROD_CHANNEL).send(assignementString)
        #await bot.get_channel(TEST_CHANNEL).send(assignementString)


@bot.command(name='del', help='Löscht bestimmtes Assignement !del <index> - Um den Index zu sehen !show')
async def delete_ass(ctx, index):
    #TO-DO: Mehrere löschen zB !del 2-4 (löscht 2,3 und 4)

   # if index.author.bot:
   #return
    try:
        await load_list()
        await bot.get_channel(PROD_CHANNEL).send(f"Assignement \"{assignements[int(index)-1][0]}\" erfolgreich gelöscht.")
        #await bot.get_channel(TEST_CHANNEL).send(f"Assignement \"{assignements[int(index)-1][0]}\" erfolgreich gelöscht.")
        del assignements[int(index)-1]
        await save_list()
    except IndexError:
        await bot.get_channel(PROD_CHANNEL).send(f"Es gibt kein Assignement mit der Nummer {index}")
        #await bot.get_channel(TEST_CHANNEL).send(f"Es gibt kein Assignement mit der Nummer {index}")



async def send_remember():
    if assignements:
        await load_list()
    else:
        print("Keine Reminder geschickt.")
        return ""
    #channel = bot.get_channel(TEST_CHANNEL)
    channel = bot.get_channel(PROD_CHANNEL)
    now = datetime.today()
    for i in range(len(assignements)):
        if assignements[i][1] < now:
            await load_list()
            await channel.send(f'\"{assignements[i][0]}\" vorbei. Wird gelöscht...')
            del assignements[i]
            await save_list()
        elif now > assignements[i][1] - timedelta(days=5) and now < assignements[i][1] - timedelta(days = 2):
            await channel.send(f'\"{assignements[i][0]}\" in unter 5 Tagen fällig!!')
        elif now > assignements[i][1] - timedelta(days=2) and now < assignements[i][1] - timedelta(days = 1):
            await channel.send(f'\"{assignements[i][0]}\" in unter 2 Tagen fällig!!') 
        elif now >= assignements[i][1]- timedelta(days=1):
            await channel.send(f'\"{assignements[i][0]}\" !!Abgabe morgen fällig!!')    


async def save_list():
    pickle.dump(assignements, open('assignement_list.obj', 'wb'))


async def load_list():
    global assignements 
    assignements = pickle.load(open('assignement_list.obj', 'rb'))

bot.run(TOKEN)