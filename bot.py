import discord
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import re, os, sys
import clock
import wikipedia
import json
import requests
import random
from PIL import Image, ImageFont, ImageDraw
import io
from discord.ext.commands import Bot
import asyncio
import time
from re import search
from discord import utils
from urllib import request
from urllib.parse import quote
import urllib.request
import config
import math
import sqlite3
import psutil as ps
from Cybernator import Paginator
from psutil import virtual_memory
from config import settings
from config import COLORS

prefix = settings['PREFIX']

client = commands.Bot(command_prefix = settings['PREFIX'])
client.remove_command("help")
queue = []
queue1 = []


connection = sqlite3.connect('server.db')
cursor = connection.cursor()


@client.event
async def on_ready():
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
		name TEXT,
		id INT,
		cash BIGINT,
		rep INT,
		lvl INT
	)""")
 
	cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
		role_id INT,
		id INT,
		cost BIGINT
	)""")
 
	for guild in client.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
			else:
				pass	

	connection.commit()
	print (f"Logged on as {settings['NAME BOT']}")

	await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=f"{prefix}help | Alpha", url="https://www.twitch.tv/bratishkinoff"))

#AutoRole and etc
@client.event
async def on_member_join( member ):
	role = discord.utils.get (member.guild.roles , id = 722476920591351899) #ID Роли
	await member.add_roles (role)
	role2 = discord.utils.get (member.guild.roles , id = 722476762574880878) #ID Роли
	await member.add_roles (role2)
	role3 = discord.utils.get (member.guild.roles , id = 722476594567970876) #ID Роли
	await member.add_roles (role3)
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
		connection.commit()
	else:
		pass



#===============Economy==============#
#Balance
@client.command(aliases = ['balance','Balance', 'BALANCE','bALANCE', 'cash','CASH','cASH','Cash','bal','BAL','bAL','Bal','ebal','EBAL','Ebal','eBAL','money','MONEY','Money','mONEY',"Баланс","баланс","БАЛАНС","бАЛАНС"])
async def __balance(ctx, member: discord.Member = None):
	if member is None:
		await ctx.send(embed = discord.Embed(
			description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :moneybag: **"""
		))
	else:
		await ctx.send(embed = discord.Embed(
			description = f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :moneybag: **"""
		))	

	print(f'[Logs:economy] Информация о балансе пользователя была успешно выведена | {prefix}balance ')


#Reward
@client.command(aliases = ['award','Award','AWARD','aWARD','reward','Reward','REWARD','rEWARD','Вознаграждение','вознаграждение','ВОЗНАГРАЖДЕНИЕ','вОЗНАГРАЖДЕНИЕ','Награда','награда','НАГРАДА','нАГАРАДА'])
@commands.has_permissions ( administrator = True )
async def __award(ctx, member: discord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите пользователя, которому вы желаете выдать денежное вознаграждение")
		print(f'[Logs:economy] Пользователь не был указан | {prefix}reward ')
	else:
		if amount is None:
			await ctx.send(f"**{ctx.author}**, укажите сумму, которую вы желаете выдать в виде денежного вознаграждения")
			print(f"[Logs:economy] [Error] Необходимо указать сумму которую вы хотите выдать | {prefix}reward")
		elif amount < 1:
			await ctx.send(f"**{ctx.author}**, вы не можете выдать отрицательную сумму :moneybag:!")
			print(f"[Logs:economy] [Error] Не возможно выдать отрицательную сумму денег | {prefix}reward")
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))	
			connection.commit()

			await ctx.message.add_reaction('✅')

			print(f'[Logs:economy] Пользователю {member} было успешно выданно {amount}$ | {prefix}reward ')
			


#Take money
@client.command(aliases = ['Take-money','take-money','TAKE-MONEY','tAKE-MONEY','Забрать-деньги','забрать-деньги','ЗАБРАТЬ-ДЕНЬГИ','зАБРАТЬ-ДЕНЬГИ', 'Отнять', 'отнять','ОТНЯТЬ','оТНЯТЬ'])
@commands.has_permissions ( administrator = True )
async def __take(ctx, member: discord.Member = None, amount = None):
	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите пользователя, у которого вы желаете отнять некоторое количество денег")
		print(f'[Logs:economy] Пользователь не был указан | {prefix}take-money ')
	else:
		if amount is None:
			await ctx.send(f"**{ctx.author}**, укажите сумму, которую вы желаете отнять у пользователя")
			print(f'[Logs:economy] Сумма не была указана | {prefix}take-money ')
		elif amount == "all":
			cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))	
			connection.commit()

			await ctx.message.add_reaction('✅')
			await ctx.send(f"У пользователя были успешно сняты все денеги!:moneybag:")
			print(f'[Logs:economy] У {member} были успешно сняты все деньги | {prefix}take-money ')
		elif int(amount) < 1:
			await ctx.send(f"**{ctx.author}**, вы не можете отнять отрицательную сумму денег :moneybag:!")
			print(f'[Logs:economy] Вы не можете отнять отрицательную сумму денег | {prefix}take-money ')
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))	
			connection.commit()

			await ctx.message.add_reaction('✅')
			await ctx.send(f"У {member} было успешно снято {int(amount)}:moneybag:! | {prefix}take-money")

			print(f'[Logs:economy] У {member} было успешно снято {int(amount)}$ | {prefix}take-money ')


