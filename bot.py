#ReminderBot
#
#Bot um Erinnerung für die HS einzustellen
#author: Jonas Hauenstein
#Date last edited: 12.12.2021
#To-Do: 
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

@bot.command(name='neu', help='Legt ein neues Assignement an\n!neu <TT-MM-JJJJ> <HH:MM> <Text>')
async def add_new(ctx, date_text, time_text, *texte):
    """Added ein neues Assignement zur Liste"""
    try:
        day, month, year = map(int, date_text.split('-'))
        hour, minute = map(int, time_text.split(':'))

        if (day > 31 or day < 1 or month > 12 or month < 1 or year > 2030 or year < datetime.datetime.now().year):
            await bot.get_channel(919595793646776371).send("Ungültige Datumsangabe")
            exit

        if (hour < 0 or hour > 24 or minute < 0 or minute > 59):
            await bot.get_channel(919595793646776371).send("Ungültige Zeitangabe")
            exit

        date_and_time = datetime.datetime(year, month, day, hour, minute)
        text = ''
        for worte in texte:
            text += worte + ' '
        await load_list() 
        items = [text.strip(), date_and_time]
        assignements.append(items)
        await save_list()
    except (ValueError) as err:
        await bot.get_channel(919595793646776371).send("Bitte folgende Syntax nutzen: \n!neu <TT-MM-JJJJ> <HH:MM> <Text>")


@bot.command(name='show', help='Zeigt alle Asses')
async def show_ass(ctx):
    try:
        await load_list() 
        test_channel = bot.get_channel(919595793646776371)
        assignementString = ''
        counter = 1
        for i in assignements:
            assignementString += f'{counter} - \'{i[0]}\' ist fällig bis zum {i[1].strftime("%d-%m-%Y %H:%M")} Uhr \n'
            counter += 1
        await test_channel.send(assignementString)
        await test_channel.send("Now we wait to see if checktime works..")
        time.sleep(2)
        await send_remember()
    except:
        await bot.get_channel(919595793646776371).send("Alles erledigt! Keine Assignements übrig :)")


@bot.command(name='del', help='Löscht bestimmtes Assignement !del <index> - Um den Index zu sehen !show')
async def delete_ass(ctx, index):
    #TO-DO: Mehrere löschen zB !del 2-4 (löscht 2,3 und 4)
    try:
        await load_list()
        del assignements[int(index)-1]
        await save_list()
    except:
        await bot.get_channel(919595793646776371).send("Assignement nicht vorhanden")


@bot.event
async def on_command_error(ctx, error):
    send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)

    if isinstance(error, commands.CommandNotFound):  # fails silently
        pass

    elif isinstance(error, send_help):
        await ctx.send("Bitte richtige Syntax nutzen! \n!help oder !help <command> für mehr Informationen")


async def send_remember():
    await load_list()
    test_channel = bot.get_channel(919595793646776371)
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