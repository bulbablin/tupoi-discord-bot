import discord
from discord.ext import tasks, commands
import sqlite3
from random import choice, randint
from discord import Color
from asyncio import sleep

import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from urllib.parse import unquote

############################

opts = Options()
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--no-sandbox')
opts.headless = True

driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), chrome_options = opts)

############################

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '_', intents = intents)

############################

db1 = sqlite3.connect('kto.db')
sql1 = db1.cursor()
db2 = sqlite3.connect('krutie.db')
sql2 = db2.cursor()
db3 = sqlite3.connect('lvl.db')
sql3 = db3.cursor()

sql3.execute("""CREATE TABLE IF NOT EXISTS lvl(
    level INT,
    exp INT
)""")
db3.commit()
sql1.execute("""CREATE TABLE IF NOT EXISTS kto(
    names TEXT,
    id INT,
    weapon TEXT,
    carry TEXT,
    support TEXT,
    reactor TEXT,
    description TEXT,
    truename TEXT,
    element TEXT,
    image TEXT
)""")
db1.commit() 
sql2.execute("""CREATE TABLE IF NOT EXISTS krutie(
    id INT,
    name TEXT
)""")
db2.commit()

############################

@client.event
async def on_ready():
	print("ВНИМАНИЕ! ВАШ КОМПЬЮТЕР БЫЛ ЗАРАЖЕН МАЙНЕРОМ!")

@client.command()
async def попит(ctx, arg1, arg2):
    try:
        arg1 = int(arg1)
        arg2 = int(arg2)
        l = []
        if arg1 > 0 and arg2 > 0 and arg1 < 14 and arg2 < 14:
            for i in range(arg1):
                l.append('||(-)||')
            l.append('\n')
            x = ''.join(l) * arg2
            await ctx.send(x)
    except:
        await ctx.send('Ну 2 числа введи камон. _попит 1-13 1-13')

            
@client.command()
async def вики(ctx, *args):
    try:
        arg1 = ' '.join(args)
        driver.get('https://genshin-impact.fandom.com/ru/wiki/Служебная:Поиск?query=&scope=internal&contentType=&ns%5B0%5D=0#')
        sleep(1)
        y = driver.find_element_by_xpath('//input[@class="unified-search__input__query"]')
        y.send_keys(arg1)
        y.send_keys(Keys.ENTER)
        x = driver.find_elements_by_class_name('unified-search__result__title')[0].get_attribute('href')
        await ctx.send("<" + unquote(x) + ">")
    except:
        await ctx.send('ошибочка...')

@client.command()
async def розыгрыш(ctx, *args):
    arg = " ".join(args)
    a = []
    channel = ctx.message.author.voice.channel
    print(channel)
    members = channel.members
    print(members)
    for member in members:
        a.append(member)
    x = choice(a)
    x = x.mention
    e = discord.Embed(title = '**Победитель выбран!**', description = f'**Поздравляем -** {x}! Вы стали победителем розыгрыша.\n\n🎁 **Приз:\n**{arg}')
    await ctx.send(embed = e)	


@client.command()
async def таймер(ctx, arg):
    try:
        arg = int(arg)
        if arg > 300:
            await ctx.send("может не надо")
        else:
            await ctx.send("Время пошло")
            sleep(arg)
            await ctx.send("Время кончилось")
    except:
        await ctx.send("Тебе нужно написать `_таймер <время (в секундах)>`")

##########################################################################################################################################################
###### ГАЙДЫ НА ПЕРСОВ ГЕНШИНА ### ГОТОВОЕ ДБ С НИМИ ИДЕТ В КОМПЛЕКТЕ, ДЛЯ ИЗМЕНЕНИЯ ВАМ НУЖНО БЫТЬ КРУТЫМ (_крутой <дискорд айди чела> имя(любое)) ######
##########################################################################################################################################################

@client.command()
async def описание(ctx, *args):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(args[0])
            arg2 = ' '.join(args[1:])
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid1 = [i[0] for i in charid]
            if arg1 in charid1:
                sql1.execute(f'UPDATE kto SET description = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Описание успешно изменено.")
            else:
                await ctx.send("Ошибочка с айди.")
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e)    