#Add Role in Shop
@client.command(aliases = ['add-shop','ADD-SHOP','Add-shop','aDD-SHOP','Добавить-магазин','добавить-магазин','ДОБАВИТЬ-МАГАЗИН','дОБАВИТЬ-МАГАЗИН'])
@commands.has_permissions ( administrator = True )
async def __add_shop(ctx, role: discord.Role = None, cost: int = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль, которую вы хотите внести в магазин")
		print(f'[Logs:economy] Необходимо указать роль, которую вы хотите внести вмагазин | {prefix}add-shop ')
	else:
		if cost is None:
			await ctx.send(f"**{ctx.author}**, укажите стоимость, которую вы хотите установить для данной роли")
			print(f'[Logs:economy] Необходимо указать стоимость данной роли | {prefix}add-shop ')
		elif cost < 0:
			await ctx.send(f"**{ctx.author}**, вы не можете установить отрицательную стоимость для данной роли!")
			print(f'[Logs:economy] Вы не можете установить отрицательную стоимость для данной роли | {prefix}add-shop ')
		else:
			cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
			connection.commit()

			await ctx.message.add_reaction('✅')

			print(f'[Logs:economy] {ctx.author} добавил роль [{role}] в магазина | {prefix}add-shop ')

#Remove Role from the Shop
@client.command(aliases = ['remove-shop','REMOVE-SHOP','Remove-shop','rEMOVE-SHOP','Удалить-магазин','удалить-магазин','УДАЛИТЬ-МАГАЗИН','уДАЛИТЬ-МАГАЗИН'])
@commands.has_permissions ( administrator = True )
async def __remove_shop(ctx, role: discord.Role = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль, которую необходимо удалить из магазина")
		print(f'[Logs:economy] Необходимо указать роль, которую необходимо удалить из магазина | {prefix}remove-shop ')
	else:
		cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		connection.commit()

		await ctx.message.add_reaction('✅')

		print(f'[Logs:economy] {ctx.author} удалил роль [{role}] из магазина | {prefix}remove-shop ')

#Shop
@client.command(aliases = ['shop','sHOP','Shop','SHOP','магазин','Магазин','МАГАЗИН','мАГАЗИН'])		
async def __shop(ctx):
	embed = discord.Embed(title = "Магазин")

	for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
		if ctx.guild.get_role(row[0]) != None:
			embed.add_field(
				name = f"Стоимость **{row[1]} :moneybag:**",
				value = f"Вы приобрете роль {ctx.guild.get_role(row[0]).mention}",
				inline = False
			)
		else:
			pass

	await ctx.send(embed = embed)	

	print(f'[Logs:economy] Магазин был успешно выведен | {prefix}shop ')

#Buy role
@client.command(aliases = ['buy','buy-role','Buy','BUY','bUY','Buy-role','bUY-ROLE','BUY-ROLE','купить','Купить','КУПИТЬ','кУПИТЬ', 'Купить-роль','КУПИТЬ-РОЛЬ','кУПИТЬ-РОЛЬ','купить-роль'])
async def __buy_role(ctx, role: discord.Role = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль, которую вы хотите приобрести")
		print(f'[Logs:economy] Необходимо указать роль, которую вы хотите приобрести | {prefix}buy-role ')
	else:
		if role in ctx.author.roles:
			await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль")
			print(f'[Logs:economy] У {ctx.author} уже имеется данная роль [{role}] | {prefix}buy-role ')
		elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки данной роли")
			print(f'[Logs:economy] Недостаточно средств для покупки данной роли | {prefix}buy-role ')
		else:
			await ctx.author.add_roles(role)
			cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
			connection.commit()

			await ctx.message.add_reaction('✅')

			print(f'[Logs:economy] {ctx.author} приобрел роль [{role}] | {prefix}buy-role ')

#+Rep
@client.command(aliases = ['rep', '+rep', '+Rep', '+REP', '+rEP', 'Rep', 'REP', 'rEP'])
async def __rep(ctx, member: discord.Member = None):
	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите участника сервера")
		print(f'[Logs:economy] Необходимо указать участника сервера | {prefix}+rep ')
	else:
		if member.id == ctx.author.id:
			await ctx.send(f"**{ctx.author}**, вы не можете указать самого себя")
			print(f'[Logs:economy] Нельзя указывать самого себя | {prefix}+rep ')
		else:
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
			connection.commit()

			await ctx.message.add_reaction('✅')

			print(f'[Logs:economy] Пользователю {member} было добавлено 1 очко репутации | {prefix}+rep ')


#Leaderboard
@client.command(aliases = ['leaderboard', 'LEADERBOARD', 'lEADERBOARD', 'Leaderboard', 'lb', 'LB', 'lB', 'Lb', 'Лидеры','лидеры', 'ЛИДЕРЫ', 'лИДЕРЫ', 'forbs', 'FORBS', 'Forbs', 'fORBS', 'форбс', 'Форбс', 'ФОРБС', 'фОРБС'])
async def __leaderboard(ctx):
    embed = discord.Embed(title = 'Топ 10 миллионеров сервера')
    counter = 0
 
    for row in cursor.execute("SELECT name, cash FROM users ORDER BY cash DESC LIMIT 10"):
        counter += 1
        embed.add_field(
            name = f'# {counter} | `{row[0]}`',
            value = f'Баланс: {row[1]}',
            inline = False
        )
 
    await ctx.send(embed = embed)

    print(f'[Logs:economy] Список богачей сервера был успешно выведен | {prefix}leaderboard ')

#Daily Rewards
@client.command(aliases = ['Rewards', 'rewards', 'REWARDS', 'rEWARDS'])
async def __daily(ctx, option = None):
    if option == "Fame" or option == "fame" or option == "FAME" or option == "fAME":
        if not str(ctx.author.id) in queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы получили свои 1250 монет')
            await ctx.send(embed= emb)
            cursor.execute("UPDATE users SET cash = cash + 625 WHERE id = {}".format(ctx.author.id))	
            connection.commit()
            queue.append(str(ctx.author.id))
            await asyncio.sleep(12*60)
            queue.remove(str(ctx.author.id))
            print(f'[Logs:economy] {ctx.author} получил свой ежедневный бонус | {prefix}daily ')
        if str(ctx.author.id) in queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
            await ctx.send(embed= emb)
            print(f'[Logs:economy] {ctx.author} попытался получить свой ежедневный бонус | {prefix}daily ')
    if option == "Daily" or option == "daily" or option == "DAILY" or option == "dAILY":
        if not str(ctx.author.id) in queue1:
            emb = discord.Embed(description=f'**{ctx.author}** Вы получили свои 1250 монет')
            await ctx.send(embed= emb)
            cursor.execute("UPDATE users SET cash = cash + 1250 WHERE id = {}".format(ctx.author.id))	
            connection.commit()
            queue1.append(str(ctx.author.id))
            await asyncio.sleep(12*60)
            queue1.remove(str(ctx.author.id))
            print(f'[Logs:economy] {ctx.author} получил свой ежедневный бонус | {prefix}leaderboard ')
        if str(ctx.author.id) in queue1:
            emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
            await ctx.send(embed= emb)
            print(f'[Logs:economy] {ctx.author} попытался получить свой ежедневный бонус | {prefix}daily ')			
    else:
        await ctx.message.add_reaction('❌')	
        emb = discord.Embed( title = "ОШИБКА❗", colour = discord.Color.red() )

        emb.add_field( name = "Выберите награду!", value = "Fame/Daily")
        emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
        await ctx.send ( embed = emb)
        print(f"[Logs:Error] Необходимо выбрать награду | {prefix}daily")

#Gender selection
#@client.command(aliases = ['gender'])
#async def __gender(ctx, option = None):
#	if option == "Female" or option == "female" or option == "FEMALE" or option == "fEMALE":
#		await ctx.send(f"Вы успешно сменили свой пол на женский")
#		await ctx.message.add_reaction('✅')
#		cursor.execute("UPDATE users SET gender = Female WHERE id = {}".format(ctx.author.id))	
#		connection.commit()
#		print(f'[Logs:Marry] {ctx.author} успешно сменил свой пол на женский')
#	if option == "Male" or option == "male" or option == "MALE" or option == "mALE":
#		await ctx.send(f"Вы успешно сменили свой пол на мужской")
#		await ctx.message.add_reaction('✅')
#		cursor.execute("UPDATE users SET gender = Male WHERE id = {}".format(ctx.author.id))	
#		connection.commit()
#		print(f'[Logs:Marry] {ctx.author} успешно сменил свой пол на мужской')    

#@client.command(aliases = ['genderinfo'])
#async def __genderinfo(ctx):  
#		await ctx.send(embed = discord.Embed(
#			description = f"""Гендер **{ctx.author}** - **{cursor.execute("SELECT gender FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} **"""
#		))	
#=========================INFORMATION=============================
#help
@client.command (aliases=['хелп', 'хЕЛП', 'ХЕЛП', 'Хелп', 'команды', 'Команды', 'КОМАНДЫ', 'кОМАНДЫ', 'commands', 'Commands', 'COMMANDS', 'cOMMANDS', 'HELP', 'hELP', 'Help', 'help'])
async def __help (ctx):
			emb = discord.Embed( title = "**ДОСТУПНЫЕ КОМАНДЫ:**", description = "ВНИМАНИЕ! Сейчас бот только в альфа версии и может работать нестабильно!", colour = discord.Color.red() )

			emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
			emb.add_field( name = "Информация", value = f"`{prefix}хелп` `{prefix}инфо` `{prefix}сервер` `{prefix}профиль` `{prefix}авторы` ", inline=False)
			emb.add_field( name = "Модерирование", value = f"`{prefix}мут` `{prefix}размут` `{prefix}бан` `{prefix}кик` `{prefix}очистить` ", inline=False)
			emb.add_field( name = "Музыка", value = f"`{prefix}плей` `{prefix}видео` `{prefix}скип` `{prefix}очередь` `{prefix}повтор` `{prefix}пауза` `{prefix}продолжить` ", inline=False)
			emb.add_field( name = "Экономика", value = f"`{prefix}баланс` `{prefix}вознаграждение` `{prefix}отнять` `{prefix}добавить-магазин` `{prefix}удалить-магазин` `{prefix}магазин` `{prefix}купить` `{prefix}форбс` `{prefix}daily` `{prefix}+rep`", inline=False)
			emb.add_field( name = "Действие", value = f"`{prefix}рыбалка` `{prefix}сантехник` ", inline=False)
			emb.add_field( name = "Весёлое", value = f"`{prefix}монетка` `{prefix}шар` `{prefix}битва` `{prefix}кнб` `{prefix}лис` `{prefix}кот` `{prefix}пёс` `{prefix}панда` `{prefix}птица` ", inline=False)
			emb.add_field( name = "Утилиты", value = f"`{prefix}аватар` `{prefix}ранд` `{prefix}вики` `{prefix}время` `{prefix}эмоция` `{prefix}вычислить` `{prefix}реверс` `{prefix}транслит` `{prefix}пинг` `{prefix}аналитика` `{prefix}времязапуска`", inline=False)
			emb.add_field( name = "ПОДДЕРЖКА", value = f"Нашли ошибку? \n Обратитесь {settings['CREATOR']} в лс!", inline=False)
			emb.set_thumbnail(url = client.user.avatar_url)
			emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
			await ctx.send ( embed = emb)

			print(f"[Logs:info] Справка по командам была успешно выведена | {prefix}help ")


#bot info
@client.command(aliases = ['ИНФО', 'инфо', 'Инфо', 'иНФО', 'Info', 'info', 'INFO', 'iNFO','Bot', 'bot', 'BOT', 'bOT','БОТ', 'Бот', 'бот', 'бОТ'])
async def __botinfo (ctx):
	emb = discord.Embed( title = f"{ctx.guild.name}", description = "Информация о боте **Aki**.\n Бот был написан специально для проекта Fame Group,\n подробнее о командах - {prefix}help или {prefix}хелп",colour = discord.Color.red() )

	emb.add_field( name = f"**Меня создал:**", value = f"{settings['Creator']}", inline=True)
	emb.add_field( name = f"**Помощь в создании:**", value = "Fsoky#9610", inline=True)
	emb.add_field( name = f"**Лицензия:**", value = "CC BG-SD-HD", inline=True)
	emb.add_field( name = f"**Версия:**", value = "Alpha", inline=True)
	emb.add_field( name = f"**Патч:**", value = "0.9", inline=True)
	emb.set_thumbnail(url = client.user.avatar_url)
	emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )

	await ctx.send ( embed = emb)

	print(f"[Logs:info] Информация о боте была успешно выведена | {prefix}info ")


#Server Info
@client.command(aliases = ['Server', 'server', 'sERVER', 'SERVER', 'Сервер', 'сервер', 'СЕРВЕР', 'сЕРВЕР'])
async def __serverinfo(ctx):
    members = ctx.guild.members
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали: **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион: **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере: **{ctx.guild.member_count}\n\n"
    )

    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = client.user.avatar_url)
    embed.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
    await ctx.send(embed=embed)

    print(f"[Logs:info] Информация о сервере была успешно выведена | {prefix}server ")


