import discord
import random
import time
import sqlite3
import datetime
import math

db=sqlite3.connect("taubot.db")
crsr=db.cursor()
levels=[0,10,30,60,100,150,210,280]

from discord.ext import commands
bot = commands.Bot(command_prefix='=', description="A bot found in the great servers of the T'au empire")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)


@bot.event
async def on_message(message):
    print(message.author.mention+str(datetime.datetime.now()))
    SQL_command="SELECT username FROM discord"
    users=[]
    crsr.execute(SQL_command)
    tempusers=crsr.fetchall()
    for i in tempusers:
        users.append(i[0])
    MessName=str("'"+message.author.mention+"'")
    if not (MessName in users):
        SQL_command="INSERT INTO discord VALUES (?,?)"
        crsr.execute(SQL_command,[MessName,1])
    else:
        SQL_command="SELECT messages FROM discord WHERE username = ?"
        crsr.execute(SQL_command,(MessName,))
        messag=crsr.fetchall()[0][0]+1
        SQL_command="UPDATE discord SET messages="+str(messag)+" WHERE username = ?"
        crsr.execute(SQL_command,(MessName,))
        print(messag)
    SQL_command="SELECT * FROM discord"
    crsr.execute(SQL_command)
    print(crsr.fetchall())
    db.commit()
    if messag in levels:
        await message.channel.send("Congrats "+message.author.mention+" Has reached level "+levels.index(messag))
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    '''Say hi!'''
    await ctx.send('Hello Cunt!')
    print("hello:"+ctx.author.mention)

@bot.command()
async def echo(ctx,*, something):
    '''Echoes your statement'''
    await ctx.message.delete()
    await ctx.send("`"+"``"+something+"`"+"``")

@bot.command()
async def messages(ctx):
    '''How many messages have i sent?'''
    user = "'"+ctx.author.mention+"'"
    SQL_command="SELECT messages FROM discord WHERE username = ?"
    crsr.execute(SQL_command,(user,))
    num=crsr.fetchall()
    await ctx.send('You have made: '+str(num[0][0])+' mesages')
    print("messages:"+ctx.author.mention)

@bot.command()
async def code(ctx):
    '''read the code'''
    file=open("Taubot.py","r")
    code=file.readlines()
    pri=""
    for i in range(0,len(code)-1):
        if code[i]=="\n" or len(pri)>1500:
            await ctx.author.send("``"+"`python\n"+pri+"\n``"+"`")
            pri=""
        else:
            pri=pri+code[i]
    print("code:"+ctx.author.mention)
    

@bot.command()
async def roll(ctx, dice):
    '''roll dice like 'roll 2d6' '''
    part=0
    times=""
    maxi=""
    for i in range(0,len(dice)):
        if dice[i]=="d":
            part=1
        elif part==0:
            times=times+dice[i]
        elif part==1:
            maxi=maxi+dice[i]
        elif i >10:
            times=""
    if times=="":
        times="0"
    times=int(times)
    maxi=int(maxi)
    var=[]
    if times==0:
        var=[random.randint(1,maxi)]
    else:
        for i in range(0,times):
            var.append(random.randint(1,maxi))
    await ctx.send(var)
    sum = 0
    for i in var:
        sum = sum+i
    await ctx.send("**Sum=**"+str(sum))
    print("roll:"+ctx.author.mention)
        

bot.run("NTc3MTU0MzYwODcwNjk5MDM5.XNg7YQ.g6ntgtqTcE1Y_03zO2i-WTZJCT4")