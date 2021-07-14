import discord
from discord.ext import commands

import sqlite3
from random import choice
from discord import Color
from time import sleep

import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote

opts = Options()
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--no-sandbox')
opts.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=opts)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='_', intents=intents)

colors = {
    'Пиро': discord.Color.red(),
    'Гидро': discord.Color.blue(),
    'Электро': discord.Color.dark_purple(),
    'Крио': discord.Color.teal(),
    'Дендро': discord.Color.dark_green(),
    'Анемо': discord.Color.green(),
    'Гео': discord.Color.dark_gold()
}

db1 = sqlite3.connect('kto.db', check_same_thread=False)
sql1 = db1.cursor()

db2 = sqlite3.connect('krutie.db', check_same_thread=False)
sql2 = db2.cursor()

db3 = sqlite3.connect('lvl.db', check_same_thread=False)
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


@client.event
async def on_ready():
    print("ВНИМАНИЕ! ВАШ КОМПЬЮТЕР БЫЛ ЗАРАЖЕН МАЙНЕРОМ!")


@client.command()
async def попит(ctx, arg1, arg2):
    if arg1.isnumeric() and arg2.isnumeric():
        arg1 = int(arg1)  # горизонтальный ряд
        arg2 = int(arg2)  # вертикальный
        pupirki = []
        if 0 < arg1 < 14 and 0 < arg2 < 14:
            for i in range(arg1):
                pupirki.append('||(-)||')
            pupirki.append('\n')
            msg = ''.join(pupirki) * arg2
            await ctx.send(msg)
    else:
        await ctx.send('Ну 2 числа введи камон. _попит 1-13 1-13')


@client.command()
async def вики(ctx, *args):
    try:
        arg1 = ' '.join(args)
        driver.get(
            'https://genshin-impact.fandom.com/ru/wiki/Служебная:Поиск?query=&scope=internal&contentType=&ns%5B0%5D=0#')
        sleep(1)
        search = driver.find_element_by_xpath('//input[@class="unified-search__input__query"]')
        search.send_keys(arg1)
        search.send_keys(Keys.ENTER)
        result = driver.find_elements_by_class_name('unified-search__result__title')[0].get_attribute('href')
        await ctx.send("<" + unquote(result) + ">")
    except:
        await ctx.send('ошибочка...')


@client.command()
async def розыгрыш(ctx, *args):
    arg = " ".join(args)
    mems = []
    channel = ctx.message.author.voice.channel
    print(channel)
    members = channel.members
    print(members)
    for member in members:
        mems.append(member)
    winner = choice(mems).mention
    emb = discord.Embed(title='**Победитель выбран!**',
                        description=f'**Поздравляем ** {winner}! Вы стали победителем розыгрыша.\n\n🎁 **Приз:\n**{arg}')
    await ctx.send(embed=emb)


# дальше гайды на персов, для изменения добавьте себя в бд редакторов (_крутой @человек)

@client.command()
async def крутой(ctx, arg1, arg2):
    ids = ['АЙДИ СВОЙ СЮДА ВВЕДИ СОВЕСТЬ ИМЕЙ И ДРУГА СУНЬ ЕСЛИ ЕСТЬ']
    if arg1.isnumeric():
        arg1 = int(arg1)
        if ctx.message.author.id in ids:
            sql2.execute(f"INSERT INTO krutie VALUES ({arg1}, '{arg2}')")
            db2.commit()
            await ctx.send(f'{arg2} теперь редактор! (айди: {arg1})')
    else:
        await ctx.send("Число введи")


@client.command()
async def описание(ctx, *args):
    if args[0].isnumeric:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(args[0])
            arg2 = ' '.join(args[1:])
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid = [i[0] for i in charid]
            if arg1 in charid:
                sql1.execute(f'UPDATE kto SET description = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Описание успешно изменено.")
            else:
                await ctx.send("Ошибочка с айди.")
    else:
        await ctx.send("Число введи")


@client.command()
async def картинка(ctx, arg1):
    if arg1.isnumeric:
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
    else:
        await ctx.send("Число введи")


@client.command()
async def оружие(ctx, arg1, arg2):
    if arg1.isnumeric:
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(arg1)
            charid = sql1.execute('SELECT id FROM kto').fetchall()
            charid = [i[0] for i in charid]
            if arg1 in charid:
                sql1.execute(f'UPDATE kto SET weapon = "{arg2}" WHERE id = {arg1}')
                db1.commit()
                await ctx.send("Оружие успешно изменено.")
            else:
                await ctx.send("Ошибочка с айди.")
    else:
        await ctx.send("Число введи")


@client.command()
async def удалить(ctx, arg1):
    if arg1.isnumeric():
        ids = sql2.execute('SELECT id FROM krutie').fetchall()
        ids = [i[0] for i in ids]
        if ctx.message.author.id in ids:
            arg1 = int(arg1)
            sql1.execute(f'DELETE FROM kto WHERE id = {arg1}')
            db1.commit()
            rows = sql1.execute('SELECT COUNT(*) FROM kto').fetchone()[0]
            for i in range(rows):
                i += 1
                try:
                    sql1.execute(f'UPDATE kto SET id = {arg1 + i - 1} WHERE id = {arg1 + i}')
                    db1.commit()
                except:
                    break

            await ctx.send("Удалил.")

    else:
        await ctx.send("Число введи")


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
    img = sql1.execute(f'SELECT image FROM kto WHERE names = "{nm}"').fetchone()[0]

    try:
        col = colors[el]
    except:
        col = Color.green()

    e = discord.Embed(title=f'**{tn}**',
                      description=f'Стихия: `{el}`\nОружие: `{oj}`\n\nКерри: `{cr}`\nСаппорт: `{sp}`\nРеактор: `{rc}`\n\n{ds}',
                      color=col)
    e.set_thumbnail(url=img)
    await ctx.send(embed=e)


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
        e = discord.Embed(description=s, title="Айдишники и имена")
        await ctx.send(embed=e)
    except Exception as e:
        await ctx.send("Ошибочка.")
        print(e)


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
    if ctx.message.author.id in ids:
        kto = os.path.abspath('kto.db')
        krutie = os.path.abspath('krutie.db')
        await ctx.send(file=discord.File(kto))
        await ctx.send(file=discord.File(krutie))


@client.command()
async def добавить(ctx, *args):
    ids = sql2.execute('SELECT id FROM krutie').fetchall()
    ids = [i[0] for i in ids]
    if ctx.message.author.id in ids:
        arg = ' '.join(args).lower()
        x = sql1.execute('SELECT COUNT(*) FROM kto').fetchone()[0]
        pic = "https://cdn.discordapp.com/attachments/517055018126278717/858594873178193930/1617445555_32bb90e8976aab5298d5da10fe66f21d.png"
        sql1.execute(
            f'INSERT INTO kto VALUES ("{arg}", {x + 1}, "Оружие какое-то", "0", "0", "0", "Описание", "Норм имя", "Элемент", {pic})')
        db1.commit()
        await ctx.send(
            f'Персонаж добавлен. Его имена: {arg}. Далее стоит указать его `_оружие, _картинка, _оценка, _описание, _нормимя, _элемент`. Айди персонажа - {x + 1}.')


if __name__ == '__main__':
    token = 'ТОКЕН СВОЙ ВВЕДИ НУ НЕ МОЙ ЖЕ Я ТЕБЕ ДАМ НУ СОВЕСТЬ ИМЕЙ'
    client.run(token)
