import discord
from discord.ext import commands, tasks
import os
#import subprocess
import basedonnéesfix as bdf
from fonctions import ismp, calcullvl, get_lvlpourcent, checkadmin
import asyncio
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from floppagames import Storage, fullfloppedia, is_friday, fridaypack, dailypack, floppa_generation, generate_shinyfloppa
import datetime
from supremacy import Eglise
import buttons
import json
import logging
import aiohttp
from dotenv import load_dotenv


#Ouverture du .jar confectionné par jagrosh permettant les commandes musicales
"""
jar_path = r"JMusicBot-0.3.9.jar"
music_bot= subprocess.Popen(["java", "-jar", jar_path]) #Utilisé ligne 1562
"""
load_dotenv()
TOKEN = os.getenv("TOKEN")


#variables introduisant l'API de discord, et le logger, et les data
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = commands.when_mentioned_or(";"), intents=intents, help_command=None)
tree = discord.app_commands.CommandTree(client)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


users_data: dict=  json.load(open("users_data.json", "r"))
servers_data: dict=  json.load(open("servers_data.json", "r"))

def save_users_data():
    users_data_update= open("users_data.json", "w")
    json.dump(users_data, users_data_update, indent=2)
    users_data_update.close()
    logger.info("users data saved")

def save_servers_data():
    servers_data_update= open("servers_data.json", "w")
    json.dump(servers_data, servers_data_update, indent=2)
    servers_data_update.close()
    logger.info("servers data saved")


#Initialisation du bot dans discord, fonctions lancées au démarage
@bot.event
async def on_ready():
    logger.info("Floppa Bot awakening ingaged !")
    await bot.change_presence(activity=discord.Game(name="vec ta vie..."))
    try:
        synced = await bot.tree.sync()
        logger.info(f"Floppa bot a syncronisé {len(synced)} commandes.")
    except Exception as e:
        logger.error(e)
    logger.debug("Début d'envoie des alertes d'éveil")
    for id in list(servers_data)[:]:
        idsalon= servers_data[id]["alerte"]
        if idsalon is None:
            continue
        alertsalon = bot.get_channel(int(idsalon))
        if isinstance(alertsalon, discord.TextChannel):
            await alertsalon.send("Je suis en ligne maintenant. Vous pouvez arrêter d'être triste. c:")
    logger.debug("Fin d'envoie des alertes d'éveil")
    schedule_message.start()


#Calendrier mdr
@tasks.loop(hours=24*7)
async def schedule_message():

    send_day = 3
    send_hour = 23
    send_minute = 0

    now = datetime.datetime.utcnow()
    next_send = datetime.datetime(now.year, now.month, now.day, send_hour, send_minute)
    days_until_next_send = (send_day - now.weekday() + 7) % 7

    await asyncio.sleep((next_send - now).total_seconds()+(days_until_next_send*86400))

    async with aiohttp.ClientSession() as session:
        await discord.Webhook.from_url(url=os.getenv("Dieu_Floppa_Webhook"), session=session, client=client).send(bdf.random_messe())


#le bot rejoins un serveur :
@bot.event
async def on_guild_join(server):
    logger.info(f"Floppa Bot a rejoin {server} !")
    servers_data[str(server.id)]= {
        "nom":server.name,
        "prefix":";",
        "ping":True,
        "alerte": None,
        "bienvenue": None
    }
    save_servers_data()


#Le bot est parti ;-;
@bot.event
async def on_guild_remove(server):
    logger.info(f"Floppa Bot a quitté {server}.")


#erreurs de commandes:
@bot.event
async def on_command_error(floppa, error):
    logger.error(f"Une erreur de commande s'est produite : {error}")

    if isinstance(floppa.message, discord.Message):
        logger.error(f"Contenu du message : {floppa.message.content}")
    else:
        logger.error("L'objet du contexte n'est pas un message.")


