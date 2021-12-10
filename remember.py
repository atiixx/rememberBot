import bot
import datetime

FIRSTREMINDER_DAYS = 5
SECONDREMINDER_DAYS = 2
LASTREMINDER_DAYS = 1

async def check_time():
    bot.load_list()
    test_channel = bot.bot.get_channel(918127437068533770)
    now = datetime.datetime.now()
    for i in range(len(bot.assignements)):
        if bot.assignements[i][1] > now:
            await bot.load_list()
            del bot.assignements[i]
            await bot.save_list()
        elif now > now - datetime.timedelta(days = FIRSTREMINDER_DAYS):
            test_channel.send(f'Abgabe in 5 Tagen fällig: {bot.assignements[i][0]}')
        elif now > now - datetime.timedelta(days = SECONDREMINDER_DAYS):
            test_channel.send(f'Abgabe in 2 Tagen fällig: {bot.assignements[i][0]}') 
        elif now > now - datetime.timedelta(days = LASTREMINDER_DAYS):
            test_channel.send(f'!!Abgabe morgen fällig: {bot.assignements[i][0]}!!')    



   