#Profile
@client.command(aliases = ['Profile', 'PROFILE', 'pROFILE', 'profile', 'USER', 'user', 'User', 'uSER', 'Профиль', 'профиль', 'пРОФИЛЬ', 'ПРОФИЛЬ', 'Юзер', 'юзер', 'ЮЗЕР', 'юЗЕР'])
async def __profile(ctx):
    roles = ctx.author.roles
    role_list = ""
    for role in roles:
        role_list += f"<@&{role.id}> "
    emb = discord.Embed(title='Profile', colour = discord.Colour.purple())
    emb.set_thumbnail(url=ctx.author.avatar_url)
    emb.add_field(name='Никнэйм', value=ctx.author.mention)
    emb.add_field(name="Активность", value=ctx.author.activity)
    emb.add_field(name='Роли', value=role_list)
    if 'online' in ctx.author.desktop_status:
        emb.add_field(name="Устройство", value=":computer:Компьютер:computer:")
    elif 'online' in ctx.author.mobile_status:
        emb.add_field(name="Устройство", value=":iphone:Телефон:iphone:")
    elif 'online' in ctx.author.web_status:
        emb.add_field(name="Устройство", value=":globe_with_meridians:Браузер:globe_with_meridians:")
    emb.add_field(name="Статус", value=ctx.author.status)
    emb.add_field(name='Id', value=ctx.author.id)
    await ctx.send(embed = emb)

    print(f"[Logs:info] Профиль был успешно выведен | {prefix}profile ")


#Authors 
@client.command(aliases = ["Authors", "AUTHORS", "aUTHORS", 'authors', "Авторы", "авторы", "АВТОРЫ", "аВТОРЫ", "Автор", "АВТОР", "автор", "аВТОР", "Author", "author", "AUTHOR", "aUTHOR"])
async def __authors(ctx):
	emb = discord.Embed( title = "",  colour = discord.Color.red() )
	emb.add_field( name = "Authors", value = "Bot authors | Special thanks :3", inline=False)
	emb.add_field( name = "Creator", value = f"{settings['CREATOR']}", inline=False)
	emb.add_field( name = "Owner", value = f"{settings['OWNER']}", inline=False)
	emb.add_field( name = "Special thanks [Support Server]", value = "Fsoky`s Fun Community", inline=False)
	emb.set_thumbnail(url = client.user.avatar_url)
	emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
	await ctx.send( embed = emb )
	print(f"[Logs:info] Информация о создателях бота была выведена | {prefix}author")


#=========================MODERATION===============================
#Clear message
@client.command( aliases = ["Очистить", "очистить", "оЧИСТИТЬ", "ОЧИСТИТЬ", "Clear", 'clear', "cLEAR", "CLEAR"])
@commands.has_permissions( administrator = True )
async def __clear (ctx, amount : int):
	await ctx.channel.purge ( limit = amount)

	await ctx.message.add_reaction('✅')
	print(f"[Logs:moderation] {amount} сообщения было очищено | {prefix}clear ")


#Kick
@client.command(aliases = ["кик", "Кик", "кИК", "КИК", "Kick", "kICK", "KICK", 'kick'])
@commands.has_permissions ( administrator = True )
async def __kick(ctx, member: discord.Member, *, reason = None):
    await ctx.message.add_reaction('✅')
    await member.kick( reason = reason )
    reason = reason
    emb = discord.Embed( title = 'kick', description = f'Пользователь {member}  был кикнут по причине { reason } ', colour = discord.Color.red() )
    emb.set_author( name = client.user.name )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.set_thumbnail(url = client.user.avatar_url)

    await ctx.send( embed = emb )	

    print(f'[Logs:moderation] Пользователь {member} был кикнут по причине {reason} | {prefix}kick ')


#Ban
@client.command (aliases = ["Ban", "bAN", 'BAN', 'ban', "Бан", "бан", "бАН", 'БАН', ])
@commands.has_permissions ( administrator = True )
async def __ban(ctx, member: discord.Member, *, reason = None):
	await ctx.message.add_reaction('✅')
	emb = discord.Embed ( title = f'**Команда** "{prefix}бан" ', description =f"Изгнать участника с сервера и заблокировать", colour = discord.Color.red() )
	await member.ban ( reason = reason )
	emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
	emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
	emb.add_field(name = "Ban" , value = f"Пользователь {member} был успешно заблокирован" )
	emb.set_thumbnail( url = "https://d2gg9evh47fn9z.cloudfront.net/800px_COLOURBOX21145683.jpg")

	await member.send("Вы были заблокированы на сервере **Fame Group**")

	await ctx.send (embed = emb)  

	print(f'[Logs:moderation] Пользователь {member} был заблокирован | {prefix}ban ')


#Unban
@client.command (aliases = ["Unban", "uNBAN", 'UNBAN', 'unban',"Разбан", "разбан", "рАЗБАН", 'РАЗБАН'])
@commands.has_permissions ( administrator = True )
async def __unban(ctx, *, member):
	await ctx.message.add_reaction('✅')
	emb = discord.Embed ( title = " ", colour = discord.Color.red() )
	banned_users = await ctx.guild.bans()
	#получаем список забаненных

	for ban_entry in banned_users:
		user = ban_entry.user
		# получаем имя забаненного

		await ctx.guild.unban ( user )

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
		emb.set_footer(text = "Разблокирован администратором {}".format (ctx.author.name), icon_url = ctx.author.avatar_url)
		emb.add_field(name = "Unban" , value = f"Пользователь {user.mention} был успешно разблокирован" )
		emb.set_thumbnail( url = "https://icons.iconarchive.com/icons/elegantthemes/beautiful-flat-one-color/128/unlocked-icon.png")

		await member.send("Вы были разблокированы на сервере **Fame Group**")

		await ctx.send (embed = emb)
		return	  

		print(f'[Logs:moderation] Пользователь {member} был разблокирован | {prefix}unban ')


#Mute
@client.command(aliases = ["Mute", "mUTE", 'mute', 'МУТ', "Мут", "мут", "мУТ", "Мьют", 'МЬЮТ' "мьют", "мЬЮТ"])
@commands.has_permissions ( administrator = True )
async def __mute (ctx, member: discord.Member):
	await ctx.message.add_reaction('✅')
	mute_role = discord.utils.get(ctx.message.guild.roles, name = "U will Muted") #НАЗВАНИЕ РОЛИ

	emb = discord.Embed ( title = " ", colour = discord.Color.red())

	await member.add_roles( mute_role)
	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	emb.set_footer(text = "Замучен администратором {}".format (ctx.author.name), icon_url = ctx.author.avatar_url)
	emb.add_field(name = "Mute" , value = f"Пользователь {member} был успешно замучен" )
	emb.set_thumbnail( url = "https://steamuserimages-a.akamaihd.net/ugc/843713701094802199/4D212FF3423CFA0C2D1D484D984BBB21ACD934C6/")

	await member.send("Вы были замучены на сервере **Fame Group**")

	await ctx.send( embed = emb )

	print(f'[Logs:moderation] Пользователь {member} был замучен | {prefix}mute ')


#Unmute	
@client.command(aliases = ["Unmute", "uNMUTE", 'UNMUTE', 'unmute', "Анмут", "анмут", "АНМУТ", 'аНМУТ', "Анмьют", "анмьют", "аНМЬЮТ", 'АНМЬЮТ'])
@commands.has_permissions ( administrator = True )
async def __unmute (ctx, member: discord.Member):
	await ctx.message.add_reaction('✅')
	unmute_role = discord.utils.get(ctx.message.guild.roles, name = "U will Muted") #НАЗВАНИЕ РОЛИ 
	await member.remove_roles( unmute_role)

	emb = discord.Embed ( title = " ", colour = discord.Color.red())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	emb.set_footer(text = "Размучен администратором {}".format (ctx.author.name), icon_url = ctx.author.avatar_url)
	emb.add_field(name = "Mute" , value = f"Пользователь {member} был успешно размучен" )
	emb.set_thumbnail( url = "https://steamuserimages-a.akamaihd.net/ugc/843713701094802199/4D212FF3423CFA0C2D1D484D984BBB21ACD934C6/")

	await member.send("Вы были размучены на сервере **Fame Group**")

	await ctx.send( embed = emb )

	print(f'[Logs:moderation] Пользователь {member} был размучен | {prefix}unmute ')