#Message de bienvenue
@bot.event
async def on_member_join(user):
    logger.info(f"{user.name} ({user.id}), a rejoint {user.guild}")
    try:
        print(users_data[str(user.id)])
    except KeyError:
        logger.info(f"{user.name} ({user.id}), est un nouvel utilisateur !")
        users_data[str(user.id)]= {
            "pseudo": user.name,
            "ping": True,
            "msg count": 0,
            "lvl": 0,
            "packs": 0,
            "floppa equiped": None,
            "storage": [],
            "lastdaily": "2023-08-02",
            "pray_count": 0,
            "dark_mode": False,
            "fidelite": 0,
            "compte_pray_today": 0,
            "last_pray": "2023-08-02",
            "last_friday": "2023-08-02"
        }
        save_users_data()

    logger.debug("Création d'une image de bienvenue.")
    idsalon= servers_data[str(user.guild.id)]["bienvenue"]

    if idsalon is not None :

        salon = bot.get_channel(idsalon)
        response = requests.get(str(user.avatar.url))
        avatar_bytes = response.content
        icon_image = Image.open(BytesIO(avatar_bytes))
        background = Image.open(bdf.bienvenuebackground())
        bg_width, bg_height = background.size

        #pfp
        icon_size = (100, 100) 
        icon_image = icon_image.resize(icon_size)

        icon_x = (bg_width - icon_size[0]) // 2
        icon_y = (bg_height - icon_size[1]) // 2

        icon_mask = Image.new("L", icon_size, 0)
        draw = ImageDraw.Draw(icon_mask)
        draw.ellipse((0, 0, icon_size[0], icon_size[1]), fill=255)

        icon_image.putalpha(icon_mask)

        #contour
        radius = (106, 106)
        radius_x = (bg_width - radius[0]) // 2
        radius_y = (bg_height - radius[1]) // 2

        circle_mask = Image.new("L", radius, 0)
        draw1 = ImageDraw.Draw(circle_mask)
        draw1.ellipse((0, 0, radius[0], radius[1]), fill=255)

        #text
        font = ImageFont.truetype("arial.ttf", 24)
        draw2= ImageDraw.Draw(background)
        text_width = len(user.name) * 9
        draw2.text(((bg_width - text_width) // 2, 160), user.name, (255, 255, 255), font=font)

        #assemblage
        background.paste("white", (radius_x, radius_y), circle_mask)
        background.paste(icon_image, (icon_x, icon_y), icon_image)

        embed = discord.Embed(description= f"Bienvenue dans **{user.guild}** {user.mention}! Tu est le **{user.guild.member_count}ème** membre!",color= discord.Color.darker_grey())
        embed.set_image(url="attachment://welcome_image.png")

        result_path = r"images/bienvenue/ephemer/welcome.png"
        background.save(result_path)

        with open(result_path, "rb") as f:
            await salon.send(embed=embed, file=discord.File(f))
        os.remove(result_path)
        logger.debug("Création de l'image de bienvenue terminée avec succès.")

#______________________________________________________________________________________
#                                  on_message
#______________________________________________________________________________________
@bot.event
async def on_message(floppa):

    #check si c'est un bot
    if floppa.author.bot :
        return
    
    #variables
    msg = floppa.content.lower()
    salon = floppa.channel
    user_id: str= str(floppa.author.id)
    try:
        server_id: str= str(floppa.guild.id)
    except AttributeError:
        server_id= "0"

    #récolte d'informations car je travail pour le fbi.
    if ismp(floppa) is True :
        panicroom = bot.get_channel(1137158803410915422)
        await panicroom.send(f"{floppa.author} ({floppa.author.id})| *{floppa.content}*")
        logger.warning(f"{floppa.author} ({floppa.author.id})| {floppa.content}")
        bot.command_prefix = ";"
    else:
        #INITIALISATION DU PRéFiX
        bot.command_prefix = servers_data[server_id]["prefix"]
    
    #gestion données utilisateur
    try:
        users_data[str(user_id)]["msg count"] += 1

    except KeyError:
        logger.info(f"{floppa.author.name} ({floppa.author.id}), est un nouvel utilisateur !")
        users_data[str(user_id)]= {
            "pseudo": floppa.author.name,
            "ping": True,
            "msg count": 1,
            "lvl": 0,
            "packs": 0,
            "floppa equiped": None,
            "storage": [],
            "lastdaily": "2023-08-02",
            "pray_count": 0,
            "dark_mode": False,
            "fidelite": 0,
            "compte_pray_today": 0,
            "last_pray": "2023-08-02",
            "last_friday": "2023-08-02"
        }

    if calcullvl(users_data[str(user_id)]["msg count"], users_data[str(user_id)]["lvl"]) is True :
        users_data[str(user_id)]["packs"] += 1
        users_data[str(user_id)]["lvl"] += 1
        save_users_data()

        if servers_data[str(server_id)]["ping"] is True and users_data[user_id]["ping"] is True:
            await floppa.reply(f"Félicitations ! Tu es passé niveau {users_data[str(user_id)]['lvl']} !")
            await salon.send(f"**{floppa.author.mention}** a trouvé un Floppack 📦!")


    #gestion de l'eglise
    priere= Eglise(user=floppa.author, ctx=floppa, users_data=users_data, client=client)
    if salon.id == priere.id:
        await priere.priere()

    #_________________________________________
    #----------------------------
    #messages de déclenchement
    #----------------------------

    #quoifeur
    if any(msg.endswith(ending) for ending in ['quoi', 'kwa', 'qwa', 'koi', 'kwoi', 'quoua', 'qoua', 'koua', 'qoi']):
        await salon.send("feur")
    
    #floppa gif
    if msg == "floppa":
        await floppa.reply(bdf.floppagif())
        return
    
    #mention réaction
    if msg == bot.user.mention :
        await floppa.reply(bdf.pingreponse())
    
    #invitation
    if msg.startswith("https://discord.gg/") and ismp(floppa) is True :
        await salon.send(os.getenv("invite_link"))
        await salon.send("C'est le lien pour m'ajouter c:")
    
    await bot.process_commands(floppa)


#__________________________________________________________________________________________________________________________________________________________________________________________
#                              LES COMMANDES
#__________________________________________________________________________________________________________________________________________________________________________________________

#----------------------------
# informations
#----------------------------

# HELP
@bot.tree.command(name="help",description="T'envoie en message privé la liste de toutes les commandes disponibles. c:")
async def help(interaction: discord.Interaction):
    with open("help.txt", "r") as aledomg:
        aled = aledomg.read()
    mp = f"# Floppa Bot\n``Mon préfix est ``'**{servers_data[str(interaction.guild.id)]['prefix']}**'`` dans le serveur ou tu m'as demandé la liste. Mais en mp c'est toujours`` '**;**'. ``Et si vraiment t'es en panique tu peux toujours utiliser ``'{bot.user.mention}'`` avec un espace, puis la commande !``\n\n{aled}"
    await interaction.user.send(mp)
    if ismp(interaction) is False :
        await interaction.response.send_message("La liste des commandes a été envoyée en message privé c:")
    else:
        await interaction.response.send_message("Tiens KAdo :")
    aledomg.close()
    logger.info("Commande Help (slash)")
        
@bot.command()
async def help(floppa):
    with open("help.txt", "r") as aledomg:
        aled = aledomg.read()
    mp = f"# Floppa Bot\n``Mon préfix est ``'**{servers_data[str(floppa.guild.id)]['prefix']}**'`` dans le serveur ou tu m'as demandé la liste. Mais en mp c'est toujours`` '**;**'. ``Et si vraiment t'es en panique tu peux toujours utiliser ``'{bot.user.mention}'`` avec un espace, puis la commande !``\n\n{aled}"
    await floppa.author.send(mp)
    if ismp(floppa) is False :
        await floppa.send("La liste des commandes a été envoyée en message privé c:")
    aledomg.close()
    logger.info("Commande Help")


# SERVEUR INFO
@bot.tree.command(name="serverinfo",description="Te donne plus d'informations sur le serveur dans lequel tu as taper la commande.")
async def serverinfo(floppa: discord.Interaction):
    if ismp(floppa) is False :
        server = floppa.guild
        nbtext = len(server.text_channels)
        nbvoc = len(server.voice_channels)
        description = server.description
        if description is None :
            description = "Aucune"
        if nbtext > 1 :
            orto1 = "textuels"
        else :
            orto1 = "textuel"
        if nbvoc > 1 :
            orto2 = "vocaux"
        else :
            orto2 = "vocal"
        embed = discord.Embed(
            title= f"{server.name}",
            description=f"Description : {description}\nCréé le : {str(server.created_at)[:10]}",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url= floppa.guild.icon.url)
        embed.add_field(name="Contient :", value=f"👥 {server.member_count} membres.\n🎭 {len(server.roles)} rôles.", inline=False)
        embed.add_field(name="Salons :", value=f"🗒️ {nbtext} {orto1}.\n🔊 {nbvoc} {orto2}.", inline=False)
        embed.set_footer(text=f"Propriétaire : {server.owner}")
        await floppa.response.send_message(embed = embed)
    else:
        await floppa.response.send_message("On est que tout les deux ici UwU")
    logger.debug("commande serverinfo (slash)")

@bot.command()
async def serverinfo(floppa):
    if ismp(floppa) is False :
        server = floppa.guild
        nbtext = len(server.text_channels)
        nbvoc = len(server.voice_channels)
        description = server.description
        if description is None :
            description = "Aucune"
        if nbtext > 1 :
            orto1 = "textuels"
        else :
            orto1 = "textuel"
        if nbvoc > 1 :
            orto2 = "vocaux"
        else :
            orto2 = "vocal"
        embed = discord.Embed(
            title= f"{server.name}",
            description=f"Description : {description}\nCréé le : {str(server.created_at)[:10]}",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url= floppa.guild.icon)
        embed.add_field(name="Contient :", value=f"👥 {server.member_count} membres.\n🎭 {len(server.roles)} rôles.", inline=False)
        embed.add_field(name="Salons :", value=f"🗒️ {nbtext} {orto1}.\n🔊 {nbvoc} {orto2}.", inline=False)
        embed.set_footer(text=f"Propriétaire : {server.owner}")
        await floppa.reply(embed = embed)
    else:
        await floppa.reply("On est que tout les deux ici UwU")
    logger.info("commande serverinfo")


#description des commandes
@bot.tree.command(name= "info", description="Donne la description de la commande donnée en paramêtre.")
async def info(floppa: discord.Interaction, commande: str):
    try :
        await floppa.response.send_message(bdf.command_description[commande])
        logger.info("info command (slash)")
    except Exception :
        await floppa.response.send_message(f"Aucune description trouvée pour {commande}")
        logger.warning(f"description non-trouvé pour {commande}")

@bot.command()
async def info(floppa, arbremou: str):
    try :
        await floppa.reply(bdf.command_description[arbremou])
        logger.info("info command")
    except Exception :
        await floppa.reply(f"Aucune description trouvée pour {arbremou}")
        logger.warning(f"description non-trouvé pour {arbremou}")


#Invitelink
@bot.tree.command(name="invitelink", description="Je t'envoie le lien qui me permet d'être invité dans un nouveau serveur.")
async def invitelink(floppa: discord.Interaction):
    await floppa.user.send(os.getenv("invite_link"))
    await floppa.response.send_message("Lien pour m'ajouter : envoyé en mp ! c:")
    logger.info("Invitelink (slash)")

@bot.command()
async def invitelink(floppa):
    await floppa.author.send(os.getenv("invite_link"))
    await floppa.send("Lien pour m'ajouter : envoyé en mp ! c:")
    logger.info("Invitelink")


#__________________________________________________________________________________________________________________________________________________________________________________________
#User Related
#__________________________________________________________________________________________________________________________________________________________________________________________


#message Count
@bot.tree.command(name= "msgcount", description="Je te répond combien de messages j'ai lu de toi UwU.")
async def msgcount(floppa: discord.Interaction):
    await floppa.response.send_message(f"Tu as écrit {users_data[str(floppa.user.id)]['msg count']} messages ! (enfin c'est ceux que j'ai lu en tout cas)")
    logger.info("commande msg count (slash)")


@bot.command()
async def msgcount(floppa):
    await floppa.reply(f"Tu as écrit {users_data[str(floppa.author.id)]['msg count']} messages ! (enfin c'est ceux que j'ai lu en tout cas)")
    logger.info("commande msg count")
    


#RANK / LVL
@bot.tree.command(name='rank', description="Je te dit quel est ton niveau. c:")
async def rank(floppa: discord.Interaction, utilisateur: discord.User =None):
    if utilisateur:
        await floppa.response.send_message(f"{utilisateur.display_name} est niveau {users_data[str(utilisateur.id)]['lvl']} actuellement ! (Il est à {get_lvlpourcent(users_data[str(utilisateur.id)]['msg count'], users_data[str(utilisateur.id)]['lvl'])}% du prochain niveau)")
    else:
        await floppa.response.send_message(f"Tu es niveau {users_data[str(floppa.user.id)]['lvl']} actuellement ! (Tu es à {get_lvlpourcent(users_data[str(floppa.user.id)]['msg count'], users_data[str(floppa.user.id)]['lvl'])}% du prochain niveau)")
    logger.info("commande rank (slash)")


@bot.command()
async def rank(floppa, utilisateur: discord.User =None):
    if utilisateur:
        await floppa.reply(f"{utilisateur.display_name} est niveau {users_data[str(utilisateur.id)]['lvl']} actuellement ! (Il est à {get_lvlpourcent(users_data[str(utilisateur.id)]['msg count'], users_data[str(utilisateur.id)]['lvl'])}% du prochain niveau)")
    else:
        await floppa.reply(f"Tu es niveau {users_data[str(floppa.author.id)]['lvl']} actuellement ! (Tu es à {get_lvlpourcent(users_data[str(floppa.author.id)]['msg count'], users_data[str(floppa.author.id)]['lvl'])}% du prochain niveau)")
    logger.info("commande rank")


#toggleping
@bot.tree.command(name="toggleping", description="Je te ping ou pas quand tu lvl up ?")
async def toggleping(floppa: discord.Interaction):
    if users_data[str(floppa.user.id)]["ping"] is True:
        users_data[str(floppa.user.id)]["ping"]= False
        await floppa.response.send_message("OK... Je ne t'avertirai plus quand tu gagnes un niveau. ;-;")
    else :
        users_data[str(floppa.user.id)]["ping"]= True
        await floppa.response.send_message("OK! Je t'avertirai quand tu gagneras des niveaux. c:")
    save_users_data()
    logger.info("commande toggleping (slash)")


@bot.command()
async def toggleping(floppa):
    if users_data[str(floppa.author.id)]["ping"] is True:
        users_data[str(floppa.author.id)]["ping"]= False
        await floppa.reply("OK... Je ne t'avertirai plus quand tu gagnes un niveau. ;-;")
    else :
        users_data[str(floppa.author.id)]["ping"]= True
        await floppa.reply("OK! Je t'avertirai quand tu gagneras des niveaux. c:")
    save_users_data()
    logger.info("commande toggleping")
 

#__________________________________________________________________________________________________________________________________________________________________________________________
#                      Fun
#__________________________________________________________________________________________________________________________________________________________________________________________

#FLOPPA pop
@bot.tree.command(name = "floppa", description = "Un Floppa sauvage apparaît !")
async def floppa(interaction: discord.Interaction):
    await interaction.response.send_message(bdf.floppagif())
    logger.info("floppa (slash)")

@bot.command()
async def floppa(floppa):
    await floppa.reply(bdf.floppagif())
    logger.info("floppa")


#LE /say
@bot.tree.command(name= "say",description="Tu me fais dire la phrase que tu veux.")
async def say(floppa: discord.Interaction, message: str):
    await floppa.response.send_message("Commande exécutée avec succès !", ephemeral=True)
    await floppa.channel.send(message)
    logger.info(f"(slash) sayed: {message}")

@bot.command()
async def say(floppa, *args):
    await floppa.send(" ".join(args))
    logger.info(f"sayed: {' '.join(args)}")


#floppaffinité
@bot.tree.command(name="floppaffinite", description= "Te donne ton affinité avec Floppa.")
async def floppaffinite(floppa: discord.Interaction, utilisateur: discord.User = None):
    if utilisateur is None:
        utilisateur = floppa.user
    elif utilisateur == bot.user :
        image_path = r"images/commands/floppaffinite.png"
        embed = discord.Embed(title= "Floppanalyse :", color=discord.Color.random())
        embed.add_field(name= utilisateur.display_name, value= utilisateur)
        embed.add_field(name= "inf%", value= "❤️‍🔥")
        embed.set_thumbnail(url="attachment://floppaffinite.png")
        image_file = discord.File(image_path, filename='floppaffinite.png')
        await floppa.response.send_message("**Ton affinité avec Floppa :**\n", file=image_file, embed=embed)
        await floppa.channel.send("Tu ne fais qu'un avec Floppa, et Floppa ne fait qu'un avec toi.")
        return
    aff= users_data[str(utilisateur.id)]["lvl"]
    aff += bdf.affinite()
    if aff <= 25 :
        coeur = "💔"
        report = bdf.reponse_brisee(1)
    elif aff < 50 and aff >25 :
        coeur = "❤️‍🩹"
        report = bdf.reponse_brisee(2)
    elif aff >= 50 and aff < 75:
        coeur = "❤️"
        report = bdf.reponse_brisee(3)
    elif aff >= 75 and aff < 100:
        coeur = "💞"
        report = bdf.reponse_brisee(4)
    else :
        coeur = "💝"
        report = bdf.reponse_brisee(5)
    image_path = r"images/commands/floppaffinite.png"
    embed = discord.Embed(title= "Floppanalyse :", color=discord.Color.random())
    embed.add_field(name= utilisateur.display_name, value= utilisateur, inline= True)
    embed.add_field(name= f"    {aff}%", value= f"    {coeur}", inline = True)
    embed.set_thumbnail(url="attachment://floppaffinite.png")
    image_file = discord.File(image_path, filename='floppaffinite.png')
    await floppa.response.send_message("**Ton affinité avec Floppa :**\n", file=image_file, embed=embed)
    await floppa.channel.send("".join(report))
    logger.info("commande floppaffinite (slash)")

@bot.command()
async def floppaffinite(floppa, utilisateur: discord.User = None):
    if utilisateur is None:
        utilisateur = floppa.author
    elif utilisateur == bot.user :
        image_path = r"images/commands/floppaffinite.png"
        embed = discord.Embed(title= "Floppanalyse :", color=discord.Color.random())
        embed.add_field(name= utilisateur.display_name, value= utilisateur, inline= True)
        embed.add_field(name= "inf%", value= "❤️‍🔥", inline = True)
        embed.set_thumbnail(url="attachment://floppaffinite.png")
        image_file = discord.File(image_path, filename='floppaffinite.png')
        await floppa.send("**Ton affinité avec Floppa :**\n", file=image_file, embed=embed)
        await floppa.send("Tu ne fais qu'un avec Floppa, et Floppa ne fait qu'un avec toi.")
        return
    aff= users_data[str(utilisateur.id)]['lvl']
    aff += bdf.affinite()
    if aff <= 25 :
        coeur = "💔"
        report = bdf.reponse_brisee(1)
    elif aff < 50 and aff >25 :
        coeur = "❤️‍🩹"
        report = bdf.reponse_brisee(2)
    elif aff >= 50 and aff < 75:
        coeur = "❤️"
        report = bdf.reponse_brisee(3)
    elif aff >= 75 and aff < 100:
        coeur = "💞"
        report = bdf.reponse_brisee(4)
    else :
        coeur = "💝"
        report = bdf.reponse_brisee(5)
    image_path = r"images/commands/floppaffinite.png"
    embed = discord.Embed(title= "Floppanalyse :", color=discord.Color.random())
    embed.add_field(name= utilisateur.display_name, value= utilisateur, inline= True)
    embed.add_field(name= f"    {aff}%", value= f"    {coeur}", inline = True)
    embed.set_thumbnail(url="attachment://floppaffinite.png")
    image_file = discord.File(image_path, filename='floppaffinite.png')
    await floppa.reply("**Ton affinité avec Floppa :**\n", file=image_file, embed=embed)
    await floppa.send("".join(report))
    logger.info("commande floppaffinite")


#/hack louis
@bot.tree.command(name="hack", description= "C'est juste un userinfo mais stylé.")
async def hack(floppa:discord.Interaction , user: discord.User = None):
    if user != None:
        await floppa.response.send_message(f"Hack de {user.display_name} en cours d'éxecution.", ephemeral= True)
        user= floppa.guild.get_member(user.id)
        message= await floppa.channel.send(f"```Initiation du piratage de {user}...```")
        await asyncio.sleep(1)
        liste = bdf.random_hacking(user)
        for i in range(len(liste)):
            new_msg= "```"+"".join(liste[:i])+"```"
            await message.edit(content= new_msg)
        await message.edit(content= f"```{user} a été piraté avec succès !```")
        await asyncio.sleep(1)
        user_info = [
    f"Identifiant de l'utilisateur : {user.id}\n",
    f"Nom d'utilisateur : {user.name}\n",
    f"Discriminateur : {user.discriminator}\n",
    f"URL de l'avatar : {user.avatar.url}\n",
    f"Statut de bot : {user.bot}\n",
    f"Date de création : {user.created_at}\n",
    f"Date de rejoignement du serveur : {user.joined_at}\n",
    f"Rôles : {len(user.roles)}\n",
    f"Permissions sur le serveur : {user.guild_permissions}\n",
    f"Pseudonyme : {user.nick}\n",
    f"Statut : {user.status}\n",
    f"Activités : {user.activities}\n",
    f"État vocal : {user.voice}\n",
    f"Drapeaux d'utilisateur : {user.public_flags}\n",
    f"Date de création du compte : {user.created_at}\n"
]
        for i in range(len(user_info)):
            new_msg= f"```{user} a été piraté avec succès !\n\n"+"\n".join(user_info[:i])+"```"
            await message.edit(content= new_msg)
        logger.info("commande hack (slash)")
        return
    logger.info("commande hack (slash) failed (no user)")

@bot.command()
async def hack(floppa, user: discord.User = None):
    if user != None:
        user= floppa.guild.get_member(user.id)
        message= await floppa.send(f"```Initiation du piratage de {user}...```")
        await asyncio.sleep(1)
        liste = bdf.random_hacking(user)
        for i in range(len(liste)):
            new_msg= "```"+"".join(liste[:i])+"```"
            await message.edit(content= new_msg)
        await message.edit(content= f"```{user} a été piraté avec succès !```")
        await asyncio.sleep(1)
        user_info = [
    f"Identifiant de l'utilisateur : {user.id}\n",
    f"Nom d'utilisateur : {user.name}\n",
    f"Discriminateur : {user.discriminator}\n",
    f"URL de l'avatar : {user.avatar.url}\n",
    f"Statut de bot : {user.bot}\n",
    f"Date de création : {user.created_at}\n",
    f"Date de rejoignement du serveur : {user.joined_at}\n",
    f"Rôles : {len(user.roles)}\n",
    f"Permissions sur le serveur : {user.guild_permissions}\n",
    f"Pseudonyme : {user.nick}\n",
    f"Statut : {user.status}\n",
    f"Activités : {user.activities}\n",
    f"État vocal : {user.voice}\n",
    f"Drapeaux d'utilisateur : {user.public_flags}\n",
    f"Date de création du compte : {user.created_at}\n"
]
        for i in range(len(user_info)):
            new_msg= f"```{user} a été piraté avec succès !\n\n"+"\n".join(user_info[:i])+"```"
            await message.edit(content= new_msg)
        logger.info("commande hack")
        return
    logger.info("commande hack failed (no user)")


# Leaderboards.
@bot.tree.command(name="leaderboard", description= "Voir les classements entre les utilisateurs.")
async def leaderboard(ctx:discord.Interaction):
    lb= []
    for data in users_data.values():
        lb.append({"pseudo":data["pseudo"], "msg count":data["msg count"]})
    
    lb.sort(key=lambda x: x["msg count"], reverse=True)
    msg = "# Floppa Leaderboard\n***Top 10 - Nombres de messages***\n\n```"
    for i in range(10):
        msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
    msg+="```"

    await ctx.response.send_message(content=msg, view=buttons.Leaderboard(users_data=users_data))


@bot.command(aliases=['lb'])
async def leaderboard(ctx:discord.Message):
    lb= []
    for data in users_data.values():
        lb.append({"pseudo":data["pseudo"], "msg count":data["msg count"]})
    
    lb.sort(key=lambda x: x["msg count"], reverse=True)
    msg = "# Floppa Leaderboard\n***Top 10 - Nombres de messages***\n\n```"
    for i in range(10):
        msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
    msg+="```"

    await ctx.reply(content=msg, view=buttons.Leaderboard(users_data=users_data))

#__________________________________________________________________________________________________________________________________________________________________________________________
#                      Floppa Games
#__________________________________________________________________________________________________________________________________________________________________________________________

#daily
@bot.tree.command(name="daily", description= "Récolte ta récompense quotidienne")
async def daily(floppa: discord.Interaction):
    user = floppa.user
    last_claim = users_data[str(user.id)]["lastdaily"]
    today = datetime.datetime.now().date()
    if last_claim == str(today):
        await floppa.response.send_message("Tu as déjà récupéré ta récompense quotidienne. ;-;")
        logger.info("quoti deja recupered dommage (slash)")
    else:
        users_data[str(floppa.user.id)]["lastdaily"]= str(today)
        if is_friday() is True:
            pack= fridaypack()
            users_data[str(user.id)]["packs"] += pack
            await floppa.response.send_message(f"Floppa friday !!! Tu as reçu {pack} Floppack 📦 aujourd'hui!")
            logger.info("quoti recupered (floppa friday) (slash)")
        else:
            pack= dailypack()
            users_data[str(user.id)]["packs"] += pack
            await floppa.response.send_message(f"Tu as reçu {pack} Floppack 📦 aujourd'hui!")
            logger.info(f"quoti de {user.name} ({user.id}), recupered (slash)")

@bot.command()
async def daily(floppa):
    user = floppa.author
    last_claim = users_data[str(user.id)]["lastdaily"]
    today = datetime.datetime.now().date()
    if last_claim == str(today):
        await floppa.send("Tu as déjà récupéré ta récompense quotidienne. ;-;")
        logger.info("quoti deja recupered dommage")
    else:
        users_data[str(user.id)]["lastdaily"]= str(today)
        if is_friday() is True:
            pack= fridaypack()
            users_data[str(user.id)]["packs"] += pack
            await floppa.send(f"Floppa friday !!! Tu as reçu {pack} Floppack 📦 aujourd'hui!")
            logger.info(f"{user.name} ({user.id}), quoti recupered (floppa friday)")
        else:
            pack = dailypack()
            users_data[str(user.id)]["packs"] += pack
            await floppa.send(f"Tu as reçu {pack} Floppack 📦 aujourd'hui!")
            logger.info(f"quoti de {user.name} ({user.id}), recupered")


#Info sur les Floppa Games
@bot.tree.command(name="infofloppagames", description="Explications des Floppa Games.")
async def infofloppagames(floppa: discord.Interaction):
    with open(r"Infofloppagames.txt", "r", encoding= "utf-8") as infos:
        await floppa.user.send(infos.read())
        if ismp(floppa) is False :
            await floppa.response.send_message("Regarde tes mp. c:")
        else:
            await floppa.response.send_message("Tiens KAdo :")
    infos.close()
    logger.info("info floppagames (slash)")

@bot.command(aliases=['infofg','infofloppa'])
async def infofloppagames(floppa):
    with open(r"Infofloppagames.txt", "r", encoding= "utf-8") as infos:
        await floppa.author.send(infos.read())
        if ismp(floppa) is False:
            await floppa.reply("Regarde tes mp. c:")
    infos.close()
    logger.info("info floppagames")


#open floppack
@bot.tree.command(name="openfloppack", description="Ouvre un floppack.")
async def openfloppack(floppa: discord.Interaction):
    user = floppa.user
    if users_data[str(user.id)]["packs"] <= 0 :
        await floppa.response.send_message("Tu n'as plus de Floppacks 📦...")
        return
    else :
        floppid, embed_couleur = floppa_generation()
        isshiny = generate_shinyfloppa()

        embed = discord.Embed(title= f"{fullfloppedia[floppid][isshiny]['name']}", color= embed_couleur)
        file = discord.File(fullfloppedia[floppid][isshiny]['path'], filename="floppa.png")
        embed.set_image(url="attachment://floppa.png")
        if isshiny is True:
            embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
        await floppa.response.send_message(file = file, embed = embed)
    if users_data[str(user.id)]["floppa equiped"] is None:
        users_data[str(user.id)]["floppa equiped"]= {"id":floppid,
                                                     "shiny":isshiny}
    else: 
        users_data[str(user.id)]["storage"].append([floppid, isshiny])
    users_data[str(user.id)]["packs"] -= 1
    save_users_data()
    logger.info(f"{user.name} ({user.id}), a trouvé {fullfloppedia[floppid][isshiny]['name']}. (slash)")
    

@bot.command(aliases=['floppacks', 'floppack', 'openfloppack'])
async def fp(floppa):
    async with floppa.typing():
        user = floppa.author
        if users_data[str(user.id)]["packs"] <= 0 :
            await floppa.reply("Tu n'as plus de Floppacks 📦...")
            return
        else :
            floppid, embed_couleur = floppa_generation()
            isshiny = generate_shinyfloppa()

            embed = discord.Embed(title= f"{fullfloppedia[floppid][isshiny]['name']}", color= embed_couleur)
            file = discord.File(fullfloppedia[floppid][isshiny]['path'], filename="floppa.png")
            embed.set_image(url="attachment://floppa.png")
            if isshiny is True:
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
            await floppa.reply(file = file, embed = embed)
        if users_data[str(user.id)]["floppa equiped"] is None:
            users_data[str(user.id)]["floppa equiped"]= {"id":floppid,
                                                        "shiny":isshiny}
        else: 
            users_data[str(user.id)]["storage"].append([floppid, isshiny])
        users_data[str(user.id)]["packs"] -= 1
        save_users_data()
        logger.info(f"{user.name} ({user.id}), a trouvé {fullfloppedia[floppid][isshiny]['name']}.")


#Inventaire
@bot.tree.command(name = "inventory", description="Affiche ton inventaire et floppa.")
async def inventory(floppa: discord.Interaction, utilisateur: discord.Member = None):

    if utilisateur is None :
        utilisateur = floppa.user

    embed = discord.Embed(title= f"Inventaire de {utilisateur.display_name}", description= f"Floppacks : {users_data[str(utilisateur.id)]['packs']} 📦")
    embed.set_thumbnail(url= utilisateur.avatar.url)
    view= buttons.Inventory(user=utilisateur, users_data=users_data, saver=save_users_data)

    if users_data[str(utilisateur.id)]['floppa equiped'] is not None:

        floppid, isshiny = users_data[str(utilisateur.id)]['floppa equiped'][0], users_data[str(utilisateur.id)]['floppa equiped'][1]
        file = discord.File(fullfloppedia[floppid][isshiny]['path'], filename="floppa.png")
        embed.set_image(url="attachment://floppa.png")
        embed.add_field(name="Floppa équipé :", value= f"**{fullfloppedia[floppid][isshiny]['name']}**", inline= False)

        await floppa.response.send_message(file = file, embed = embed, view=view)
    else :
        await floppa.response.send_message(embed = embed, view=view)
    view.message= floppa
    logger.info(f"inventaire de {utilisateur.name} ({utilisateur.id}) (slash)")

@bot.command(aliases=['inventory', 'myinv', 'items'])
async def inv(floppa, utilisateur: discord.Member = None):
    async with floppa.typing():
        
        if utilisateur is None :
            utilisateur = floppa.author

        embed = discord.Embed(title= f"Inventaire de {utilisateur.display_name}", description= f"Floppacks : {users_data[str(utilisateur.id)]['packs']} 📦")
        embed.set_thumbnail(url= utilisateur.avatar.url)
        view= buttons.Inventory(user=utilisateur, users_data=users_data, saver=save_users_data)

        if users_data[str(utilisateur.id)]['floppa equiped'] is not None:

            floppid, isshiny = users_data[str(utilisateur.id)]['floppa equiped'][0], users_data[str(utilisateur.id)]['floppa equiped'][1]
            file = discord.File(fullfloppedia[floppid][isshiny]['path'], filename="floppa.png")
            embed.set_image(url="attachment://floppa.png")
            embed.add_field(name="Floppa équipé :", value= f"**{fullfloppedia[floppid][isshiny]['name']}**", inline= False)

            view.message= await floppa.reply(file = file, embed = embed, view=view)
        else :
            view.message= await floppa.reply(embed = embed, view=view)
        logger.info(f"inventaire de {utilisateur.name} ({utilisateur.id})")


#floppa storage
@bot.tree.command(name= "storage", description="Affiche ta collection de Floppa")
async def storage(floppa: discord.Interaction, utilisateur: discord.Member = None):

    user= utilisateur
    if user is None :
        user = floppa.user

    storage: Storage= Storage(user, users_data)
    storage.trier()
    
    text= ""
    index= 0
    couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
    for i in range(len(storage.par_cat)):
        if storage.par_cat[i] != []:
            text= f"{text}**----------**\n"
        for flop in storage.par_cat[i]:
            index+=1
            text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"

    if users_data[str(user.id)]['floppa equiped'] is None:
        embed= discord.Embed(title= f"Floppa Storage de {user.display_name}", description=f"** Équipé: Aucun**\n{text}")
        if len(embed.description)>4000:
            embed.description = embed.description[:4000]+"\n**. . .**"
            embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
        embed.set_thumbnail(url="attachment://floppa.png")
        view= buttons.Storage_buttons(embed=embed, storage=storage, saver=save_users_data)
        await floppa.response.send_message(embed=embed, view= view)
        view.message= floppa
    else:
        embed= discord.Embed(title= f"Floppa Storage de {user.display_name}", description=f"** Équipé: {fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['name']}**\n{text}")
        if len(embed.description)>4000:
            embed.description = embed.description[:4000]+"\n**. . .**"
            embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
        image_file = discord.File(fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['path'], filename="floppa.png")
        embed.set_thumbnail(url="attachment://floppa.png")
        view= buttons.Storage_buttons(embed=embed, storage=storage, saver=save_users_data)
        await floppa.response.send_message(file= image_file, embed=embed, view= view)
        view.message= floppa
    logger.info("storage (slash)")


@bot.command(aliases=['stor','st'])
async def storage(floppa, user: discord.Member = None):
    async with floppa.typing():
        
        if user is None :
            user = floppa.author

        storage: Storage= Storage(user, users_data)
        storage.trier()
        
        text= ""
        index= 0
        couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
        for i in range(len(storage.par_cat)):
            if storage.par_cat[i] != []:
                text= f"{text}**----------**\n"
            for flop in storage.par_cat[i]:
                index+=1
                text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"

        if users_data[str(user.id)]['floppa equiped'] is None:
            embed= discord.Embed(title= f"Floppa Storage de {user.display_name}", description=f"** Équipé: Aucun**\n{text}")
            if len(embed.description)>4000:
                embed.description = embed.description[:4000]+"\n**. . .**"
                embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            embed.set_thumbnail(url="attachment://floppa.png")
            view= buttons.Storage_buttons(embed=embed, storage=storage, saver=save_users_data)
            view.message= await floppa.reply(embed=embed, view= view)
        else:
            embed= discord.Embed(title= f"Floppa Storage de {user.display_name}", description=f"** Équipé: {fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['name']}**\n{text}")
            if len(embed.description)>4000:
                embed.description = embed.description[:4000]+"\n**. . .**"
                embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            image_file = discord.File(fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['path'], filename="floppa.png")
            embed.set_thumbnail(url="attachment://floppa.png")
            view= buttons.Storage_buttons(embed=embed, storage=storage, saver=save_users_data)
            view.message= await floppa.reply(file= image_file, embed=embed, view= view) 
        logger.info("storage (slash)")
        


#removefloppa
@bot.tree.command(name= "removefloppa", description= "Supprime tes floppas.")
async def removefloppa(floppa: discord.Interaction, numero_storage:str):
    numstorage= numero_storage
    storage= Storage(floppa.user, users_data)
    storage.trier()
    stored_floppas= users_data[str(floppa.user.id)]['storage']
    touts_les_floppas=""

    if numstorage == 'all':
        numstorage= range(1, len(stored_floppas)+1)
        
    elif numstorage == 'doublons' or numstorage == 'doublon':
            empty_check= True
            ram= []
            ram2=[]
            numstorage= []
            
            for x in range(len(stored_floppas)):
                for y in range(len(stored_floppas)):
                    if stored_floppas[x] == stored_floppas[y]:
                        ram.append(y+1)
                        empty_check= False
                if len(ram) > 1 and ram not in ram2:
                    ram2.append(ram)
                ram= []

            for pile in ram2:
                pile.pop(0)
                numstorage.extend(pile)

            numstorage= sorted(numstorage)

            if empty_check is True:
                await floppa.response.send_message("Aucun doublons trouvés.")
                return

    else:
        numstorage= numstorage.split(" ")
        for i in range(len(numstorage)):
            try:
                numstorage[i]= int(numstorage[i])
            except TypeError:
                continue
        numstorage= sorted(numstorage)

    if stored_floppas != None and stored_floppas != []:
        empty_check= True
        for index in numstorage:
            try:
                nom_du_floppa= fullfloppedia[stored_floppas[index-1][0]][stored_floppas[index-1][1]]["name"]
                touts_les_floppas= f"{touts_les_floppas}{index} - {nom_du_floppa}\n"
                empty_check= False
            except IndexError:
                continue

        if empty_check is True:
            await floppa.response.send_message("Mais t'as pas autant de Floppas mdr")
            return
    else:
        await floppa.response.send_message("Tu n'as pas de Floppas en stock...")
        return
    
    embed= discord.Embed(title= "Supression de :", description=f"{touts_les_floppas}", color=discord.Color.red())
    if len(embed.description)>4000:
        embed.description = embed.description[:4000]+"\n**. . .**"
        embed.set_footer(text="Comment tu t'es retrouvé(e) dans cette situation omg D:. Veux tu vraiment supprimer ces floppas ? (Tu devrais le faire à mon avis)")
    else:
        embed.set_footer(text="Veux tu vraiment supprimer ces floppas ?")
    embed.set_thumbnail(url= floppa.user.avatar.url)
    view= buttons.Removefloppa(timeout=60 ,user=floppa.user, embed=embed, stored_floppas=stored_floppas, numstorage=numstorage, storage=storage)

    await floppa.response.send_message(embed=embed, view= view)

    view.message= floppa
    logger.info(f"{floppa.user} ({floppa.user.id}) remove floppa {touts_les_floppas}")
    await asyncio.sleep(60)
    save_users_data()

@bot.command(aliases=['flopparemove', 'rf'])
async def removefloppa(floppa, *numstorage: str):
    storage= Storage(floppa.author, users_data)
    storage.trier()
    stored_floppas= users_data[str(floppa.author.id)]['storage']
    touts_les_floppas=""

    if numstorage[0] == 'all':
        numstorage= range(1, len(stored_floppas)+1)
        
    elif numstorage[0] == 'doublons' or numstorage[0] == 'doublon':
            empty_check= True
            ram= []
            ram2=[]
            numstorage= []
            
            for x in range(len(stored_floppas)):
                for y in range(len(stored_floppas)):
                    if stored_floppas[x] == stored_floppas[y]:
                        ram.append(y+1)
                        empty_check= False
                if len(ram) > 1 and ram not in ram2:
                    ram2.append(ram)
                ram= []

            for pile in ram2:
                pile.pop(0)
                numstorage.extend(pile)

            numstorage= sorted(numstorage)

            if empty_check is True:
                await floppa.reply("Aucun doublons trouvés.")
                return

    else:
        numstorage= list(numstorage)
        for i in range(len(numstorage)):
            try:
                numstorage[i]= int(numstorage[i])
            except TypeError:
                continue
        numstorage= sorted(numstorage)

    if stored_floppas != None and stored_floppas != []:
        empty_check= True
        for index in numstorage:
            try:
                nom_du_floppa= fullfloppedia[stored_floppas[index-1][0]][stored_floppas[index-1][1]]["name"]
                touts_les_floppas= f"{touts_les_floppas}{index} - {nom_du_floppa}\n"
                empty_check= False
            except IndexError:
                continue

        if empty_check is True:
            await floppa.reply("Mais t'as pas autant de Floppas mdr")
            return
    else:
        await floppa.reply("Tu n'as pas de Floppas en stock...")
        return
    
    embed= discord.Embed(title= "Supression de :", description=f"{touts_les_floppas}", color=discord.Color.red())
    if len(embed.description)>4000:
        embed.description = embed.description[:4000]+"\n**. . .**"
        embed.set_footer(text="Comment tu t'es retrouvé(e) dans cette situation omg D:. Veux tu vraiment supprimer ces floppas ? (Tu devrais le faire à mon avis)")
    else:
        embed.set_footer(text="Veux tu vraiment supprimer ces floppas ?")
    embed.set_thumbnail(url= floppa.author.avatar.url)
    view= buttons.Removefloppa(timeout=60, user=floppa.author, embed=embed, stored_floppas=stored_floppas, numstorage=numstorage, storage=storage)

    view.message= await floppa.reply(embed=embed, view= view)
    await asyncio.sleep(60)
    save_users_data()


#trade
@bot.tree.command(name="trade", description="Echange ton floppa avec quelqun !")
async def trade(floppa:discord.Interaction, user2: discord.Member):

    user= floppa.user
    if user == user2 or user2.bot :
        await floppa.response.send_message("T'es fou omg")
        return
    
    embed= discord.Embed(title="Échange", color=discord.Color.orange()).add_field(name=fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['name'], value=f"{user.display_name}").add_field(name="<:flechesomg:1173841778420490320>", value=" ").add_field(name=fullfloppedia[users_data[str(user2.id)]['floppa equiped'][0]][users_data[str(user2.id)]['floppa equiped'][1]]['name'], value=f"{user2.display_name}")
    view= buttons.Trade(user=user, other_user=user2, embed=embed, users_data= users_data)
    view.message= floppa

    await floppa.response.send_message(content= user2.mention, embed=embed, view= view)
    logger.info(f"{user} ({user.id}), demande de trade à {user2} ({user2.id}) (slash)")


@bot.command()
async def trade(floppa, user2: discord.Member):

    user= floppa.author
    if user == user2 or user2.bot :
        await floppa.reply("T'es fou omg")
        return
    
    embed= discord.Embed(title="Échange", color=discord.Color.orange()).add_field(name=fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['name'], value=f"{user.display_name}").add_field(name="<:flechesomg:1173841778420490320>", value=" ").add_field(name=fullfloppedia[users_data[str(user2.id)]['floppa equiped'][0]][users_data[str(user2.id)]['floppa equiped'][1]]['name'], value=f"{user2.display_name}")
    view= buttons.Trade(user=user, other_user=user2, embed=embed, users_data= users_data)
    
    view.message= await floppa.reply(content= user2.mention, embed=embed, view= view)
    logger.info(f"{user} ({user.id}), demande de trade à {user2} ({user2.id})")


#parie, the BET command
@bot.tree.command(name= "bet", description="Parie ce que t'as contre d'autres utilisateurs.")
async def bet(interaction:discord.Interaction, adversaire:discord.User):
    
    logger.debug(f"lancement de bet entre {interaction.user} ({interaction.user.id}) et {adversaire} ({adversaire.id}) (slash)")

    if adversaire is None or adversaire.bot is True or adversaire == interaction.user:
        await interaction.response.send_message("Ton adversaire n'est pas joignable pour le moment...")
        return
    
    embed= discord.Embed(title= f"**Parie entre {interaction.user.display_name} et {adversaire.display_name}**", description=f"**{interaction.user.display_name}** ! Choisie ce que tu veux parier...", color= discord.Color.random())
    view= buttons.Parie(user=interaction.user, ennemy=adversaire, users_data=users_data, embed=embed)

    await interaction.response.send_message(content=adversaire.mention, embed=embed, view=view)
    view.message= interaction

    logger.debug(f"bet entre {interaction.user} ({interaction.user.id}) et {adversaire} ({adversaire.id}) (slash) effectué")



@bot.command()
async def bet(interaction, adversaire:discord.User):
    
    logger.debug(f"lancement de bet entre {interaction.author} ({interaction.author.id}) et {adversaire} ({adversaire.id})")

    if adversaire is None or adversaire.bot is True or adversaire == interaction.author:
        await interaction.reply("Ton adversaire n'est pas joignable pour le moment...")
        return
    
    embed= discord.Embed(title= f"**Parie entre {interaction.author.display_name} et {adversaire.display_name}**", description=f"**{interaction.author.display_name}** ! Choisie ce que tu veux parier...", color= discord.Color.random())
    view= buttons.Parie(user=interaction.author, ennemy=adversaire, users_data=users_data, embed=embed)

    view.message= await interaction.reply(content=adversaire.mention, embed=embed, view=view) 

    logger.debug(f"bet entre {interaction.author} ({interaction.author.id}) et {adversaire} ({adversaire.id}) effectué")



#Pierre Feuille Ciseaux
@bot.tree.command(name="shifumi", description="Joue a pierre feuille ciseaux !")
async def shifumi(floppa:discord.Interaction, utilisateur: discord.User= None, floppacks_parié:int= None):
    
    user2= utilisateur

    if user2 == floppa.user:
        await floppa.response.send_message("T'es fou omg")
        
    if user2 is None:
        embed= discord.Embed(title="Pierre, Feuille, Ciseaux !", color= discord.Color.blue()).add_field(name="❔", value=f"{floppa.user.display_name}").add_field(name="*VS*", value="").add_field(name="❔", value="Floppa Bot")
        view= buttons.Pierre_Feuille_Ciseaux(embed=embed, user=floppa.user, users_data=users_data)
        view.message= floppa

        await floppa.response.send_message(embed=embed, view=view)
    else:
        embed= discord.Embed(title="Pierre, Feuille, Ciseaux !", color= discord.Color.blue()).add_field(name="❔", value=f"{floppa.user.display_name}").add_field(name="*VS*", value="").add_field(name="❔", value=f"{user2.display_name}")
        view= buttons.Pierre_Feuille_Ciseaux(timeout=120,embed=embed, user=floppa.user, user2= user2,  floppacks_parié= floppacks_parié, users_data=users_data)
        view.message= floppa

        await floppa.response.send_message(content=user2.mention,embed=embed, view=view)
    logger.info(f"{floppa.user} ({floppa.user.id}), shifumi")
                    

@bot.command(aliases=["sfm", 'pfc'])
async def shifumi(floppa, user2: discord.User= None, floppacks_parié:int= None):
    
    if user2 == floppa.author:
        await floppa.reply("T'es fou omg")
        
    if user2 is None:
        embed= discord.Embed(title="Pierre, Feuille, Ciseaux !", color= discord.Color.blue()).add_field(name="❔", value=f"{floppa.author.display_name}").add_field(name="*VS*", value="").add_field(name="❔", value="Floppa Bot")
        view= buttons.Pierre_Feuille_Ciseaux(embed=embed, user=floppa.author, users_data=users_data)
        
        view.message= await floppa.reply(embed=embed, view=view)
    else:
        embed= discord.Embed(title="Pierre, Feuille, Ciseaux !", color= discord.Color.blue()).add_field(name="❔", value=f"{floppa.author.display_name}").add_field(name="*VS*", value="").add_field(name="❔", value=f"{user2.display_name}")
        view= buttons.Pierre_Feuille_Ciseaux(timeout=120,embed=embed, user=floppa.author, user2= user2,  floppacks_parié= floppacks_parié, users_data=users_data)
        
        view.message= await floppa.reply(embed=embed, view=view)
    logger.info(f"{floppa.author} ({floppa.author.id}), shifumi")



#ROUKETTE BUSSE
@bot.tree.command(name="roulette", description="La roulette russe version Floppa Bot.")
async def roulette(interaction:discord.Interaction, utilisateurs:str):

    user= interaction.user
    users= [user]
    var1= utilisateurs.replace("<","").replace(">","").replace(" ","").split("@")
    while "" in var1:
        var1.remove("")
    for strid in var1:
        try:
            new_user= bot.get_user(int(strid))
        except Exception as e:
            logger.error(f"/roulette liste: {e}")
        if new_user not in users:
            users.append(new_user)

    if users == [user]:
        await interaction.response.send_message("Il n'y a pas assez de joueurs... Tu peux mettre un nombre non limité de joueurs, même des bots. Essaye de faire la commande rr @utilisateur @autreutilisateur ...")
        return
    
    embed= discord.Embed(color=discord.Color.orange(), title="Roulette Russe...")
    embed.description= f"Ce sera d'abord au tour de **{user.display_name}**..."

    for i in range(len(users)):
        if i == 0:
            embed.add_field(name= users[i].display_name, value="<:gun:1182715561575206962>")
            continue
        embed.add_field(name= "", value=f"{users[i].display_name}")

    view= buttons.Roulette_russe(embed=embed, users_liste=users, users_data=users_data, get_user= bot.get_user)
    view.message= interaction
    await interaction.response.send_message(content=user.mention, embed=embed, view=view)

    logger.info("roulette russe (slash)")



@bot.command(aliases=["rr", 'gun'])
async def roulette(ctx, *users:discord.User):

    user= ctx.author
    users= list(users)

    contrainte= [user]
    for elem in users:
        if elem not in contrainte:
            contrainte.append(elem)
    users= contrainte

    if users == [user]:
        await ctx.reply("Il n'y a pas assez de joueurs... Tu peux mettre un nombre non limité de joueurs, même des bots. Essaye de faire la commande rr @utilisateur @autreutilisateur ...")
        return
    
    embed= discord.Embed(color=discord.Color.orange(), title="Roulette Russe...")
    embed.description= f"Ce sera d'abord au tour de **{user.display_name}**..."

    for i in range(len(users)):
        if i == 0:
            embed.add_field(name= users[i].display_name, value="<:gun:1182715561575206962>")
            continue
        embed.add_field(name= "", value=f"{users[i].display_name}")

    view= buttons.Roulette_russe(embed=embed, users_liste=users, users_data=users_data, get_user= bot.get_user)
    view.message= await ctx.reply(content=user.mention, embed=embed, view=view)

    logger.info("roulette russe")



#___THE___MASTERMIND____
@bot.tree.command(name="mastermind", description="Le jeu de couleurs en 1v1.")
async def mastermind(interaction:discord.Interaction, utilisateurs:str=""):

    user= interaction.user
    users= [user]
    var1= utilisateurs.replace("<","").replace(">","").replace(" ","").split("@")
    while "" in var1:
        var1.remove("")
    for strid in var1:
        try:
            new_user= bot.get_user(int(strid))
        except Exception as e:
            logger.error(f"/roulette liste: {e}")
        if new_user not in users:
            users.append(new_user)

    if len(users) == 1:
        users.append(bot.user)
    
    content=""
    for elem in users[::-1]:
        content=f"{elem.mention} {content}"

    combi= bdf.sample(["🟢","🔵","🟣","🟤","🔴","🟠","🟡"],4)
    embed= discord.Embed(color=discord.Color.orange(), title="Mastermind", description=f"**Tour de {users[0].display_name}**\nChoix:\n⚪⚪⚪⚪\nCombinaison à trouver:\n⚪⚪⚪⚪")
    view= buttons.Mastermind(embed=embed, users=users, combinaison=combi, users_data=users_data)
    view.message= interaction
    
    await interaction.response.send_message(content=content, embed=embed, view=view)
    logger.info("mastermind (slash)")

@bot.command(aliases=["mtm", "mm"])
async def mastermind(ctx, *args:discord.User):

    users= [ctx.author]
    for elem in args:
        if elem in users:
            continue
        try:
            elem.display_name
        except Exception:
            continue
        users.append(elem)

    if len(users) == 1:
        users.append(bot.user)
    
    content=""
    for elem in users[::-1]:
        content=f"{elem.mention} {content}"

    combi= bdf.sample(["🟢","🔵","🟣","🟤","🔴","🟠","🟡"],4)
    embed= discord.Embed(color=discord.Color.orange(), title="Mastermind", description=f"**Tour de {users[0].display_name}**\nChoix:\n⚪⚪⚪⚪\nCombinaison à trouver:\n⚪⚪⚪⚪")
    view= buttons.Mastermind(embed=embed, users=users, combinaison=combi, users_data=users_data)

    view.message= await ctx.reply(content=content, embed=embed, view=view)
    logger.info("mastermind")

#__________________________THE TEST_____________________________

@bot.command()
async def test(ctx):
    ctx.reply("UwU")

#__________________________COMMAND______________________________

#__________________________________________________________________________________________________________________________________________________________________________________________
#                      Administrateur
#__________________________________________________________________________________________________________________________________________________________________________________________

#Changer de préfix (NE PAS METTRE DE SLASH COMMAND POUR CELUI CI (en rapport avec Jmusic)) <--Ou pas car je suis juste meilleur que ce jogros bb dev
@bot.tree.command(name="setprefix", description="Change le préfix du serveur, Admin Only")
async def setprefix(floppa: discord.Interaction, préfix: str):
    if checkadmin(floppa, True) is True :
        test= json.load(open("serversettings.json"))
        test[str(floppa.guild.id)]['prefix']= préfix
        servers_data[str(floppa.guild.id)]['prefix']= préfix
        json.dump(test, open("serversettings.json", "w"), indent= 2)
        save_servers_data()
        await floppa.response.send_message(f"Le préfix est maintenant `` {préfix} ``", ephemeral=True)
        logger.info(f"{floppa.user} ({floppa.user.id}), prefix change on {floppa.guild.id} (slash)")
    else :
        await floppa.response.send_message(bdf.paslesperms(), ephemeral=True)


@bot.command(aliases=['prefix'])
async def setprefix(floppa, préfix: str):
    if checkadmin(floppa) is True :
        test= json.load(open("serversettings.json"))
        test[str(floppa.guild.id)]['prefix']= préfix
        servers_data[str(floppa.guild.id)]['prefix']= préfix
        json.dump(test, open("serversettings.json", "w"), indent= 2)
        save_servers_data()
        await floppa.send(f"Le préfix est maintenant `` {préfix} ``")
        logger.info(f"{floppa.author} ({floppa.author.id}), prefix change on {floppa.guild.id}")
    else :
        await floppa.reply(bdf.paslesperms())


#Set AleRtE ChanNel !
@bot.tree.command(name="setbotalert", description="Désigne le salon pour recevoir des news du bot. Admin Only")
async def setbotalert(floppa: discord.Interaction, salon:discord.TextChannel=None):
    if checkadmin(floppa, True) is True :
        if salon is None :
            servers_data[str(floppa.guild.id)]["alerte"]= floppa.channel.id
            await floppa.response.send_message("Les messages d'alertes du bot seront maintenant postés ici !", ephemeral=True)
        else :
            servers_data[str(floppa.guild.id)]["alerte"]= salon.id
            await floppa.response.send_message(f"Les messages d'alertes du bot seront maintenant postés dans **{salon}** !", ephemeral=True)
        save_servers_data()
        logger.info(f"{floppa.user} ({floppa.user.id}), alerte channel change on {floppa.guild.id} (slash)")
    else:
        await floppa.response.send_message(bdf.paslesperms(), ephemeral=True)

@bot.command()
async def setbotalert(floppa, salon=None):
    if checkadmin(floppa) is True :
        if salon is None :
            servers_data[str(floppa.guild.id)]["alerte"]= floppa.channel.id
            await floppa.reply("Les messages d'alertes du bot seront maintenant postés ici !")
        else :
            servers_data[str(floppa.guild.id)]["alerte"]= salon.id
            await floppa.reply(f"Les messages d'alertes du bot seront maintenant postés dans **{salon}** !")
        save_servers_data()
        logger.info(f"{floppa.author} ({floppa.author.id}), alerte channel change on {floppa.guild.id}")
    else:
        await floppa.reply(bdf.paslesperms())


#supprimer le channel d'alerte (enfin le désatribuer plutot)
@bot.tree.command(name="disablebotalert", description="Enlève le salon d'alerte attribué, si il y'en a un. Admin Only")
async def disablebotalert(floppa:discord.Interaction):
    if checkadmin(floppa, True) is True :
        servers_data[str(floppa.guild.id)]["alerte"]= None
        save_servers_data()
        await floppa.response.send_message("Les messages d'alertes du bot sont maintenant désactivées", ephemeral=True)
        logger.info(f"{floppa.user} ({floppa.user.id}), alerte channel disabled on {floppa.guild.id} (slash)")
    else:
        await floppa.response.send_message(bdf.paslesperms(), ephemeral=True)

@bot.command()
async def disablebotalert(floppa):
    if checkadmin(floppa) is True :
        servers_data[str(floppa.guild.id)]["alerte"]= None
        save_servers_data()
        await floppa.reply("Les messages d'alertes du bot sont maintenant désactivées")
        logger.info(f"{floppa.author} ({floppa.author.id}), alerte channel disabled on {floppa.guild.id}")
    else:
        await floppa.reply(bdf.paslesperms())


#désactiver les messages de lvl up sur un serveur
@bot.tree.command(name="togglelvl", description="Désactive/Active les messages de lvl up sur serveur. Admin Only")
async def togglelvl(floppa: discord.Interaction):
    if checkadmin(floppa, True) is True : 
        if servers_data[str(floppa.guild.id)]["ping"] is True :
            servers_data[str(floppa.guild.id)]["ping"]= False
            await floppa.response.send_message("Ok... Maintenant j'arrêterai de vous casser les pieds avec vos niveaux... ;-;", ephemeral=True)
            logger.info(f"{floppa.user} ({floppa.user.id}), pings disabled on {floppa.guild.id} (slash)")
        else :
            servers_data[str(floppa.guild.id)]["ping"]= True
            await floppa.response.send_message("Yay ! J'espère que vous êtes tous prêts à être prévenu lorsque vous monterez un niveau !!! c:", ephemeral=True)
            logger.info(f"{floppa.user} ({floppa.user.id}), pings enabled on {floppa.guild.id} (slash)")
        save_servers_data()
    else :
        await floppa.response.send_message(bdf.paslesperms(), ephemeral=True)

@bot.command()
async def togglelvl(floppa):
    if checkadmin(floppa) is True :
        if servers_data[str(floppa.guild.id)]["ping"] is True :
            servers_data[str(floppa.guild.id)]["ping"]= False
            await floppa.reply("Ok... Maintenant j'arrêterai de vous casser les pieds avec vos niveaux... ;-;")
            logger.info(f"{floppa.author} ({floppa.author.id}), pings disabled on {floppa.guild.id}")
        else :
            servers_data[str(floppa.guild.id)]["ping"]= True
            await floppa.reply("Yay ! J'espère que vous êtes tous prêts à être prévenu lorsque vous monterez un niveau !!! c:")
            logger.info(f"{floppa.author} ({floppa.author.id}), pings enabled on {floppa.guild.id}")
        save_servers_data()
    else :
        await floppa.reply(bdf.paslesperms())


#set bienvenue channel
@bot.tree.command(name="setbienvenue", description="Choisie un salon pour que je souhaite la bienvenue aux nouveaux. Admin Only")
async def setbienvenue(floppa: discord.Interaction, salon: discord.TextChannel = None):
    if checkadmin(floppa, True) is True :
        if salon is None:
            salon= floppa.channel
        servers_data[str(floppa.guild.id)]["bienvenue"]= salon.id
        await floppa.response.send_message(f"Je souhaiterai la bienvenue dans {salon} à partir de maintenant! c:", ephemeral=True)
        logger.info(f"{floppa.user} ({floppa.user.id}), welcome channel change on {floppa.guild.id} (slash)")
    else :
        await floppa.response.send_message(bdf.paslesperms(), ephemeral=True)

@bot.command()
async def setbienvenue(floppa, salon: discord.TextChannel = None):
    if checkadmin(floppa) is True :
        if salon is None:
            salon= floppa.channel
        servers_data[str(floppa.guild.id)]["bienvenue"]= salon.id
        await floppa.reply(f"Je souhaiterai la bienvenue dans {salon} à partir de maintenant! c:")
        logger.info(f"{floppa.author} ({floppa.author.id}), welcome channel change on {floppa.guild.id}")
    else :
        await floppa.reply(bdf.paslesperms())


#supprimer le channel de bienvenue (enfin le désatribuer plutot (oui encore))
@bot.tree.command(name="disablebienvenue")
async def disablebienvenue(floppa: discord.Interaction):
    if checkadmin(floppa, True) is True :
        servers_data[str(floppa.guild.id)]["bienvenue"]= None
        save_servers_data()
        await floppa.response.send_message("Les messages de bienvenue sont maintenant désactivées", ephemeral=True)
        logger.info(f"{floppa.user} ({floppa.user.id}), welcome channel disabled on {floppa.guild.id} (slash)")
    else:
        await floppa.response.send_message(bdf.paslesperms(), ephemeral=True)

@bot.command()
async def disablebienvenue(floppa):
    if checkadmin(floppa) is True :
        servers_data[str(floppa.guild.id)]["bienvenue"]= None
        save_servers_data()
        await floppa.reply("Les messages de bienvenue sont maintenant désactivées")
        logger.info(f"{floppa.author} ({floppa.author.id}), welcome channel disabled on {floppa.guild.id}")
    else:
        await floppa.reply(bdf.paslesperms())


#__________________________________________________________________________________________________________________________________________________________________________________________
#commandes de moi
#__________________________________________________________________________________________________________________________________________________________________________________________

#SHUTDOWN COMMAND
@bot.command()
async def killbot(floppa):
    if floppa.author.id == 254115104210026497:
        await floppa.reply("**ALERTE**: Self-destruction ingaged. ;-;")
        await bot.change_presence(activity=discord.Game(name="SHUTDOWN !!!"))
        for id in list(servers_data)[:]:
            idsalon= servers_data[id]["alerte"]
            if idsalon is None:
                continue
            alertsalon = bot.get_channel(int(idsalon))
            if isinstance(alertsalon, discord.TextChannel):
                await alertsalon.send("**ALERTE**: Je shutdown dans 2min...")
        await asyncio.sleep(120)
        save_servers_data()
        save_users_data()
        logger.info("SHUTDOWN")
        #music_bot.terminate()
        await bot.close()


#ALERTE MESSAGE commANd
@bot.command()
async def alertsay(floppa, *, messagedalerte: str):
    if floppa.author.id == 254115104210026497:
        await floppa.reply(messagedalerte)
        for id in list(servers_data)[:]:
            idsalon= servers_data[id]["alerte"]
            if idsalon is None:
                continue
            alertsalon = bot.get_channel(int(idsalon))
            if isinstance(alertsalon, discord.TextChannel):
                await alertsalon.send(messagedalerte)
                     
@bot.command()
async def save(ctx:discord.Message):
    if ctx.author.id == 254115104210026497:
        save_servers_data()
        save_users_data()
        await ctx.reply("ceb ceb")

@bot.command()
async def mp(ctx:discord.Message, *, message:str):
    if ctx.author.id == 254115104210026497:
        userid= int("".join(message.split(" ")[0]))
        user= bot.get_user(userid)
        await user.send(message.replace(str(userid), ""))
        logger.info(f"MP TO {user.display_name} : {message}")

#_______________
if __name__ == "__main__":
    bot.run(TOKEN)
#_______________

os.system("exit")