@client.command()
async def картинка(ctx, arg1):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(arg1)
            arg2 = ctx.message.attachments[0].url
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid1 = [i[0] for i in charid]
            if arg1 in charid1:
                sql1.execute(f'UPDATE kto SET image = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Картинка успешно изменена.")
            else:
                await ctx.send("Ошибочка с айди.")
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e)  

        
@client.command()
async def оружие(ctx, arg1, arg2):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(arg1)
            arg2 = str(arg2)
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid1 = [i[0] for i in charid]
            if arg1 in charid1:
                sql1.execute(f'UPDATE kto SET weapon = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Оружие успешно изменено.")
            else:
                await ctx.send("Ошибочка с айди.")
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e)  


@client.command()
async def удалить(ctx, arg1):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(arg1)
            sql1.execute(f'DELETE FROM kto WHERE id = {arg1}')
            db1.commit()
            l = sql1.execute('SELECT COUNT(*) FROM kto').fetchone()[0]
            for i in range(l):
                i += 1
                try:
                    sql1.execute(f'UPDATE kto SET id = {arg1 + i - 1} WHERE id = {arg1 + i}')
                    db1.commit()
                except:
                    break
            await ctx.send("Удалил.")
    except Exception as e:
        await ctx.send("Ошибка.")
        print(e)