#=========================UTILITIES===============================
#Avatar
@client.command(aliases = ['Avatar', 'AVATAR', 'aVATAR', 'avatar', 'Ava', 'ava', 'AVA', 'aVA', 'Ава', 'АВА', 'ава', 'аВА', 'аВАТАР', 'АВАТАР', 'Аватар', 'аватар'])
async def __avatar(ctx, member : discord.Member = None):

	user = ctx.message.author if (member == None) else member

	embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)

	embed.set_image(url=user.avatar_url)

	await ctx.send(embed=embed)

	print(f'[Logs:utils] Аватарка пользователя {member} была выведена | {prefix}avatar ')


#random number
@client.command(aliases = ['рандом','РАНДОМ', "Рандом", "рАНДОМ", 'Ранд','РАНД', 'ранд', "рАНД", "Random", "RANDOM", 'rANDOM', 'random'])
async def __число(ctx, count=None):
	if count == None:
		emb = discord.Embed(description=f'Пример использования: `{prefix}ранд 5` - выведу рандомное число от 1 до 5 .', color=discord.Color.red())
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
		await ctx.send( embed = emb )
		print(f'[Logs:utils] Максимальное число не было указано | {prefix}random ')
	else:
		try:
			await ctx.send(str(random.randint(int(1), int(count))))
			print(f'[Logs:utils] Случайное число было успешно сгенерировано, оно равняется == [{str(random.randint(int(1), int(count)))}] | {prefix}random ')
		except ValueError:
			msg = await ctx.send(embed=discord.Embed(description='В аргументах присутствуют сторонние символы!', color=discord.Color.orange()))
			print(f'[Logs:error] В аргументах присутствуют сторонние символы | {prefix}random')

#time
@client.command (aliases = ["Time","tIME", 'time', "TIME", "Время", "время", "вРЕМЯ", "ВРЕМЯ", "Тайм", "тайм", "тАЙМ", "ТАЙМ"])
async def __time( ctx):


	clock_dt = datetime.datetime.now()
	time_clock = (f"{ clock_dt.hour }{ clock_dt.minute }")

	time_clock = float(datetime.datetime.strptime(time_clock, '%H%M').strftime('%I.%M').lower())
	print(f"[Logs:utils] Вывожу время | {prefix}time")
	print(f"[")

	table_clock = clock.diff
	result_clock = table_clock.get(time_clock, table_clock[min(table_clock.keys(), key=lambda k: abs(k-time_clock))])


	emb = discord.Embed( title = "Время онлайн", description = "Текущее время по МСК", colour = discord.Color.green(), url = "https://time100.ru/" )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
	print("	[Logs:utils:timeclock:paste.image] - добавление картинки")
	emb.set_thumbnail( url = str(result_clock) ) #clock.image_url().url

	dt = datetime.datetime.now()
	data = (f"{ dt.day }.{ dt.month }.{ dt.year }")
	time = (f"{ dt.hour }:{ dt.minute }")

	emb.add_field( name = f"Дата: { data }", value = f"Время: { time }" )
	print(f"	[Logs:utils:timeclock] - время: { time }")

	await ctx.send( embed = emb )
	print(f']')
	

#wiki
@client.command(aliases = ["Вики", "вики", "ВИКИ", 'вИКИ', 'Wiki', 'WIKI', 'wIKI', 'wiki'])
async def __wiki(ctx, *, text=None):
	if text == None:
		emb = discord.Embed(title = f"**Команда `{prefix}вики`**", description = "Найдите интересующую вас вещь на WIKIPEDIA")
		emb.add_field( name = 'Использование', value = f"{prefix}вики <Наименование>", inline=False)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
		await ctx.send(embed=emb)
		print(f"[Logs:utils] Необходимо ввести предмет поиска | {prefix}wiki")
	else:
		wikipedia.set_lang("ru")
		new_page = wikipedia.page(text)
		summ = wikipedia.summary(text)
		emb = discord.Embed(
			title= new_page.title,
			description= summ,
			color = 0x00ffff
		)
		emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
		await ctx.send(embed=emb)

		print(f"[Logs:utils] Информация о {text} была выведена | {prefix}wiki")


#emoji for messages
@client.command(aliases = ['Emoji', 'EMOJI', 'eMOJI', 'emoji', 'Емоджи', 'емоджи', 'ЕМОДЖИ', 'еМОДЖИ', 'эмоция', 'Эмоция', 'эМОЦИЯ', 'ЭМОЦИЯ'])
@commands.has_permissions ( administrator = True )
async def __emoji(ctx,id:int,reaction:str):
		await ctx.message.delete()
		message = await ctx.message.channel.fetch_message(id)
		await message.add_reaction(reaction)
		print(f"[Logs:utils] К сообщению [{id}] была добавлена эмоджи | {prefix}emoji")


#ping
@client.command(aliases = ['Ping', 'PING', 'pING', 'ping','Пинг', 'пинг', 'ПИНГ', 'пИНГ', 'Понг', 'понг', 'пОНГ', 'ПОНГ'])
async def __ping(ctx):
	ping = client.ws.latency

	ping_emoji = "🟩🔳🔳🔳🔳"

	if ping > 0.10000000000000000:
		ping_emoji = "🟧🟩🔳🔳🔳"

	if ping > 0.15000000000000000:
		ping_emoji = "🟥🟧🟩🔳🔳"

	if ping > 0.20000000000000000:
		ping_emoji = "🟥🟥🟧🟩🔳"

	if ping > 0.25000000000000000:
		ping_emoji = "🟥🟥🟥🟧🟩"

	if ping > 0.30000000000000000:
		ping_emoji = "🟥🟥🟥🟥🟧"

	if ping > 0.35000000000000000:
		ping_emoji = "🟥🟥🟥🟥🟥"

	message = await ctx.send("Пожалуйста, подождите. . .")
	await message.edit(content = f"Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:")
	print(f"[Logs:utils] Пинг сервера был выведен | {prefix}ping")
	print(f"[Logs:utils] На данный момент пинг == {ping * 1000:.0f}ms | {prefix}ping")

#timeup
startTime = time.time()

@client.command(aliases = ['timeup', 'TIMEUP', 'tIMEUP', 'Timeup', 'времязапуска', 'Времязапуска', 'ВРЕМЯЗАПУСКА', 'вРЕМЯЗАПУСКА'])
async def __timeup(ctx):
	timeUp = time.time() - startTime
	hoursUp = round(timeUp) // 3600
	timeUp %= 3600
	minutesUp = round(timeUp) // 60
	timeUp = round(timeUp % 60)
	msg = "Бот запустился: **{0}** час. **{1}** мин. **{2}** сек. назад :alarm_clock: ".format(hoursUp, minutesUp, timeUp)
	await ctx.send(f"{msg}")    
	print(f"[Logs:utils] Информация о времени запуска бота выведена | {prefix}timeup")
	print(f"[Logs:utils] {msg} | {prefix}timeup")


@client.command(aliases = ['транслит', 'Транслит', 'ТРАНСЛИТ', 'тРАНСЛИТ', 'Translit', 'translit', 'TRANSLIT', 'tRANSLIT'])
async def __translit(ctx,*,message=None):
  a = {"q":"й","w":"ц","e":"у","r":"к","t":"е","y":"н","u":"г","i":"ш","o":"щ","p":"з","[":"х","{":"х","}":"ъ","]":"ъ","a":"ф","s":"ы","d":"в","f":"а","g":"п","h":"р","j":"о","k":"л","l":"д",":":"ж",";":"ж",'"':"э","'":"э","z":"я","x":"ч","c":"с","v":"м","b":"и","n":"т","m":"ь","<":"б",",":"б",">":"ю",".":"ю","?":",","/":".","`":"ё","~":"ё"," ":" "}
  if message is None:
    await ctx.send("Введите сообщение!")
    print(f'[Logs:utils] Аргументы не были введены | {prefix}translit')
  else:
    itog = ""
    errors = ""
    for i in message:
      if i.lower() in a:
        itog += a[i.lower()]
      else:
        errors += f"`{i}` "
    if len(errors) <= 0:
      errors_itog=""
    else:
      errors_itog=f"\nНепереведенные символы: {errors}"
      print(f"[Logs:utils] [Warning] Перевод содержит непереводимые символы | {prefix}translit")

    if len(itog) <= 0:
      itog_new= "Перевода нет!"
      print(f"[Logs:utils] [Error] Не удалось перевести сообщение | {prefix}translit")
    else:
      itog_new=f"Перевод: {itog}"
      print(f"[Logs:utils] Команда была успешно использована | {prefix}translit")
    await ctx.send(f"{itog_new}{errors_itog}")	


@client.command(aliases = ['Reverse', 'reverse', 'REVERSE', 'rEVERSE', 'Реверс', 'реверс', 'РЕВЕРС', 'рЕВЕРС'])
async def __reverse(ctx, *, text: str):

    t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    print(f"[Logs:utils] Команда была успешно использована | {prefix}reverse")
    await ctx.send(f"{t_rev}")    

