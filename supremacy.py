from floppagames import is_friday, fullfloppedia
import discord
import aiohttp
import datetime
from os import getenv
from dotenv import load_dotenv

#initialize dotenv
load_dotenv()

class Eglise:

    def __init__(self, user, ctx, users_data, client):
        self.user:discord.User= user
        self.users_data= users_data
        self.ctx:discord.Message= ctx
        self.msg:str= ctx.content
        self.id= 1095216086405881856
        self.client= client
        
    async def priere(self):

        priere=self.msg.count("<:dorime:1095209010027843584>")
        self.users_data[str(self.user.id)]["pray_count"]+=priere

        if priere == 3:
            await self.ctx.add_reaction("<:trahison:1183803938244399215>")
        elif priere != 0:
            await self.ctx.add_reaction("✨")

        if is_friday() is True:

            if self.users_data[str(self.user.id)]["dark_mode"] is False and priere == 3:
                self.users_data[str(self.user.id)]["dark_mode"]= True

                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(f"{self.user.mention}, tu as ouvert les yeux... Bienvenue à toi...")

                dark_floppa=discord.utils.get(self.ctx.guild.roles, id=1101692429989593150)
                floppa=discord.utils.get(self.ctx.guild.roles, id=1094927705599905803)
                await self.ctx.author.add_roles(dark_floppa)
                await self.ctx.author.remove_roles(floppa)
            
            if self.users_data[str(self.user.id)]["last_pray"] != str(datetime.datetime.now().date()):
                self.users_data[str(self.user.id)]["last_pray"]= str(datetime.datetime.now().date())
                self.users_data[str(self.user.id)]["fidelite"]+=1
                await self.check_kado()



    async def check_kado(self):

        if self.users_data[str(self.user.id)]["dark_mode"] is False:
            
            if self.users_data[str(self.user.id)]["fidelite"] == 2:
                self.users_data[str(self.user.id)]["packs"]+=2
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(f"{self.user.mention}, je vois que tu es fidèle, je te donne 2 Floppacks 📦. Continue de prier chaque vendredi et tu continura de recevoir des dons...")
            
            if self.users_data[str(self.user.id)]["fidelite"] % 5 == 0:
                self.users_data[str(self.user.id)]["packs"]+=5
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(f"{self.user.mention}, je te donne 5 Floppacks 📦 pour ta fidèlitée.")

            if self.users_data[str(self.user.id)]["fidelite"] == 21:
                self.users_data[str(self.user.id)]["storage"].append([36, True])
                embed = discord.Embed(title= f"{fullfloppedia[36][True]['name']}", color= discord.Color.dark_blue())
                file = discord.File(fullfloppedia[36][True]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, pour toute ta fidèlitée je t'offre ceci: ", embed=embed, file=file)

            if self.users_data[str(self.user.id)]["fidelite"] == 52:
                self.users_data[str(self.user.id)]["storage"].append([3, False])
                embed = discord.Embed(title= f"{fullfloppedia[3][False]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[3][False]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 1 an de fidèlité, c'est beau... ", embed=embed, file=file)

            if self.users_data[str(self.user.id)]["fidelite"] == 104:
                self.users_data[str(self.user.id)]["storage"].append([3, True])
                embed = discord.Embed(title= f"{fullfloppedia[3][True]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[3][True]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 2 ans de fidèlité, c'est incroyable... ", embed=embed, file=file)

            if self.users_data[str(self.user.id)]["fidelite"] == 156:
                self.users_data[str(self.user.id)]["storage"].append([2, False])
                embed = discord.Embed(title= f"{fullfloppedia[2][False]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[2][False]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 3 ans de fidèlité, omg ça fait beaucoup.", embed=embed, file=file)
            
            if self.users_data[str(self.user.id)]["fidelite"] == 208:
                self.users_data[str(self.user.id)]["storage"].append([2, True])
                embed = discord.Embed(title= f"{fullfloppedia[2][True]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[2][True]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Dieu_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 4 ans de fidèlité, c'est... WAIT WHAT 4 ANS ?!", embed=embed, file=file)
        
        else:
            
            if self.users_data[str(self.user.id)]["fidelite"] == 2:
                self.users_data[str(self.user.id)]["packs"]+=2
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(f"{self.user.mention}, je vois que tu es fidèle, je te donne 2 Floppacks 📦. Continue de prier chaque vendredi et tu continura de recevoir des dons...")
            
            if self.users_data[str(self.user.id)]["fidelite"] % 5 == 0:
                self.users_data[str(self.user.id)]["packs"]+=5
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(f"{self.user.mention}, je te donne 5 Floppacks 📦 pour ta fidèlitée.")

            if self.users_data[str(self.user.id)]["fidelite"] == 21:
                self.users_data[str(self.user.id)]["storage"].append([20, True])
                embed = discord.Embed(title= f"{fullfloppedia[20][True]['name']}", color= discord.Color.dark_blue())
                file = discord.File(fullfloppedia[20][True]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, pour toute ta fidèlitée je t'offre ceci: ", embed=embed, file=file)

            if self.users_data[str(self.user.id)]["fidelite"] == 52:
                self.users_data[str(self.user.id)]["storage"].append([5, False])
                embed = discord.Embed(title= f"{fullfloppedia[5][False]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[5][False]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 1 an de fidèlité, c'est beau... ", embed=embed, file=file)

            if self.users_data[str(self.user.id)]["fidelite"] == 104:
                self.users_data[str(self.user.id)]["storage"].append([5, True])
                embed = discord.Embed(title= f"{fullfloppedia[5][True]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[5][True]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 2 ans de fidèlité, c'est incroyable... ", embed=embed, file=file)

            if self.users_data[str(self.user.id)]["fidelite"] == 156:
                self.users_data[str(self.user.id)]["storage"].append([1, False])
                embed = discord.Embed(title= f"{fullfloppedia[1][False]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[1][False]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 3 ans de fidèlité, omg ça fait beaucoup.", embed=embed, file=file)
            
            if self.users_data[str(self.user.id)]["fidelite"] == 208:
                self.users_data[str(self.user.id)]["storage"].append([1, True])
                embed = discord.Embed(title= f"{fullfloppedia[1][True]['name']}", color= discord.Color.red())
                file = discord.File(fullfloppedia[1][True]['path'], filename="floppa.png")
                embed.set_image(url="attachment://floppa.png")
                embed.set_footer(text= "Ce floppa semble avoir des couleurs différentes...")
                
                async with aiohttp.ClientSession() as session:
                    await discord.Webhook.from_url(getenv("Big_Floppa_Webhook"), session=session, client=self.client).send(content=f"{self.user.mention}, 4 ans de fidèlité, c'est... WAIT WHAT 4 ANS ?!", embed=embed, file=file)
