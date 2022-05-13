#ReminderBot

#Bot um Erinnerung für die HS einzustellen
#author: Jonas Hauenstein
#Date last edited: 13.05.2022
#To-Do: 
#Mehrere Assignements löschen
# " wird bei neu nicht erkannt
# Riesen files und texte als Argument
#Logger hinzufügen
#pickle save machen
#checken ob remote code execution verhindert wird

import os
import pickle

from datetime import datetime, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv

assignements = list()
remember_channel = None

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='neu', help='Legt ein neues Assignement an\n!neu <TT-MM-JJ> <HH:MM> <Text>')
async def add_ass(ctx, date_text, time_text, *texteingabe):
    try:
        date_time_string = date_text + " " + time_text

        date_and_time = datetime.strptime(date_time_string, '%d-%m-%y %H:%M')

        texte = " ".join(texteingabe)

        if len(texte) > 100:
            await ctx.send("Chad Knauber sagt: Kein Assignement hat so einen langen Namen")
            return ""


        if assignements:
            await load_list() 

        items = [texte.strip(), date_and_time]
        assignements.append(items)
        await save_list()
        await ctx.send("Chad Knauber sagt: Geiler Ass. Ist hinzugefügt.")
    except ValueError:
        await ctx.send("Datum oder Datumsformat ungültig. Format: dd-mm-yy hh:mm")


@bot.command(name='show', help='Zeigt alle Asses')
async def show_ass(ctx):
        if assignements:
            await load_list()
        else:
            await ctx.send("Alles erledigt :)")
            return ""
        
        assignementString = ''
        counter = 1
        for i in assignements:
            assignementString += f'{counter} - \'{i[0]}\' ---- {i[1].strftime("%d-%m-%Y %H:%M")} Uhr\n'
            counter += 1
        await ctx.send(assignementString)


@bot.command(name='del', help='Löscht bestimmtes Assignement !del <index> - Um den Index zu sehen !show')
async def delete_ass(ctx, index):
    #TO-DO: Mehrere löschen zB !del 2-4 (löscht 2,3 und 4)
    try:
        await load_list()
        await ctx.send(f"Assignement \"{assignements[int(index)-1][0]}\" erfolgreich gelöscht.")
        del assignements[int(index)-1]
        await save_list()
    except IndexError:
        await ctx.send(f"Es gibt kein Assignement mit der Nummer {index}")


@bot.command(name='register', help='Auf dem ausgeführten Channel kommen die Erinnerungen')
async def set_remember_channel(ctx):
    global remember_channel
    remember_channel = ctx.channel



@tasks.loop(hours=24.0)
async def send_remember():
    if (remember_channel == None):
        return ""

    if assignements:
        await load_list()
    else:
        return ""

    now = datetime.today()
    for i in range(len(assignements)):
        if assignements[i][1] < now:
            await load_list()
            await remember_channel.send(f'\"{assignements[i][0]}\" vorbei. Wird gelöscht...')
            del assignements[i]
            await save_list()
        elif now >= assignements[i][1] - timedelta(days=5) and now < assignements[i][1] - timedelta(days = 2):
            await remember_channel.send(f'\"{assignements[i][0]}\" in unter 5 Tagen fällig!!')
        elif now >= assignements[i][1] - timedelta(days=2) and now < assignements[i][1] - timedelta(days = 1):
            await remember_channel.send(f'\"{assignements[i][0]}\" in unter 2 Tagen fällig!!') 
        elif now >= assignements[i][1]- timedelta(days=1):
            await remember_channel.send(f'\"{assignements[i][0]}\" !!Abgabe morgen fällig!!')    


#Helping Methods

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Chad Knauber brauch mehr Infos! !help \"command\" für mehr Infos!")

#File handling
async def save_list():
    pickle.dump(assignements, open('assignement_list.obj', 'wb'))


async def load_list():
    global assignements 
    assignements = pickle.load(open('assignement_list.obj', 'rb'))

send_remember.start()
bot.run(TOKEN)