async def bytes2human(number, typer=None):
    # Пример Работы Этой Функции перевода чисел:
    # >> bytes2human(10000)
    # >> '9.8K'
    # >> bytes2human(100001221)
    # >> '95.4M'

    if typer == "system":
        symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')  # Для перевода в Килобайты, Мегабайты, Гигобайты, Террабайты, Петабайты, Петабайты, Эксабайты, Зеттабайты, Йоттабайты
    else:
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')  # Для перевода в обычные цифры (10k, 10MM)

    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if number >= prefix[s]:
            value = float(number) / prefix[s]
            return '%.1f%s' % (value, s)

    return f"{number}B"

def bytes2human(number, typer=None):
    if typer == "system":
        symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')  # Для перевода в Килобайты, Мегабайты, Гигобайты, Террабайты, Петабайты, Петабайты, Эксабайты, Зеттабайты, Йоттабайты
    else:
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')  # Для перевода в обычные цифры (10k, 10MM)

    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if number >= prefix[s]:
            value = float(number) / prefix[s]
            return '%.1f%s' % (value, s)

    return f"{number}B"

@client.command(aliases = ['analytics', 'Analytics', 'ANALYTICS', 'aNALYTICS', 'Аналитика', 'аналитика', 'АНАЛИТИКА', 'аНАЛИТИКА'])
async def __analytics(ctx):
	mem = ps.virtual_memory()
	ping = client.ws.latency

	ping_emoji = "🟩🔳🔳🔳🔳"
	ping_list = [
		{"ping": 0.00000000000000000, "emoji": "🟩🔳🔳🔳🔳"},
		{"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
		{"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
		{"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
		{"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
		{"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
		{"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}
	]
	for ping_one in ping_list:
		if ping <= ping_one["ping"]:
			ping_emoji = ping_one["emoji"]
			break	

	emb=discord.Embed(title="Нагрузка бота")
	emb.add_field(name='Использование CPU',
						value=f'В настоящее время используется: {ps.cpu_percent()}%',
						inline=True)
	emb.add_field( name = 'Использование RAM', value = f'Доступно: {bytes2human(mem.available, "system")}\n'
								f'Используется: {bytes2human(mem.used, "system")} ({mem.percent}%)\n'
								f'Всего: {bytes2human(mem.total, "system")}',inline=True)
	emb.add_field(name='Пинг Бота',
						value=f'Пинг: {ping * 1000:.0f}ms\n'
							f'`{ping_emoji}`',
						inline=True)																	
	emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
	await ctx.send( embed = emb )
	print(f"[Logs:info] Информация о нагрузке была выведена | {prefix}analytics")  
#embed.set_footer(text=f"{round(virtual_memory().used /1024/1024/1024, 2)} GB out of {round(ram /1024/1024/1024, 2)} GB")
#===========================MUSIC=================================
# Join in voice chat
@client.command(aliases=['J', 'j', 'JOIN', 'Join', 'jOIN', 'join', 'ПОДКЛЮЧИТЬСЯ', 'Подключиться', 'пОДКЛЮЧИТЬСЯ', 'подключиться'])
async def __join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        return await voice.move_to(channel)
        print(f"[Logs:music] Бот переподключился к каналу [{channel}]| {prefix}join")
    else:
        await channel.connect()
        await ctx.message.add_reaction('✅')
        print(f"[Logs:music] Бот подключился к каналу [{channel}]| {prefix}join")


# Leave with voice chat
@client.command(aliases=['отключиться', 'ОТКЛЮЧИТЬСЯ', 'Отключиться', 'оТКЛЮЧИТЬСЯ', 'L', 'l', 'Leave', 'lEAVE', 'leave', 'LEAVE'])
async def __leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"[Logs:music] Бот отключился от канала [{channel}]| {prefix}leave")
        await ctx.message.add_reaction('✅')
    else:
        print(f"[Logs:music:] [Error] Бот не находится не в одном голосовом канале | {prefix}leave")
        await ctx.send("Эй!Я не нахожусь не в одном голосовм канале!")


#Old player (Creating a new!!!)
@client.command(aliases=['play','PLAY', 'Play', 'pLAY','плей', 'ПЛЕЙ', 'Плей','пЛЕЙ'])
async def __play(ctx, url: str):
	song_there = os.path.isfile("song.mp3")

	try:
		if song_there:
			os.remove("song.mp3")
			print(f"[Logs:music] [OS] Старый файл был удалён | {prefix}play")
	except PermissionError:
		print(f"[Logs:music] [OS] Не удалось удалить старый файл | {prefix}play")

	await ctx.send("Пожалуйста ожидайте")

	voice = get(client.voice_clients, guild = ctx.guild)

	ydl_opts = {
		"format" : "bestaudio/best",
		"postprocessors" : [{
			"key" : "FFmpegExtractAudio",
			"preferredcodec" : "mp3",
			"preferredquality" : "192"
		}]
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print(f"[Logs:music] [Downloading] Загрузка музыки... | {prefix}play")
		ydl.download([url])

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			name = file
			print(f"[Logs:music] [OS] Переименование... | {prefix}play")
			os.rename(file, "song.mp3")

	voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print(f"[Logs:music] {name}, музыка закончила свое проигрывание"))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	song_name = name.rsplit("-", 2)
	await ctx.send(f"Сейчас проигрывается музыка: {song_name[0]}")


#PAUSE
@client.command(aliases=['PAUSE', 'Pause', 'pAUSE', 'pause', 'пауза','ПАУЗА', 'пАУЗА', 'Пауза'])
async def __pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print(f"[Logs:music] Музыка поставлена на паузу | {prefix}pause")
        voice.pause()
        await ctx.send("Музыка была поставлена на паузу")
    else:
        print(f"[Logs:music] [Error] Бот не проигрывает музыку | {prefix}pause")
        await ctx.send("Ошибка! Бот не проигрывает музыку")


#RESUME       
@client.command(aliases=['продолжить', 'ПРОДОЛЖИТЬ', 'Продолжить', 'пРОДОЛЖИТЬ', 'RESUME', 'resume', 'Resume', 'rESUME'])
async def __resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print(f"[Logs:music] Музыка продолжила своё проигрывание | {prefix}resume")
        voice.resume()
        await ctx.send("Музыка продолжила своё проигрывание")
    else:
        print(f"[Logs:music] [Error] Музыка не находится на паузе | {prefix}resume")
        await ctx.send("Ошибка! Музыка не находится на паузе")  


#STOP
@client.command(aliases=['STOP', 'Stop', 'sTOP', 'stop', 'Остановить', 'остановить',  'оСТАНОВИТЬ', 'ОСТАНОВИТЬ'])
async def __stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print(f"[Logs:music] Проигрывание музыки прервано | {prefix}stop")
        voice.stop()
        await ctx.send("Проигрывание музыки прервано")
    else:
        print(f"[Logs:music] [Error] Сейчас не проигрывается музыка | {prefix}stop")
        await ctx.send("Ошибка! Сейчас не проигрывается музыка")   

               
#repeat
@client.command(aliases=['REPEAT', 'Repeat', 'rEPEAT', 'repeat', 'Повтор', 'повтор', 'пОВТОР', 'ПОВТОР'])
async def __repeat (ctx):
	print(f"[Logs:music] Повтор песни: {song_name[0]} включен | {prefix}repeat")
	song_this = os.path.isfile("song.mp3")

	voice = get(client.voice_clients, guild = ctx.guild)
	for file in range(100):
		voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print(f"[logs] музыка закончила свое проигрывание"))
		voice.source = discord.PCMVolumeTransformer(voice.source)
		voice.source.volume = 0.07

	await ctx.send(f"Повтор песни: {song_name[0]} включен")


#video with youtube.com
@client.command(aliases=['видео', 'search', 'поиск', 'ПОИСК', 'SEARCH', 'VIDEO', 'ВИДЕО', 'Видео', 'Search', 'sEARCH','вИДЕО','Поиск', 'пОИСК', 'Video', 'vIDEO'])
async def video(ctx, title=None):
    if not title:
        await ctx.send('Напишите какое видео вы хотите посмотреть')
        print(f"[Logs:music] [Error] Название видео не было указано | {prefix}video")
    else:
        mas = []
        emb = discord.Embed(title='YouTube', colour=discord.Color.red())
        sq = f'https://www.youtube.com/results?search_query={quote(title)}&sp=EgIQAQ%253D%253D'# quote приабразуем удобочитаемасть для адресной строки
        doc = urllib.request.urlopen(sq).read().decode('cp1251', errors='ignore')
        match = re.findall(r"\?v\=(.+?)\"", doc)# Ищем на стронички все эти символы
        if not(match is None):#Если мы нашли
            for ii in match:
                if (len(ii) < 25):#25 потомучто в строке поиска ютуба максимму 25 символов
                    mas.append(ii)
    
    
        mas = dict(zip(mas, mas)).values()#Очищаем од дублей
        mas2 = []
        for y in mas:
            mas2.append({
                'href': f'https://www.youtube.com/watch?v={y}'
                })
        i = 1
        for item in mas2:
            emb.add_field(name=f'Ссылка номер {i}', value=f'Ccылка: {item["href"]}')
            if i == 5:
                await ctx.send(embed=emb)
            i += 1 

        print(f"[Logs:music] Ссылка на видео была выведена | {prefix}video")

#===========================FUNNY=================================
#dog
@client.command(aliases=['DOG', 'Dog', 'dOG', 'dog', 'ПЁС', 'пёс', 'Пёс', 'пЁС', "Пес", 'ПЕС', 'пес', 'пЕС'])
async def __dog( ctx ):
	response = requests.get('https://api.thedogapi.com/v1/images/search')
	json_data = json.loads(response.text)
	url = json_data[0]['url']

	embed = discord.Embed(color = 0xff9900)
	embed.set_image( url = url )

	await ctx.send( embed = embed )

	print(f"[Logs:funny] Картинка с собакой была выведена | {prefix}dog")


#cat
@client.command(aliases = ['Cat', 'CAT', 'cAT', 'cat', 'Кот', 'кот', 'КОТ', 'кОТ'])
async def __cat( ctx ):
	response = requests.get('https://api.thecatapi.com/v1/images/search')
	json_data = json.loads(response.text)
	url = json_data[0]['url']

	embed = discord.Embed(color = 0xff9900)
	embed.set_image( url = url )

	await ctx.send( embed = embed )

	print(f"[Logs:funny] Картинка с кошкой была выведена | {prefix}cat")


#fox
@client.command(aliases = ['Fox', 'FOX', 'fOX', 'fox', 'ЛИС', 'Лис', 'лис', 'лИС'])
async def __fox( ctx ):
	num = random.randint(1, 122)

	embed = discord.Embed(color = 0xff9900)
	embed.set_image( url = f'https://randomfox.ca/images/{num}.jpg' )

	await ctx.send( embed = embed )

	print(f"[Logs:funny] Картинка с лисой была выведена | {prefix}fox")

#panda
@client.command(aliases = ['Панда', 'панда', 'ПАНДА','пАНДА', 'Panda', 'PANDA', 'pANDA', 'panda'])
async def __panda( ctx ):
	response = requests.get('https://some-random-api.ml/img/panda')
	jsoninf = json.loads(response.text)
	url = jsoninf['link']
	embed = discord.Embed(color = 0xff9900)
	embed.set_image(url = url)
	await ctx.send(embed = embed)

	print(f"[Logs:funny] Картинка с пандой была выведена | {prefix}panda")

#bird
@client.command(aliases = ['Птица', 'птица', 'ПТИЦА', 'пТИЦА', 'Bird', 'BIRD', 'bIRD', 'bird'])
async def __bird( ctx ):
	response = requests.get('https://some-random-api.ml/img/birb')
	jsoninf = json.loads(response.text)
	url = jsoninf['link']
	embed = discord.Embed(color = 0xff9900)
	embed.set_image(url = url)
	await ctx.send(embed = embed)

	print(f"[Logs:funny] Картинка с птицей была выведена | {prefix}bird")

#rock paper scissors
@client.command( aliases=['RPS', 'Rps', 'rPS', 'rps', 'КНБ', 'Кнб', 'кНБ', 'кнб'])
async def __rps(ctx, *, mess):
	robot = ['Камень', 'Ножницы', 'Бумага']
	print(f"[Logs:funny] Игра в камень ножницы бумага была начата | {prefix}rps")
	if mess == "Камень" or mess == "К" or mess == "камень" or mess == "к":
		robot_choice = random.choice(robot)
		emb = discord.Embed(title = robot_choice, colour = discord.Colour.lighter_grey())
		if robot_choice == 'Ножницы':
			emb.add_field(name = '✂', value = 'Вы выиграли!')
			print(f"[Logs:funny] Камень победил | {prefix}rps")
		elif robot_choice == 'Бумага':
			emb.add_field(name = '📜', value = 'Вы проиграли :с')
			print(f"[Logs:funny] Победила бумага | {prefix}rps")
		else:
			emb.add_field(name = '🗿', value = 'Ничья!')
			print(f"[Logs:funny] Победила дружба | {prefix}rps")
		await ctx.send(embed = emb)

	elif mess == "Бумага" or mess == "Б" or mess == "бумага" or mess == "б":
		robot_choice = random.choice(robot)
		emb = discord.Embed(title = robot_choice, colour = discord.Colour.lighter_grey())
		if robot_choice == 'Ножницы':
			emb.add_field(name = '✂', value = 'Вы проиграли :с')
			print(f"[Logs:funny] Ножницы победили | {prefix}rps")
		elif robot_choice == 'Камень':
			emb.add_field(name = '🗿', value = 'Вы выиграли!')
			print(f"[Logs:funny] Победила бумага | {prefix}rps")
		else:
			emb.add_field(name = '📜', value = 'Ничья!')
			print(f"[Logs:funny] Победила дружба | {prefix}rps")
		await ctx.send(embed = emb)
            
	elif mess == "Ножницы" or mess == "Н" or mess == "ножницы" or mess == "н":
		robot_choice = random.choice(robot)
		emb = discord.Embed(title = robot_choice, colour = discord.Colour.lighter_grey())
		if robot_choice == 'Бумага':
			emb.add_field(name = '📜', value = 'Вы выиграли!')
			print(f"[Logs:funny] Ножницы победили | {prefix}rps")
		elif robot_choice == 'Камень':
			emb.add_field(name = '🗿', value = 'Вы проиграли :с')
			print(f"[Logs:funny] Камень победил | {prefix}rps")
		else:
			emb.add_field(name = '✂', value = 'Ничья!')
			print(f"[Logs:funny] Победила дружба | {prefix}rps")
		await ctx.send(embed = emb)


# 8ball
@client.command(aliases = ["8ball", '8BALL', '8Ball', 'Ball', 'ball', 'BALL', 'bALL', 'Шар', 'ШАР', 'шар', 'шАР' ])
async def __ball(ctx, *, arg):

	message = ['Нет','Да','Возможно','Опредленно нет', 'Точно нет'] 
	s = random.choice( message )
	await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0x0c0c0c))
	print(f"[Logs:funny] Пользователь [{ctx.author}] попытался узнать свою судьбу | {prefix}8ball")
	return           
	


# coin
@client.command(aliases = ['Монетка', 'МОНЕТКА', 'монетка','мОНЕТКА', 'coin', 'COIN', 'Coin', 'cOIN'])
async def __coin( ctx, title = None ):
	if not title:
		print(f"[Logs:funny] Монетка была подброшена | {prefix}coin")
		a = random.randint(1,2)
		if a == 1:
			emb = discord.Embed( title = "",  colour = discord.Color.red() )
			emb.add_field( name = f"{ctx.author.name} подкинул монетку", value = "Орел :eagle:", inline=False)
			await ctx.send( embed = emb )
			print(f"[Logs:funny] Выпал орёл | {prefix}coin")

		if a == 2:
			emb = discord.Embed( title = "",  colour = discord.Color.red() )
			emb.add_field( name = f"{ctx.author.name} подкинул монетку", value = "Решка :full_moon:", inline=False)
			await ctx.send( embed = emb )
			print(f"[Logs:funny] Выпала решка | {prefix}coin")


#battle
@client.command(aliases = ["Дуэль", "дуэль", "ДУЭЛЬ", "дУЭЛЬ", "битва", "Битва", "БИТВА", "бИТВА", "Battle", 'BATTLE', "bATTLE", 'battle'])
async def __battle( ctx, member: discord.Member = None ):
    if member is None:
        await ctx.send('С кем ты хочешь перестреляться !')
        print(f"[Logs:funny] [Error] Соперник не был выбран | {prefix}battle")
    else:
        a = random.randint(1,2)
        if a == 1:
            emb = discord.Embed( title = f"Победитель - {ctx.author}", color = discord.Color.red())
            emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
            await ctx.send( embed = emb )
            print(f"[Logs:funny] В перестрелке победил {ctx.author} | {prefix}battle")

        elif member.id == ctx.author.id:
            emb = discord.Embed( title = f"Вы не можете с собой сражаться !", color = discord.Color.red())
            emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
            await ctx.send( embed = emb )
            print(f"[Logs:funny] [Error] Пользователь [{ctx.author}] попытался постреляться с самим собой | {prefix}battle")

        else:
            emb = discord.Embed( title = f"Победитель - {member}", color = discord.Color.red())
            emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
            await ctx.send( embed = emb )
            print(f"[Logs:funny] В перестрелке победил {member} | {prefix}battle")

#=================ROLE=PLAY==================#
#fishing
@client.command(aliases = ["Fishing", "FISHING", "fISHING", 'fishing',"Рыбалка", "рыбалка", "РЫБАЛКА", "рЫБАЛКА"])
async def __fishing(ctx, *, mess):
    print(f"[Logs:roleplay] Пользователь [{ctx.author}] начал рыбалку | {prefix}fishing")
    robot_lakes = ['судака', 'карася', 'карпа', 'щуку', 'толстолобика','линь','белого амура','окуня','плотву','убежала','сорвалась']
    robot_rivers = ['сорога', 'хариуса', 'щуку', 'налима', 'пескаря', 'леща', 'сома', 'ерша', 'окуня','краснопёрку','язя','убежала','сорвалась']
    robot_oceans = ['палтуса', 'терпугу', 'осетра', 'бонита', 'барракуду', 'шэда', 'лосося', 'чавычу', 'нерку','горбушу','форель','мальму','убежала','сорвалась']
    rand = random.randint(200, 1100)
    if mess == "озеро" or mess == "Озеро" or mess == "ОЗЕРО" or mess == "оЗЕРО" or mess == "lake" or mess == "Lake" or mess == "lAKE" or mess == "LAKE":
        robot_choice = random.choice(robot_lakes)
        message = await ctx.send(f'`{ctx.author.name} закинул удочку в озеро!`')
        await asyncio.sleep(2)
        await message.edit(content = f'`Наконец-то клюет!` :fishing_pole_and_fish: ')
        await asyncio.sleep(2)
        if robot_choice == 'судака' or robot_choice == 'карася' or robot_choice == 'карпа' or robot_choice == 'щуку' or robot_choice == 'толстолобика' or robot_choice == 'линь' or robot_choice == 'белого амура' or robot_choice == 'окуня' or robot_choice == 'плотву':
            await ctx.send(f'`Вы поймали {robot_choice}! Продано за: {rand}$` :fish:')
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
            connection.commit()
        elif robot_choice == 'убежала' or robot_choice == 'сорвалась':
            await ctx.send(f'`Увы, рыба {robot_choice}!` :wastebasket:')  
    if mess == "река" or mess == "Река" or mess == "РЕКА" or mess == "рЕКА" or mess == "River" or mess == "RIVER" or mess == "river" or mess == "rIVER":
        robot_choice = random.choice(robot_rivers)
        message = await ctx.send(f'`{ctx.author.name} закинул удочку в реку!`')
        await asyncio.sleep(3) 
        await message.edit(content = f'`Наконец-то клюет!` :fishing_pole_and_fish: ')
        await asyncio.sleep(2)
        if robot_choice == 'сорога' or robot_choice == 'хариуса' or robot_choice == 'щуку' or robot_choice == 'налима' or robot_choice == 'пескаря' or robot_choice == 'леща' or robot_choice == 'сома' or robot_choice == 'ерша' or robot_choice == 'окуня' or robot_choice == 'краснопёрку' or robot_choice == 'язя':
            await ctx.send(f'`Вы поймали {robot_choice}! Продано за: {rand}$` :fish:')
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
            connection.commit()
        elif robot_choice == 'убежала' or robot_choice == 'сорвалась':
            await ctx.send(f'`Увы, рыба {robot_choice}!` :wastebasket:')  
    if mess == "море" or mess == "Море" or mess == "МОРЕ" or mess == "мОРЕ" or mess == "Ocean" or mess == "OCEAN" or mess == "ocean" or mess == "oCEAN":
        robot_choice = random.choice(robot_oceans)
        message = await ctx.send(f'`{ctx.author.name} закинул удочку в море!`')
        await asyncio.sleep(3) 
        await message.edit(content = f'`Наконец-то клюет!` :fishing_pole_and_fish: ')
        await asyncio.sleep(2)
        if robot_choice == 'палтуса' or robot_choice == 'терпугу' or robot_choice == 'осетра' or robot_choice == 'бонита' or robot_choice == 'барракуду' or robot_choice == 'шэда' or robot_choice == 'лосося' or robot_choice == 'чавычу' or robot_choice == 'нерку' or robot_choice == 'горбушу' or robot_choice == 'форель' or robot_choice == 'мальму':
            await ctx.send(f'`Вы поймали {robot_choice}! Продано за: {rand}$` :fish:')
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
            connection.commit()
        elif robot_choice == 'убежала' or robot_choice == 'сорвалась':
            await ctx.send(f'`Увы, рыба {robot_choice}!` :wastebasket:')  


@client.command(aliases = ['Электрик', 'электрик', 'ЭЛЕКТРИК', 'эЛЕКТРИК', 'electric', 'eLECTRIC', 'Electric', 'ELECTRIC'])
async def __electric(ctx):
  #делаем переменную rand и рандомное число
    rand = random.randint(300, 1200)
  #для разнообразия я решил сделать несколько вариантов сообщения по зарплату
    if rand > 400:
        await ctx.send(f"Ты плохо поработал и заработал всего лишь {rand} :moneybag: ")
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
        connection.commit()
    elif rand > 600:
        await ctx.send(f"Ты неплохо поработал сантехником и заработал {rand} :moneybag: ")
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
        connection.commit()
    elif rand > 800:
        await ctx.send(f"Ого, ты усердно поработал и заработал {rand} :moneybag: ")
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
        connection.commit()
    elif rand > 1000:
        await ctx.send(f"Ты очень хорошо поработал и заработал всего лишь {rand} :moneybag: ")
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
        connection.commit()
    elif rand > 1200:
        await ctx.send(f"Ты блестяще поработал сантехником и заработал всего лишь {rand} :moneybag: ")
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(rand, ctx.author.id))
        connection.commit()
	
#======================FOR==ADMINISTARION=========================#
#Команда на смену статуса (Играет в ...) 
@client.command( aliases = ['Statgames', 'STATGAMES', 'sTATGAMES', 'statgames', 'ИГРАЕТ В', 'играет в', 'Играет в', 'иГРАЕТ В'])
@commands.is_owner()
async def __statgames(ctx, *, arg):
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
        print(f"[Logs:admincmd] [Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался сменить префикс бота | {prefix}statgames")
    else:
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.streaming))
        await ctx.send("Изменяем...")
        await ctx.send("Статус бота изменен!")
        print(f"[Logs:admincmd] Префикс бота был успешно сменен на играет в {arg} | {prefix}statgames")


