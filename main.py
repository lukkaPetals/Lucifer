# -*- coding: latin-1 -*-
import datetime
import urllib.request
import urllib.parse, urllib.request, re
import discord
from discord.ext import commands
from pytube import YouTube
import os
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents, help_command=None)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Use $help. Estou em ' + str(len(client.guilds))) + 'servers' )
    print(f'Logamo como {client.user}')


playlist = {}

def check_playlist(ctx, id):
    if playlist[id] != []:
        voice = ctx.guild.voice_client
        source = playlist[id].pop(0)
        player = voice.play(source, after=lambda x=None: check_playlist(ctx, ctx.message.guild.id))


@client.command(name='leave', aliases=['t2'])
async def leave(ctx):
    await ctx.voice_client.disconnect(force=True)
    return 


@client.command(name='sans', aliases=['t3'])
async def sans(ctx):
    await ctx.send("https://tenor.com/view/undertale-sans-meme-twerk-gif-24676350")


@client.command(name='play', aliases=['t4'])
async def play(ctx):
    search = ctx.message.content[5:]
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
    url =  'http://www.youtube.com/watch?v=' + search_results[0]
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='.')

    base, ext = os.path.splitext(out_file)
    new_file = out_file + '.mp3'
    os.rename(out_file, new_file)
    music =  new_file

    user = ctx.message.author
    vc = user.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    source = FFmpegPCMAudio(source=(music))

    if voice == None:
        connection = await vc.connect()
        player = connection.play(source, after=lambda x=None: check_playlist(ctx, ctx.message.guild.id))
        await ctx.send('Tocando agora: {0}'.format(yt.title))
    else:
        await ctx.voice_client.disconnect(force=True)
        connection = await vc.connect()
        player = connection.play(source, after=lambda x=None: check_playlist(ctx, ctx.message.guild.id))
        await ctx.send(f'Tocando agora: {yt.title}')


@client.command(name='pause', aliases=['t5'])
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('Tá tocando nada ')


@client.command(name='resume', aliases=['t6'])
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Tem nada pausado')


@client.command(name='stop', aliases=['t7'])
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(name='add', aliases=['t8'])
async def add(ctx):
    voice = ctx.guild.voice_client
    search = ctx.message.content[5:]
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
    url =  'http://www.youtube.com/watch?v=' + search_results[0]
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='.')
    
    base, ext = os.path.splitext(out_file)
    new_file = out_file + '.mp3'
    os.rename(out_file, new_file)
    music =  new_file
    source = FFmpegPCMAudio(music)

    guild_id = ctx.message.guild.id

    if guild_id in playlist:
        playlist[guild_id].append(source)
    else:
        playlist[guild_id] = [source]

    await ctx.send('adicionado a playlist')


@client.command(name='skip', aliases=['t9'])
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    voice.play(playlist[0])


@client.command(name='vaca', aliases=['t10'])
async def sans(ctx):
    await ctx.send("Vaca Medonha")
    await ctx.send("https://cdn.discordapp.com/attachments/633013517099728918/1077653585434775552/-98op8s.jpg")


@client.command(name='yoku', aliases=['t11'])
async def yoku(ctx):
	await ctx.send("Ela ainda é lésbica")
	await ctx.send("https://cdn.discordapp.com/attachments/633013517099728918/1077732877766234122/image0.jpg")


@client.command(name='help', aliases=['t12'])
async def help(ctx):
    await ctx.send('$play (nome da música): toca música')
    await ctx.send('$add (nome da música): adiciona música a playlist')
    await ctx.send('$pause: pausa a música')
    await ctx.send('$resume: despausa a música')
    await ctx.send('$stop: para a música')
    await ctx.send('$skip: pula a música')
    

@client.command(name='invite', aliases=['t13'])
async def invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=1047273912842604674&permissions=279747071040&scope=bot')


def delete():
    dir_name = "/home/ubuntu/bots/lucifer"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".mp3"):
            os.remove(os.path.join(dir_name, item))


now = datetime.datetime.now()
if now.hour == 5:
    delete()


client.run('')