@client.command()
async def оценка(ctx, arg1, arg2, arg3, arg4):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(arg1)
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid1 = [i[0] for i in charid]
            if arg1 in charid1:
                sql1.execute(f'UPDATE kto SET carry = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                sql1.execute(f'UPDATE kto SET support = "{arg3}" WHERE id = {arg1}')
                db1.commit()
                sql1.execute(f'UPDATE kto SET reactor = "{arg4}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Оценка успешно изменена.")
            else:
                await ctx.send("Ошибочка с айди.")
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e)  


@client.command()
async def кто(ctx, arg1):
    arg1 = arg1.lower()
    nms = sql1.execute("SELECT names FROM kto").fetchall()
    nms1 = [i[0] for i in nms]
    for i, elem in enumerate(nms):
        elem = elem[0]
        if arg1 in elem:
            nm = nms1[i]
    tn = sql1.execute(f'SELECT truename FROM kto WHERE names = "{nm}"').fetchone()[0]
    el = sql1.execute(f'SELECT element FROM kto WHERE names = "{nm}"').fetchone()[0] 
    oj = sql1.execute(f'SELECT weapon FROM kto WHERE names = "{nm}"').fetchone()[0] 
    cr = sql1.execute(f'SELECT carry FROM kto WHERE names = "{nm}"').fetchone()[0]
    sp = sql1.execute(f'SELECT support FROM kto WHERE names = "{nm}"').fetchone()[0] 
    rc = sql1.execute(f'SELECT reactor FROM kto WHERE names = "{nm}"').fetchone()[0] 
    ds = sql1.execute(f'SELECT description FROM kto WHERE names = "{nm}"').fetchone()[0]
    u = sql1.execute(f'SELECT image FROM kto WHERE names = "{nm}"').fetchone()[0]
    if el == "Пиро":
        col = Color.red()
    elif el == "Гидро":
        col = Color.dark_blue()
    elif el == "Электро":
        col = Color.dark_purple()
    elif el == "Крио":
        col = Color.teal()
    elif el == "Дендро":
        col = Color.dark_green()
    elif el == "Анемо":
        col = Color.green()
    elif el == "Гео":
        col = Color.dark_gold()
    else:
        col = Color.green()
    
    e = discord.Embed(title = f'**{tn}**', description = f'Стихия: `{el}`\nОружие: `{oj}`\n\nКерри: `{cr}`\nСаппорт: `{sp}`\nРеактор: `{rc}`\n\n{ds}', color = col)
    e.set_thumbnail(url = u)
    await ctx.send(embed = e)

    
@client.command()
async def нормимя(ctx, *args):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(args[0])
            arg2 = ' '.join(args[1:])
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid1 = [i[0] for i in charid]
            if arg1 in charid1:
                sql1.execute(f'UPDATE kto SET truename = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Имя успешно изменено.")
            else:
                await ctx.send("Ошибочка с айди.")
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e)    


@client.command()
async def элемент(ctx, *args):
    try:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(args[0])
            arg2 = ' '.join(args[1:])
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid1 = [i[0] for i in charid]
            if arg1 in charid1:
                sql1.execute(f'UPDATE kto SET element = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Элемент успешно изменен.")
            else:
                await ctx.send("Ошибочка с айди.")
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e)     


@client.command()
async def айди(ctx):
    try:
        ids = sql1.execute('SELECT id FROM kto').fetchall()
        ids = [i[0] for i in ids]
        nms = sql1.execute('SELECT names FROM kto').fetchall()
        nms = [i[0] for i in nms]
        tnms = sql1.execute('SELECT truename FROM kto').fetchall()
        tnms = [i[0] for i in tnms]
        s = ""
        for i in range(len(ids)):
            s = s + str(tnms[i] + " - " + str(nms[i]) + " - **" + str(ids[i]) + "**\n")
        e = discord.Embed(description = s, title = "Айдишники и имена")
        await ctx.send(embed = e)
    except Exception as e:
        await ctx.send("Ошибочка.")            
        print(e) 


@client.command()
async def крутой(ctx, arg1, arg2):
    try:
        arg1 = int(arg1)
        ids = [698606229521432606, 399857176895815680, 802556252332752926]
        if ctx.message.author.id in ids:
            sql2.execute(f"INSERT INTO krutie VALUES ({arg1}, '{arg2}')")
            db2.commit()
            await ctx.send(f'{arg2} теперь редактор! (айди: {str(arg1)})')
    except Exception as e:
        print(e)
        await ctx.send("ошибка...")


@client.command()
async def имена(ctx, arg1):
    try:
        x = sql1.execute('SELECT names FROM kto').fetchall()
        x = [i[0] for i in x]
        print(x)
        s = ''
        for i, elem in enumerate(x):
            print(elem)
            if arg1 in elem:
                s = x[i]
                break
        if s != '':
            s = ', '.join(s.split())
            await ctx.send("`" + s + "`")
        else:
            await ctx.send('Чет не так.')
    except Exception as e:
        print(e)
        await ctx.send("ошибка...")	
    

@client.command()
async def бекап(ctx):
    ids = sql2.execute('SELECT id FROM krutie').fetchall()
    ids = [i[0] for i in ids]
    x = ''
    if ctx.message.author.id in ids:
        x = os.path.abspath('kto.db')
        await eval(f'ctx.send(file=discord.File(r"{x}"))')
        x = os.path.abspath('krutie.db')
        await eval(f'ctx.send(file=discord.File(r"{x}"))')
        x = os.path.abspath('chto.db')
        await eval(f'ctx.send(file=discord.File(r"{x}"))')
	

@client.command()
async def добавить(ctx, *args):
    ids = sql2.execute('SELECT id FROM krutie').fetchall()
    ids = [i[0] for i in ids]
    if ctx.message.author.id in ids:
        arg = ' '.join(args).lower()
        x = sql1.execute('SELECT COUNT(*) FROM kto').fetchone()[0]
        sql1.execute(f'INSERT INTO kto VALUES ("{arg}", {x + 1}, "Оружие какое-то", "0", "0", "0", "Описание", "Норм имя", "Элемент", "https://cdn.discordapp.com/attachments/517055018126278717/858594873178193930/1617445555_32bb90e8976aab5298d5da10fe66f21d.png")')
        db1.commit()
        await ctx.send(f'Персонаж добавлен. Его имена: {arg}. Далее стоит указать его `_оружие, _картинка, _оценка, _описание, _нормимя, _элемент`. Айди персонажа - {x + 1}.')

if __name__ == '__main__':
    token = 'ТОКЕН СВОЙ ВВЕДИ НУ НЕ МОЙ ЖЕ Я ТЕБЕ ДАМ НУ СОВЕСТЬ ИМЕЙ'
    client.run(token)