#Команда на смену статуса (Смотрит ...)
@client.command(aliases = ['STATWATCH', 'Statwatch', 'sTATWATCH', 'statwatch','смотрит', 'СМОТРИТ', 'сМОТРИТ', "Смотрит", ])
@commands.is_owner()
async def __statwatch(ctx, *, arg):
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
        print(f"[Logs:admincmd] [Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался сменить префикс бота | {prefix}statwatch")
    else:
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.watching))
        await ctx.send("Изменяем...")
        await ctx.send("Статус бота изменен!")
        print(f"[Logs:admincmd] Префикс бота был успешно сменен на смотрит {arg} | {prefix}statwatch") 


#Команда на смену статуса(Слушает ...)
@client.command(aliases = ['Statlisten', 'sTATLISTEN', 'STATLISTEN', 'statlisten', 'Слушает', 'СЛУШАЕТ', 'слушает', 'сЛУШАЕТ'])
@commands.is_owner()
async def __statlisten(ctx, *, arg):
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
        print(f"[Logs:admincmd] [Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался сменить префикс бота | {prefix}statlisten")
    else:
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.listening))
        await ctx.send("Изменяем...")
        await ctx.send("Статус бота изменен!")   
        print(f"[Logs:admincmd] Префикс бота был успешно сменен на слушает {arg} | {prefix}statlisten") 


#Команда на смену статуса (Стримит ...)
@client.command(aliases = ['Statstream', 'STATSTREAM', 'sTATSTREAM', 'statstream', 'СТРИМИТ', 'сТРИМИТ', 'Стримит', 'стримит', ])
@commands.is_owner()
async def __statstream(ctx, *, arg):
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
        print(f"[Logs:admincmd] [Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался сменить префикс бота | {prefix}statstream")
    else:
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, url="https://www.twitch.tv/bratishkinoff", type=discord.ActivityType.streaming))
        await ctx.send("Изменяем...")
        await ctx.send("Статус бота изменен!")  
        print(f"[Logs:admincmd] Префикс бота был успешно сменен на стримит {arg} | {prefix}statstream")


# Выдача роли за тык в реакцию под сообщением:
@client.event
async def on_raw_reaction_add(payload):
    msgID = int(payload.message_id)
    if msgID == int(config.message_id):
        emoji = str(payload.emoji)
        member = payload.member 
        role = discord.utils.get(member.guild.roles, id=config.roles[emoji])
        await member.add_roles(role)
       	print(f"[Logs:admincmd] Роль была успешна выдана | Reaction System")
    else:
        pass

@client.event
async def on_raw_reaction_remove(payload):
    msgID = int(payload.message_id)
    if msgID == int(config.message_id):
        channelID = payload.channel_id
        channel = client.get_channel(channelID)
        messageID = payload.message_id
        message = await channel.fetch_message(messageID)
        userID = payload.user_id
        member = discord.utils.get(message.guild.members, id= userID)
        emoji = str(payload.emoji)
        role = discord.utils.get(member.guild.roles, id=config.roles[emoji])
        await member.remove_roles(role)
        print(f"[Logs:admincmd] Роль была успешна снята | Reaction System")
    else:
        pass
#===========================ERROR=================================
@client.event
async def on_command_error( ctx, error):
	pass

@__clear.error
async def clear_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}очистить"**', description = f'Очищает заданное количество строк чата ', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = f"{prefix}очистить <кол-во строк>", inline=False)
		emb.add_field( name = 'Пример', value = f"`{prefix}очистить 10`\n┗ Очистит 10 строк.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать количество строк для очистки | {prefix}clear")
	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}очистить"**', description = f'Очищает заданное количество строк чата ', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался очистить чат | {prefix}clear")


@__kick.error
async def kick_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}кик"**', description = f'Изгоняет указаного участника с сервера с возможностью возвращения ', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = "!кик <@⁣Участник | ID>", inline=False)
		emb.add_field( name = 'Пример', value = "`!кик @⁣Участник`\n┗ Кикнет указаного участника.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать участника | {prefix}kick")

	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}кик"**', description = f'Изгоняет указаного участника с сервера с возможностью возвращения ', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался кикнуть | {prefix}kick")

@__ban.error
async def ban_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}бан"**', description = f'Изгнать участника с сервера и заблокировать', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = "!бан <@⁣Участник | ID>", inline=False)
		emb.add_field( name = 'Пример', value = "`!бан @⁣Участник`\n┗ Забанит участника перманентно.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать участника | {prefix}ban")

	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}бан"**', description = f'Изгнать участника с сервера и заблокировать', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался забанить | {prefix}ban")


@__unban.error
async def unban_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}Разбан"**', description = f'Разблокировать участника сервера', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = f"{prefix}Разбан <@⁣Участник | ID>", inline=False)
		emb.add_field( name = 'Пример', value = f"`{prefix}Разбан @⁣Участник`\n┗ Разбанит участника", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать участника | {prefix}unban")

	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}Разбан"**', description = f'Разблокировать участника сервера', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался разбанить | {prefix}unban")


@__mute.error
async def mute_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}Мьют"**', description = f'Заблокировать чат участнику сервера', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = f"{prefix}Мьют <@⁣Участник | ID>", inline=False)
		emb.add_field( name = 'Пример', value = f"`{prefix}Мьют @⁣Участник`\n┗ Заблокирует чат участнику.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать участника | {prefix}mute")

	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}Мьют"**', description = f'Заблокировать чат участнику сервера', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался замутить | {prefix}mute")


@__unmute.error
async def unmute_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}Анмьют"**', description = f'Разблокировать чат участнику сервера', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = f"{prefix}Анмьют <@⁣Участник | ID>", inline=False)
		emb.add_field( name = 'Пример', value = f"`{prefix}Анмьют @⁣Участник`\n┗ Разблокирует чат участнику.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать участника | {prefix}unmute")

	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}Анмьют"**', description = f'Разблокировать чат участнику сервера', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)		
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался размутить | {prefix}unmute")


@__fishing.error
async def fishing_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = "ОШИБКА❗", colour = discord.Color.red() )

		emb.add_field( name = "Выберите место для рыбалки!", value = "Озеро/Река/Море")
		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] Место для рыбалки не было выбрано | {prefix}fishing")


@__rps.error
async def rps_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = "ОШИБКА❗", colour = discord.Color.red() )

		emb.add_field( name = "Причина: **укажите что-то из списка!**", value = "Камень/Ножницы/Бумага")
		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
		await ctx.send ( embed = emb)		
		print(f"[Logs:Error] Необходимо указать что-то из списка == [Камень/Ножницы/Бумага] | {prefix}rps")


@__emoji.error
async def emoji_error(ctx, error):
	if isinstance ( error, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}Емоджи"**', description = f'Емоджи реакция для любого сообщения', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = f"{prefix}Емоджи <ID СООБЩЕНИЯ> <EMOJI>", inline=False)
		emb.add_field( name = 'Пример', value = f"`{prefix}Емоджи <723539748815372419> <👍>`\n┗ Добавит реакцию 👍 к сообщению, ID которого было указано", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать емоджи | {prefix}emoji")

	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}Емоджи"**', description = f'Емоджи реакция для любого сообщения', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)	
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался добавить емоджи к сообщению | {prefix}emoji")


@__ball.error 
async def ball_error(ctx, error):

	if isinstance( error, commands.MissingRequiredArgument ): 
		emb = discord.Embed( title = f'**Команда "{prefix}Шар"**', description = f'Задать вопрос шару предсказаний', colour = discord.Color.red())
		
		emb.add_field( name = 'Использование', value = f"{prefix}Шар <Ваш вопрос>", inline=False)
		emb.add_field( name = 'Пример', value = f"`{prefix}Шар <Съесть вкусняшку??> <👍>`\n┗ Даст ответ на этот вопрос.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены")
		await ctx.send ( embed = emb) 			
		print(f"[Logs:Error] Необходимо указать вопрос | {prefix}8ball")


@__award.error
async def award_error(ctx, error):
	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}вознаграждение"**', description = f'Вознаграждение для пользователя', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)	
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался выдать вознаграждение| {prefix}reward") 


@__take.error
async def take_error(ctx, error):
	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}забрать-деньги"**', description = f'Забрать некоторое количество денег у пользователя', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)	
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался забрать деньги | {prefix}reward")



@__add_shop.error
async def add_shop_error(ctx, error):
	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}add-shop"**', description = f'Добавить роль на продажу', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)	
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался поставить роль на продажу | {prefix}reward")	


@__remove_shop.error
async def remove_shop_error(ctx, error):
	if isinstance (error, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}remove-shop"**', description = f'Удалить роль с магазина', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f"{settings['CREATOR NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)	
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался удалить роль с магазина | {prefix}reward")
#===========================AWAIT=================================

#new play !!!! (idk how to fix it)
# @client.command(aliases=['плей', 'PLAY', 'Play', 'pLAY', 'ПЛЕЙ', 'Плей','пЛЕЙ'])
# async def play(ctx, *, args):
#     channel = ctx.message.author.voice.channel
#     voice = get(client.voice_clients, guild=ctx.guild)
#     await channel.connect()
#     await ctx.send(f"Бот присоединился к каналу: {channel}") 

    # if args.startswith('https://www.youtube.com/'):
    #     ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    #     ydl.add_default_info_extractors()
    #     result = ydl.extract_info(args, download=False)
    #     if 'entries' in result:
    #         video = result['entries'][0]
    #     else:
    #         video = result
    #         for format in video['formats']:
    #             if format['ext'] == 'm4a':
    #                 audio_url = format['url']
    #                 print(audio_url)
    #         voice = get(client.voice_clients, guild=ctx.guild)
    #         voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=audio_url))
    #         voice.source = discord.PCMVolumeTransformer(voice.source)
    #         voice.source.volume = 0.10
    # else:
    #     song_there = os.path.isfile('song.mp3')
    #     try:
    #         if song_there:
    #             os.remove('song.mp3')
    #             print('[log] Старый файл удален')
    #     except PermissionError:
    #         print('[log] Не удалось удалить файл')
    #     res = bot.search(args).best.result
    #     track_id = res.id
    #     track = bot.tracks([track_id])[0]
    #     print('[log] Загружаю музыку...')
    #     track.download(filename='song.mp3', codec='mp3', bitrate_in_kbps=192)
    #     voice = get(client.voice_clients, guild=ctx.guild)
    #     voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='song.mp3'),
    #                after=lambda e: check_queue())
    #     voice.source = discord.PCMVolumeTransformer(voice.source)
    #     voice.source.volume = 0.10  


#queue        
# @client.command(aliases=['очередь', 'q', 'ОЧЕРЕДЬ', 'Q', 'QUEUE', 'Очередь', 'Queue','оЧЕРЕДЬ', 'qUEUE'])
# async def queue(ctx, *, args):
#     voice = get(client.voice_clients, guild=ctx.guild)
#     if voice and voice.is_playing():
#         que.append(args)
#         await ctx.send('Песня добавлена в очередь')
#         print(que)
#     else:
#         pass


#NEXT
# @client.command(aliases=['дальше', 'NEXT', 'Next','ДАЛЬШЕ', 'Дальше', 'дАЛЬШЕ', 'nEXT'])
# async def next(ctx):
#     voice = get(client.voice_clients, guild=ctx.guild)
#     if voice and voice.is_playing():
#         print("Воспроизведение Следующей Песни")
#         voice.stop()
#         await ctx.send("Следующая песня")
#     else:
#         print("Не удалось воспроизвести музыку")
#         await ctx.send("Не удалось воспроизвести музыку")    


#math
#client.command(aliases = [ 'вычислить', 'math', "Count", 'COUNT', 'cOUNT', 'CALC', 'Calc', 'cALC', 'ВЫЧИСЛИТЬ', 'Вычислить', 'вЫЧИСЛИТЬ','Math', 'MATH', 'mATH'])
#async def count(ctx, *, args = None):
#    text = ctx.message.content
#
#    if args == None:
#        await ctx.send(embed = discord.Embed(description = 'Please, specify expression to evaluate.', color = 0x39d0d6))
#    else:
#        result = eval(args)
#        await ctx.send(embed = discord.Embed(description = f'Evaluation result of `{args}`: \n`{result}`', color = 0x39d0d6))












#RUN
client.run (settings['TOKEN'])