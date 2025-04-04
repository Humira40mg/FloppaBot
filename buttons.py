from typing import Any, Coroutine, List, Optional
import discord
import asyncio
from random import randint, sample
from discord.components import SelectOption
from discord.interactions import Interaction
from discord.utils import MISSING
from floppagames import Storage, fullfloppedia, randompackadd


#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Removefloppa(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, user, embed: discord.Embed, stored_floppas: list, numstorage, storage:Storage):
        super().__init__(timeout=timeout)
        self.user= user
        self.embed= embed
        self.stored_floppas= stored_floppas
        self.numstorage= numstorage
        self.storage= storage
        self.completed= False

    async def on_timeout(self) -> None:
        if self.completed is False:
            try:
                await self.message.edit(content="# Trop tard", embed=None, view=None)
            except AttributeError:
                await self.message.edit_original_response(content="# Trop tard", embed=None, view=None)

    @discord.ui.button(label="Supprimer", style=discord.ButtonStyle.danger)
    async def suppr_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.user:
            return
        
        await interaction.message.edit(view= None)
        
        self.embed.title= "Supprimés"
        self.embed.color= discord.Color.lighter_grey()
        self.embed.set_footer(text="Ces Floppas ont été supprimés ;-;")
        
        floppacks_won= 0

        for num in self.numstorage[::-1]:
            self.stored_floppas.pop(num-1)
            luck= randint(1,3)
            if luck == 3 :
                floppacks_won+=1

        if floppacks_won != 0:
            self.storage.users_data[str(self.user.id)]["packs"] += floppacks_won
            await interaction.response.send_message(f"{interaction.user.mention}, tu as gagné **{floppacks_won}** Floppacks 📦!")

        await interaction.message.edit(embed=self.embed)
        self.completed= True


    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.primary)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            return
        await interaction.message.edit(content="**Supression Annulée**", embed=None, view= None)
        self.completed= True


#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Inventory(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, user:discord.User, users_data:dict, saver):
        super().__init__(timeout=timeout)
        self.user= user
        self.users_data= users_data
        self.save= saver

    
    async def on_timeout(self) -> None:
        try:
            await self.message.edit(view=None)
        except AttributeError:
            try:
                await self.message.edit_original_response(view=None)
            except AttributeError:
                pass
            

    @discord.ui.button(label= "Storage",style=discord.ButtonStyle.success)
    async def stor_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        user = self.user
        users_data= self.users_data

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
            view= Storage_buttons(embed=embed, storage=storage, saver=self.save)
            await interaction.message.edit(embed=embed, view= view)
        else:
            embed= discord.Embed(title= f"Floppa Storage de {user.display_name}", description=f"** Équipé: {fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['name']}**\n{text}")
            if len(embed.description)>4000:
                embed.description = embed.description[:4000]+"\n**. . .**"
                embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            image_file = discord.File(fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['path'], filename="floppa.png")
            embed.set_thumbnail(url="attachment://floppa.png")
            view= Storage_buttons(embed=embed, storage=storage, saver=self.save)
            await interaction.message.edit(attachments=[image_file], embed=embed, view= view)


#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Storage_buttons(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, embed: discord.Embed, storage: Storage, saver):
        super().__init__(timeout=timeout)
        self.embed= embed
        self.user= storage.user
        self.line= 0
        self.all_lines= range(len(storage.in_order)+1)
        self.storage= storage
        self.users_data= storage.users_data
        self.save= saver

    async def on_timeout(self) -> None:
        try:
            await self.message.edit(view=None)
        except AttributeError:
            try:
                await self.message.edit_original_response(view=None)
            except AttributeError:
                pass


    @discord.ui.button(emoji="<:gauche:1173048276480696441>",style=discord.ButtonStyle.primary)
    async def left_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        if self.line == 0 :
            self.line = self.all_lines[-1]
            self.children[1].disabled= False
        else:
            self.line-= 1
            if self.line == 0:
                self.children[1].disabled= True

        self.storage.trier()
        self.all_lines= range(len(self.storage.in_order)+1)
        text= ""
        index= 0
        couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
        for i in range(len(self.storage.par_cat)):
            if self.storage.par_cat[i] != []:
                text= f"{text}**----------**\n"
            for flop in self.storage.par_cat[i]:
                index+=1
                if self.line == index:
                    text= f"{text}{couloir[i]}**{index} - {fullfloppedia[flop[0]][flop[1]]['name']}**\n"
                    image_file = discord.File(fullfloppedia[flop[0]][flop[1]]['path'], filename="floppa.png")
                else:
                    text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"

        
        if self.line == 0:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"** Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}**\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
                image_file = discord.File(fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]["path"], filename="floppa.png")
        else:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
        
        try:
            await interaction.message.edit(embed=self.embed, attachments=[image_file], view= self)
        except UnboundLocalError:
            pass
    

    @discord.ui.button(label="Équiper",style=discord.ButtonStyle.secondary, disabled=True)
    async def equip_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.user:
            return

        await interaction.response.defer()

        if self.users_data[str(self.user.id)]["floppa equiped"] != None:
            safeswitch= [self.users_data[str(self.user.id)]['floppa equiped'][0], self.users_data[str(self.user.id)]['floppa equiped'][1]]
            self.users_data[str(self.user.id)]['floppa equiped'][0]= self.users_data[str(self.user.id)]["storage"][self.line-1][0]
            self.users_data[str(self.user.id)]['floppa equiped'][1]= self.users_data[str(self.user.id)]["storage"][self.line-1][1]
            self.users_data[str(self.user.id)]["storage"][self.line-1]= safeswitch
        else:
            self.users_data[str(self.user.id)]['floppa equiped'][0]= self.users_data[str(self.user.id)]["storage"][self.line-1][0]
            self.users_data[str(self.user.id)]['floppa equiped'][1]= self.users_data[str(self.user.id)]["storage"][self.line-1][1]
            self.users_data[str(self.user.id)]["storage"].pop(self.line-1)
        
        self.storage.trier()
        self.all_lines= range(len(self.storage.in_order)+1)
        self.line= 0
        text= ""
        index= 0
        couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
        
        for i in range(len(self.storage.par_cat)):
            if self.storage.par_cat[i] != []:
                text= f"{text}**----------**\n"
            for flop in self.storage.par_cat[i]:
                index+=1
                text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"
            
        self.embed.description= f"** Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}**\n{text}"
        if len(self.embed.description)>4000:
            self.embed.description = self.embed.description[:4000]+"\n**. . .**"
            self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
        image_file = discord.File(fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]["path"], filename="floppa.png")
        await interaction.message.edit(embed=self.embed, attachments=[image_file])
        self.save()


    @discord.ui.button(emoji="<:droite:1173048491514282014>",style=discord.ButtonStyle.primary)
    async def right_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        
        if self.line == self.all_lines[-1] :
            self.line = 0
            self.children[1].disabled= True
        else:
            self.line += 1
            if self.line != 0:
                self.children[1].disabled= False

        self.storage.trier()
        self.all_lines= range(len(self.storage.in_order)+1)
        text= ""
        index= 0
        couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
        for i in range(len(self.storage.par_cat)):
            if self.storage.par_cat[i] != []:
                text= f"{text}**----------**\n"
            for flop in self.storage.par_cat[i]:
                index+=1
                if self.line == index:
                    text= f"{text}{couloir[i]}**{index} - {fullfloppedia[flop[0]][flop[1]]['name']}**\n"
                    image_file = discord.File(fullfloppedia[flop[0]][flop[1]]['path'], filename="floppa.png")
                else:
                    text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"

        
        if self.line == 0:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"** Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}**\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
                image_file = discord.File(fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]["path"], filename="floppa.png")
        else:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
        try:
            await interaction.message.edit(embed=self.embed, attachments=[image_file], view= self)
        except UnboundLocalError:
            pass
    

    @discord.ui.button(label="Inventaire",style=discord.ButtonStyle.success)
    async def inv_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        utilisateur = self.user
        users_data= self.users_data

        embed = discord.Embed(title= f"Inventaire de {utilisateur.display_name}", description= f"Floppacks : {users_data[str(utilisateur.id)]['packs']} 📦")
        embed.set_thumbnail(url= utilisateur.avatar.url)
        view= Inventory(user=utilisateur, users_data=users_data, saver=self.save)

        if users_data[str(utilisateur.id)]['floppa equiped'] is not None:

            floppid, isshiny = users_data[str(utilisateur.id)]['floppa equiped'][0], users_data[str(utilisateur.id)]['floppa equiped'][1]
            file = discord.File(fullfloppedia[floppid][isshiny]['path'], filename="floppa.png")
            embed.set_image(url="attachment://floppa.png")
            embed.add_field(name="Floppa équipé :", value= f"**{fullfloppedia[floppid][isshiny]['name']}**", inline= False)

            await interaction.message.edit(attachments=[file], embed = embed, view=view)
        else :
            await interaction.message.edit(embed = embed, view=view)


#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Trade(discord.ui.View):

    def __init__(self, *, timeout: float | None = 120, user: discord.User, other_user: discord.User, embed: discord.Embed, users_data: dict):
        super().__init__(timeout=timeout)
        self.user= user
        self.other_user= other_user
        self.children[0].label= user.display_name
        self.children[2].label= other_user.display_name
        self.embed= embed
        self.users_data= users_data
        self.ready= False
        self.other_ready= False
        self.completed= False

    async def on_timeout(self) -> None:
        if self.completed is False:
            try:
                await self.message.edit(content="# Trop tard", embed=None, view=None)
            except AttributeError:
                await self.message.edit_original_response(content="# Trop tard", embed=None, view=None)

    @discord.ui.button(emoji="<:white_checkmark:1173814301744713809>", style=discord.ButtonStyle.success)
    async def left_agree_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.user:
            return
        
        await interaction.response.defer()

        self.ready= True
        button.disabled= True

        await interaction.message.edit(view=self)

        if self.other_ready is True:

            safe_switch= self.users_data[str(self.user.id)]['floppa equiped']
            self.users_data[str(self.user.id)]['floppa equiped']= self.users_data[str(self.other_user.id)]['floppa equiped']
            self.users_data[str(self.other_user.id)]['floppa equiped']= safe_switch

            self.embed.title= "***Échange complété***"
            self.embed.color= discord.Color.green()

            await interaction.message.edit(embed=self.embed, view=None)
            self.completed= True


    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.primary)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user not in [self.user, self.other_user]:
            return
        
        self.embed.title= "Échange annulé"
        self.embed.color= discord.Color.red()

        await interaction.message.edit(embed=self.embed, view=None)



    @discord.ui.button(emoji="<:white_checkmark:1173814301744713809>", style=discord.ButtonStyle.success)
    async def right_agree_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.other_user:
            return
        
        await interaction.response.defer()

        self.other_ready= True
        button.disabled= True

        await interaction.message.edit(view=self)

        if self.ready is True:

            safe_switch= self.users_data[str(self.user.id)]['floppa equiped']
            self.users_data[str(self.user.id)]['floppa equiped']= self.users_data[str(self.other_user.id)]['floppa equiped']
            self.users_data[str(self.other_user.id)]['floppa equiped']= safe_switch

            self.embed.title= "***Échange complété***"
            self.embed.color= discord.Color.green()

            await interaction.message.edit(embed=self.embed, view=None)
            self.completed= True


#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Parie(discord.ui.View):
    """

    Args:
        discord (_type_): _description_
    """
    def __init__(self, *, timeout: float | None = 180, user:discord.User, ennemy:discord.User, users_data:dict, embed:discord.Embed) -> None:
        super().__init__(timeout=timeout)
        self.tour= user
        self.users= {user:ennemy, ennemy:user}
        self.users_data= users_data
        self.embed= embed
        self.paries= {user:None,ennemy:None}
        self.completed= False
        self.check_data()


    async def on_timeout(self) -> None:
        if self.completed is False:
            try:
                await self.message.edit(content="# Vous êtes lents omg",attachements= [], embed= None, view=None)
            except AttributeError:
                try:
                    await self.message.edit_original_response(content="# Vous êtes lents omg", attachements= [], embed= None, view=None)
                except AttributeError:
                    pass


    def check_data(self):
        if self.users_data[str(self.tour.id)]["packs"] == 0:
            self.children[0].disabled = True
        if self.users_data[str(self.tour.id)]["floppa equiped"] is None and self.users_data[str(self.tour.id)]["storage"] == []:
            self.children[1].disabled= False


    async def winner(self, interaction: discord.Interaction, winner= discord.User):
        if type(self.paries[self.users[winner]]) == int:
            self.users_data[str(winner.id)]["packs"] += self.paries[self.users[winner]]
            self.users_data[str(self.users[winner].id)]["packs"] -= self.paries[self.users[winner]]
            mot= f"**{self.paries[self.users[winner]]}** Floppacks"
        else:
            self.users_data[str(winner.id)]["storage"].append(self.paries[self.users[winner]])
            if self.users_data[str(self.users[winner].id)]["floppa equiped"] == self.paries[self.users[winner]]:
                self.users_data[str(self.users[winner].id)]["floppa equiped"] = None
            else:
                self.users_data[str(self.users[winner].id)]["storage"].remove(self.paries[self.users[winner]])
            mot= f"**{fullfloppedia[self.paries[self.users[winner]][0]][self.paries[self.users[winner]][1]]['name']}**"

        await interaction.channel.send(content=f"{winner.display_name} a gagné le parie, il remporte {mot} ! Désolé {self.users[winner].display_name}, ce que t'as parié à été retiré.")


    @discord.ui.button(label="Floppack(s)", emoji="📦", style=discord.ButtonStyle.primary)
    async def pack_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.tour:
            return
        
        await interaction.response.defer()

        self.embed.description= f"**{self.tour.display_name}** tu paries **1** floppacks ?"
        self.paries[self.tour]= 1
        view= Parie_floppacks(part1= self)

        await interaction.message.edit(embed=self.embed, view=view)


    @discord.ui.button(label="Floppa", emoji="<:floppa:1178979356186529812>", style=discord.ButtonStyle.primary)
    async def floppa_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.tour:
            return
        
        await interaction.response.defer()

        user = self.tour
        users_data= self.users_data

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
            self.embed.description=f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            self.embed.set_thumbnail(url="attachment://floppa.png")
            view= Parie_floppa(storage=storage, part1=self)
            await interaction.message.edit(embed=self.embed, view= view)
        else:
            self.embed.description=f"** Équipé: {fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['name']}**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            image_file = discord.File(fullfloppedia[users_data[str(user.id)]['floppa equiped'][0]][users_data[str(user.id)]['floppa equiped'][1]]['path'], filename="floppa.png")
            self.embed.set_thumbnail(url="attachment://floppa.png")
            view= Parie_floppa(storage=storage, part1=self)
            await interaction.message.edit(attachments=[image_file], embed=self.embed, view= view)


    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in list(self.users):
            return
        await interaction.message.edit(content=f"**{interaction.user.display_name} à annulé le parie...**",attachments= [] , embed=None, view= None)
    
     
#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Parie_floppacks(discord.ui.View):


    def __init__(self, *, timeout: float | None = 180, part1: Parie) -> None:
        super().__init__(timeout=timeout)
        self.o= part1
        if self.o.users_data[str(self.o.tour.id)]["packs"] == 1:
            self.children[2].disabled= True


    @discord.ui.button(emoji="<:white_checkmark:1173814301744713809>", style=discord.ButtonStyle.success)
    async def check_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.o.tour:
            return
    
        await interaction.response.defer()

        
        if self.o.paries[self.o.users[self.o.tour]] is None:
            self.o.tour= self.o.users[self.o.tour]
            self.o.embed.description= f"**{self.o.users[self.o.tour].display_name}** parie **{self.o.paries[self.o.users[self.o.tour]]}** Floppacks 📦,\n{self.o.tour.display_name}, Choisie ce que tu paries..."
            view= self.o
        else:
            if type(self.o.paries[self.o.users[self.o.tour]]) == int:
                motun= f"**{self.o.paries[self.o.users[self.o.tour]]}** Floppacks 📦"
            else:
                motun= f"{fullfloppedia[self.o.paries[self.o.users[self.o.tour]][0]][self.o.paries[self.o.users[self.o.tour]][1]]['name']}"
            
            if type(self.o.paries[self.o.tour]) == int:
                motdeux= f"**{self.o.paries[self.o.tour]}** Floppacks 📦"
            else:
                motdeux= f"**{fullfloppedia[self.o.paries[self.o.tour][0]][self.o.paries[self.o.tour][1]]['name']}**"
            
            self.o.embed.description= f"**{self.o.users[self.o.tour].display_name}** parie {motun},\n**{self.o.tour.display_name}** parie {motdeux}."
            self.o.embed.set_footer(text=f"{self.o.users[self.o.tour].display_name} choisie un jeu...")

            self.o.tour= self.o.users[self.o.tour]
            view= Parie_jeux(part1=self.o)

        self.o.check_data()
        await interaction.message.edit(embed=self.o.embed, view= view)


    @discord.ui.button(emoji="<:minus:1178928774725767279>", style=discord.ButtonStyle.primary, disabled=True)
    async def moins_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.o.tour:
            return
    
        await interaction.response.defer()

        self.o.paries[self.o.tour] -= 1

        if self.children[2].disabled is True:
            self.children[2].disabled= False

        if self.o.paries[self.o.tour] == 1:
            button.disabled = True

        self.o.embed.description= f"**{self.o.tour.display_name}** tu paries **{self.o.paries[self.o.tour]}** Floppacks 📦 ?"
        
        await interaction.message.edit(embed=self.o.embed, view=self)


    @discord.ui.button(emoji="<:plus:1178928743419498547>", style=discord.ButtonStyle.primary)
    async def plus_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.o.tour:
            return
    
        await interaction.response.defer()

        self.o.paries[self.o.tour] += 1

        if self.children[1].disabled is True:
            self.children[1].disabled= False

        if self.o.paries[self.o.tour] == self.o.users_data[str(self.o.tour.id)]["packs"]:
            button.disabled = True

        self.o.embed.description= f"**{self.o.tour.display_name}** tu paries **{self.o.paries[self.o.tour]}** Floppacks 📦 ?"
        
        await interaction.message.edit(embed=self.o.embed, view=self)


    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in list(self.o.users):
            return
        await interaction.message.edit(content=f"**{interaction.user.display_name} à annulé le parie...**",attachments= [] , embed=None, view= None)
    
#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________


class Parie_floppa(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, storage: Storage, part1:Parie):
        super().__init__(timeout=timeout)
        self.o= part1
        self.embed= part1.embed
        self.user= storage.user
        self.line= 0
        self.all_lines= range(len(storage.in_order)+1)
        self.storage= storage
        self.users_data= storage.users_data
        if self.users_data[str(self.o.tour.id)]['floppa equiped'] is None:
            self.children[1].disabled= True


    @discord.ui.button(emoji="<:gauche:1173048276480696441>",style=discord.ButtonStyle.primary)
    async def left_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.user:
            return
        
        await interaction.response.defer()

        if self.line == 0 :
            self.line = self.all_lines[-1]
            self.children[1].disabled= False
        else:
            self.line-= 1
            if self.users_data[str(self.user.id)]["floppa equiped"] is None and self.line == 0:
                self.children[1].disabled= True

        self.storage.trier()
        self.all_lines= range(len(self.storage.in_order)+1)
        text= ""
        index= 0
        couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
        for i in range(len(self.storage.par_cat)):
            if self.storage.par_cat[i] != []:
                text= f"{text}**----------**\n"
            for flop in self.storage.par_cat[i]:
                index+=1
                if self.line == index:
                    text= f"{text}{couloir[i]}**{index} - {fullfloppedia[flop[0]][flop[1]]['name']}**\n"
                    image_file = discord.File(fullfloppedia[flop[0]][flop[1]]['path'], filename="floppa.png")
                else:
                    text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"

        
        if self.line == 0:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"** Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}**\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
                image_file = discord.File(fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]["path"], filename="floppa.png")
        else:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
        
        try:
            await interaction.message.edit(embed=self.embed, attachments=[image_file], view= self)
        except UnboundLocalError:
            pass
    

    @discord.ui.button(label="Parier", emoji="<:white_checkmark:1173814301744713809>", style=discord.ButtonStyle.success)
    async def equip_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.user:
            return

        await interaction.response.defer()
        
        if self.line != 0:
            self.o.paries[self.o.tour]= self.users_data[str(self.user.id)]["storage"][self.line-1]
        else:
            self.o.paries[self.o.tour]= self.users_data[str(self.user.id)]["floppa equiped"]

        if self.o.paries[self.o.users[self.o.tour]] != None:
            if type(self.o.paries[self.o.users[self.o.tour]]) == int:
                motun= f"**{self.o.paries[self.o.users[self.o.tour]]}** Floppacks 📦"
            else:
                motun= f"{fullfloppedia[self.o.paries[self.o.users[self.o.tour]][0]][self.o.paries[self.o.users[self.o.tour]][1]]['name']}"
            
            if type(self.o.paries[self.o.tour]) == int:
                motdeux= f"**{self.o.paries[self.o.tour]}** Floppacks 📦"
            else:
                motdeux= f"**{fullfloppedia[self.o.paries[self.o.tour][0]][self.o.paries[self.o.tour][1]]['name']}**"
            
            self.o.embed.description= f"**{self.o.users[self.o.tour].display_name}** parie {motun},\n**{self.o.tour.display_name}** parie {motdeux}."
            self.o.embed.set_footer(text=f"{self.o.users[self.o.tour].display_name} choisie un jeu...")

            self.o.tour= self.o.users[self.o.tour]
            view= Parie_jeux(part1=self.o)
        else:
            self.o.tour= self.o.users[self.o.tour]
            self.o.embed.description= f"**{self.o.users[self.o.tour].display_name}** parie **{fullfloppedia[self.o.paries[self.o.users[self.o.tour]][0]][self.o.paries[self.o.users[self.o.tour]][1]]['name']}**,\n{self.o.tour.display_name}, Choisie ce que tu paries..."
            view= self.o
        
        self.o.check_data()
        await interaction.message.edit(embed=self.o.embed, view=view)



    @discord.ui.button(emoji="<:droite:1173048491514282014>",style=discord.ButtonStyle.primary)
    async def right_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user != self.user:
            return
        
        await interaction.response.defer()
        
        if self.line == self.all_lines[-1] :
            self.line = 0
            if self.users_data[str(self.user.id)]["floppa equiped"] is None:
                self.children[1].disabled= True
        else:
            self.line += 1
            if self.line != 0:
                self.children[1].disabled= False

        self.storage.trier()
        self.all_lines= range(len(self.storage.in_order)+1)
        text= ""
        index= 0
        couloir= ["<:red:1175274156783317094>","<:gold:1175274184612532245>","<:purple:1175274208146755635>","<:blue:1175274230129115168>","<:green:1175274252254056519>","<:grey:1175274272718077962>"]
        for i in range(len(self.storage.par_cat)):
            if self.storage.par_cat[i] != []:
                text= f"{text}**----------**\n"
            for flop in self.storage.par_cat[i]:
                index+=1
                if self.line == index:
                    text= f"{text}{couloir[i]}**{index} - {fullfloppedia[flop[0]][flop[1]]['name']}**\n"
                    image_file = discord.File(fullfloppedia[flop[0]][flop[1]]['path'], filename="floppa.png")
                else:
                    text= f"{text}{couloir[i]}{index} - {fullfloppedia[flop[0]][flop[1]]['name']}\n"

        
        if self.line == 0:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"** Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}**\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
                image_file = discord.File(fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]["path"], filename="floppa.png")
        else:
            self.embed.description= f"** Équipé: Aucun**\n{text}"
            if len(self.embed.description)>4000:
                self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
            if self.users_data[str(self.user.id)]['floppa equiped'] is not None:
                self.embed.description= f"Équipé: {fullfloppedia[self.users_data[str(self.user.id)]['floppa equiped'][0]][self.users_data[str(self.user.id)]['floppa equiped'][1]]['name']}\n{text}"
                if len(self.embed.description)>4000:
                    self.embed.description = self.embed.description[:4000]+"\n**. . .**"
                    self.embed.set_footer(text="Tu as beaucoup trop de Floppas D:, essaye la commande : /removefloppa doublons")
                    
        try:
            await interaction.message.edit(embed=self.embed, attachments=[image_file], view= self)
        except UnboundLocalError:
            pass
    

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in list(self.o.users):
            return
        await interaction.message.edit(content=f"**{interaction.user.display_name} à annulé le parie...**", attachments= [], embed=None, view= None)

#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Select(discord.ui.Select):

    def __init__(self, part1: Parie) -> None:
        self.o= part1
        options=[
            discord.SelectOption(label="Pierre, feuille, ciseaux", emoji="🧻"),
            discord.SelectOption(label="Roulette Russe", emoji="<:gun:1182715561575206962>"),
            discord.SelectOption(label="Mastermind", emoji="🟠"),
        ]
        super().__init__(placeholder="Choisie un jeu", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        if interaction.user != self.o.tour:
            return
        
        await interaction.response.defer()
        
        if self.values[0] == "Pierre, feuille, ciseaux":
            self.o.embed.set_footer(text= "Le jeu sera Pierre, feuille, ciseaux. Vous devez accepter tout les deux pour continuer.")
            view= Parie_validation(part1=self.o, jeu= 0)
            await interaction.message.edit(attachments= [], embed= self.o.embed, view= view)
        
        elif self.values[0] == "Roulette Russe":
            self.o.embed.set_footer(text= "Le jeu sera la Roulette Russe. Vous devez accepter tout les deux pour continuer.")
            view= Parie_validation(part1=self.o, jeu= 1)
            await interaction.message.edit(attachments= [], embed= self.o.embed, view= view)

        elif self.values[0] == "Mastermind":
            self.o.embed.set_footer(text= "Le jeu sera le Mastermind. Vous devez accepter tout les deux pour continuer.")
            view= Parie_validation(part1=self.o, jeu= 2)
            await interaction.message.edit(attachments= [], embed= self.o.embed, view= view)


#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Parie_jeux(discord.ui.View):
  
  def __init__(self, *, timeout: float | None = 180, part1: Parie):
      super().__init__(timeout=timeout)
      self.add_item(Select(part1= part1))
    
#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Parie_validation(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, part1:Parie, jeu:int):
        super().__init__(timeout=timeout)
        self.o= part1
        self.jeu= jeu
        self.agree1= False
        self.agree2= False

    @discord.ui.button(emoji="<:white_checkmark:1173814301744713809>", style=discord.ButtonStyle.success)
    async def agree_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user == list(self.o.users)[0]:
            self.agree1= True
        elif interaction.user == list(self.o.users)[1]:
            self.agree2= True
        else:
            return
        
        await interaction.response.defer()

        if self.agree1 is True and self.agree2 is True :
            self.o.completed= True

            if self.jeu == 0:
                embed= discord.Embed(title="Pierre, Feuille, Ciseaux !", color= discord.Color.blue()).add_field(name="❔", value=f"{self.o.tour.display_name}").add_field(name="*VS*", value="").add_field(name="❔", value=f"{self.o.users[self.o.tour].display_name}")
                view= Pierre_Feuille_Ciseaux(timeout=120,embed=embed, user=self.o.tour, user2= self.o.users[self.o.tour], parie=self.o, users_data=self.o.users_data)
            
            elif self.jeu == 1:
                users= list(self.o.users)
                embed= discord.Embed(color=discord.Color.orange(), title="Roulette Russe...")
                embed.description= f"Ce sera d'abord au tour de **{users[0].display_name}**..."
                for i in range(len(users)):
                    if i == 0:
                        embed.add_field(name= users[i].display_name, value="<:gun:1182715561575206962>")
                        continue
                    embed.add_field(name= "", value=f"{users[i].display_name}")

                view= Roulette_russe(embed=embed, users_liste=users, users_data=self.o.users_data, get_user=None)

            elif self.jeu == 2:
                users= list(self.o.users)
                combi= sample(["🟢","🔵","🟣","🟤","🔴","🟠","🟡"],4)
                embed= discord.Embed(color=discord.Color.orange(), title="Mastermind", description=f"**Tour de {users[0].display_name}**\nChoix:\n⚪⚪⚪⚪\nCombinaison à trouver:\n⚪⚪⚪⚪")
                view= Mastermind(embed=embed, users=users, combinaison=combi, users_data=self.o.users_data)
           
           
            view.message= interaction
            await interaction.message.edit(embed=embed, view=view)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in list(self.o.users):
            return
        await interaction.message.edit(content=f"**{interaction.user.display_name} à annulé le parie...**", attachments= [], embed=None, view= None)

#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Pierre_Feuille_Ciseaux(discord.ui.View):
    """_summary_

    Args:
        discord (_type_): _description_
    """


    def __init__(self, *, timeout: float | None = 60, users_data:dict, embed: discord.Embed, user:discord.User, user2:discord.User= None, parie:Parie | None= None):
        super().__init__(timeout=timeout)
        self.pfc= {"🪨":"✂️",
                   "🧻":"🪨",
                   "✂️":"🧻"}
        self.choix_bot= "".join(sample(["🪨","🧻","✂️"], 1))
        self.embed= embed
        self.user= user
        self.user2= user2
        self.parie= parie
        self.choix_user= None
        self.choix_user2= None
        self.completed= False
        self.users_data= users_data


    async def on_timeout(self) -> None:
        if self.completed is False:
            try:
                await self.message.edit(content="# Trop tard", embed=None, view=None)
            except AttributeError:
                await self.message.edit_original_response(content="# Trop tard", embed=None, view=None)


    async def disable_all(self, interaction:discord.Interaction):
        for item in self.children:
            item.disabled= True
        await interaction.message.edit(embed= self.embed, view= self)


    @discord.ui.button(emoji="🪨", style=discord.ButtonStyle.secondary)
    async def pierre_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if interaction.user not in [self.user, self.user2]:
            return
        
        await interaction.response.defer()
    
        if self.user2 is None:
            if self.pfc["🪨"] == self.choix_bot:
                button.style= discord.ButtonStyle.success
                self.embed.title= "Victoire !"
                self.embed.color= discord.Color.green()
                self.embed.clear_fields()
                self.embed.add_field(name="🪨", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                if randompackadd(2) is True :
                    self.users_data[str(self.user.id)]['packs']+=1
                    await interaction.channel.send(f"{self.user.mention} a trouvé un Floppack 📦!")

            elif "🪨" == self.choix_bot:
                self.embed.title= "Égalité !"
                self.embed.color= discord.Color.orange()
                self.embed.clear_fields()
                self.embed.add_field(name="🪨", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                checkwhowin= list(self.pfc)
                for i in range(len(checkwhowin)):
                    if self.pfc[checkwhowin[i]] == self.choix_bot:
                        self.children[i].style= discord.ButtonStyle.success

            else:
                self.embed.title= "Perdu !"
                button.style= discord.ButtonStyle.danger
                self.embed.color= discord.Color.red()
                self.embed.clear_fields()
                self.embed.add_field(name="🪨", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                checkwhowin= list(self.pfc)
                for i in range(len(checkwhowin)):
                    if self.pfc[checkwhowin[i]] == self.choix_bot:
                        self.children[i].style= discord.ButtonStyle.success

            await self.disable_all(interaction=interaction)
            self.completed= True
            return

        if interaction.user == self.user :
            if self.choix_user != None:
                await interaction.channel.send(f"Tu as déjà choisi, {self.user.display_name}...")
                return
            self.choix_user= "🪨"
            if self.choix_user2 is None:
                return
        
        elif interaction.user == self.user2 :
            if self.choix_user2 != None:
                await interaction.channel.send(f"Tu as déjà choisi, {self.user2.display_name}...")
                return
            else:
                self.choix_user2= "🪨"
                if self.choix_user is None:
                    return

        if self.pfc[self.choix_user] == self.choix_user2:
            self.embed.title= f"Victoire de {self.user.display_name}!"
            self.embed.color= discord.Color.green()
            self.embed.clear_fields()
            self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
            self.embed.add_field(name="VS", value="")
            self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

            if randompackadd(2) is True :
                self.users_data[str(self.user.id)]['packs'] += 1
                await interaction.channel.send(f"{self.user.mention} a trouvé un Floppack 📦!")

            if self.parie is not None:
                await self.parie.winner(interaction=interaction, winner= self.user)

        elif self.choix_user == self.choix_user2:
            self.embed.title= "Égalité !"
            self.embed.color= discord.Color.orange()
            self.embed.clear_fields()
            self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
            self.embed.add_field(name="VS", value="")
            self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

        else:
            if self.pfc[self.choix_user2] == self.choix_user:
                self.embed.title= f"Victoire de {self.user2.display_name}!"
                self.embed.color= discord.Color.red()
                self.embed.clear_fields()
                self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

                if randompackadd(2) is True :
                    self.users_data[str(self.user2.id)]['packs'] += 1
                    await interaction.channel.send(f"{self.user2.mention} a trouvé un Floppack 📦!")

                if self.parie is not None:
                    await self.parie.winner(interaction=interaction, winner= self.user2)
                        
        await self.disable_all(interaction=interaction)
        self.completed= True


    @discord.ui.button(emoji="🧻", style=discord.ButtonStyle.secondary)
    async def papier_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user not in [self.user, self.user2]:
            return
        
        await interaction.response.defer()

        if self.user2 is None:
            if self.pfc["🧻"] == self.choix_bot:
                button.style= discord.ButtonStyle.success
                self.embed.title= "Victoire !"
                self.embed.color= discord.Color.green()
                self.embed.clear_fields()
                self.embed.add_field(name="🧻", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                if randompackadd(2) is True :
                    self.users_data[str(self.user.id)]['packs'] += 1
                    await interaction.channel.send(f"{self.user.mention} a trouvé un Floppack 📦!")

            elif "🧻" == self.choix_bot:
                self.embed.title= "Égalité !"
                self.embed.color= discord.Color.orange()
                self.embed.clear_fields()
                self.embed.add_field(name="🧻", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                checkwhowin= list(self.pfc)
                for i in range(len(checkwhowin)):
                    if self.pfc[checkwhowin[i]] == self.choix_bot:
                        self.children[i].style= discord.ButtonStyle.success

            else:
                self.embed.title= "Perdu !"
                button.style= discord.ButtonStyle.danger
                self.embed.color= discord.Color.red()
                self.embed.clear_fields()
                self.embed.add_field(name="🧻", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                checkwhowin= list(self.pfc)
                for i in range(len(checkwhowin)):
                    if self.pfc[checkwhowin[i]] == self.choix_bot:
                        self.children[i].style= discord.ButtonStyle.success

            await self.disable_all(interaction=interaction)
            self.completed= True
            return

        if interaction.user == self.user :
            if self.choix_user != None:
                await interaction.channel.send(f"Tu as déjà choisi, {self.user.display_name}...")
                return
            self.choix_user= "🧻"
            if self.choix_user2 is None:
                return
        
        elif interaction.user == self.user2 :
            if self.choix_user2 != None:
                await interaction.channel.send(f"Tu as déjà choisi, {self.user2.display_name}...")
                return
            else:
                self.choix_user2= "🧻"
                if self.choix_user is None:
                    return

        if self.pfc[self.choix_user] == self.choix_user2:
            self.embed.title= f"Victoire de {self.user.display_name}!"
            self.embed.color= discord.Color.green()
            self.embed.clear_fields()
            self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
            self.embed.add_field(name="VS", value="")
            self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

            if randompackadd(2) is True :
                self.users_data[str(self.user.id)]['packs'] += 1
                await interaction.channel.send(f"{self.user.mention} a trouvé un Floppack 📦!")

            if self.parie is not None:
                await self.parie.winner(interaction=interaction, winner= self.user)

        elif self.choix_user == self.choix_user2:
            self.embed.title= "Égalité !"
            self.embed.color= discord.Color.orange()
            self.embed.clear_fields()
            self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
            self.embed.add_field(name="VS", value="")
            self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

        else:
            if self.pfc[self.choix_user2] == self.choix_user:
                self.embed.title= f"Victoire de {self.user2.display_name}!"
                self.embed.color= discord.Color.red()
                self.embed.clear_fields()
                self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

                if randompackadd(2) is True :
                    self.users_data[str(self.user2.id)]['packs'] += 1
                    await interaction.channel.send(f"{self.user2.mention} a trouvé un Floppack 📦!")

                if self.parie is not None:
                    await self.parie.winner(interaction=interaction, winner= self.user2)

        await self.disable_all(interaction=interaction)
        self.completed= True


    @discord.ui.button(emoji="✂️", style=discord.ButtonStyle.secondary)
    async def ciseaux_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user not in [self.user, self.user2]:
            return
        
        await interaction.response.defer()

        if self.user2 is None:
            if self.pfc["✂️"] == self.choix_bot:
                button.style= discord.ButtonStyle.success
                self.embed.title= "Victoire !"
                self.embed.color= discord.Color.green()
                self.embed.clear_fields()
                self.embed.add_field(name="✂️", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                if randompackadd(2) is True :
                    self.users_data[str(self.user.id)]['packs'] += 1
                    await interaction.channel.send(f"{self.user.mention} a trouvé un Floppack 📦!")

            elif "✂️" == self.choix_bot:
                self.embed.title= "Égalité !"
                self.embed.color= discord.Color.orange()
                self.embed.clear_fields()
                self.embed.add_field(name="✂️", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                checkwhowin= list(self.pfc)
                for i in range(len(checkwhowin)):
                    if self.pfc[checkwhowin[i]] == self.choix_bot:
                        self.children[i].style= discord.ButtonStyle.success

            else:
                self.embed.title= "Perdu !"
                button.style= discord.ButtonStyle.danger
                self.embed.color= discord.Color.red()
                self.embed.clear_fields()
                self.embed.add_field(name="✂️", value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_bot, value="Floppa Bot")

                checkwhowin= list(self.pfc)
                for i in range(len(checkwhowin)):
                    if self.pfc[checkwhowin[i]] == self.choix_bot:
                        self.children[i].style= discord.ButtonStyle.success

            await self.disable_all(interaction=interaction)
            self.completed= True
            return

        if interaction.user == self.user :
            if self.choix_user != None:
                await interaction.channel.send(f"Tu as déjà choisi, {self.user.display_name}...")
                return
            self.choix_user= "✂️"
            if self.choix_user2 is None:
                return
        
        elif interaction.user == self.user2 :
            if self.choix_user2 != None:
                await interaction.channel.send(f"Tu as déjà choisi, {self.user2.display_name}...")
                return
            else:
                self.choix_user2= "✂️"
                if self.choix_user is None:
                    return

        if self.pfc[self.choix_user] == self.choix_user2:
            self.embed.title= f"Victoire de {self.user.display_name}!"
            self.embed.color= discord.Color.green()
            self.embed.clear_fields()
            self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
            self.embed.add_field(name="VS", value="")
            self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

            if randompackadd(2) is True :
                self.users_data[str(self.user.id)]['packs'] += 1
                await interaction.channel.send(f"{self.user.mention} a trouvé un Floppack 📦!")

            if self.parie is not None:
                await self.parie.winner(interaction=interaction, winner= self.user)

        elif self.choix_user == self.choix_user2:
            self.embed.title= "Égalité !"
            self.embed.color= discord.Color.orange()
            self.embed.clear_fields()
            self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
            self.embed.add_field(name="VS", value="")
            self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

        else:
            if self.pfc[self.choix_user2] == self.choix_user:
                self.embed.title= f"Victoire de {self.user2.display_name}!"
                self.embed.color= discord.Color.red()
                self.embed.clear_fields()
                self.embed.add_field(name=self.choix_user, value=f"{self.user.display_name}")
                self.embed.add_field(name="VS", value="")
                self.embed.add_field(name=self.choix_user2, value=f"{self.user2.display_name}")

                if randompackadd(2) is True :
                    self.users_data[str(self.user2.id)]['packs'] += 1
                    await interaction.channel.send(f"{self.user2.mention} a trouvé un Floppack 📦!")

                if self.parie is not None:
                    await self.parie.winner(interaction=interaction, winner= self.user2)

        await self.disable_all(interaction=interaction)
        self.completed= True

#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Roulette_russe(discord.ui.View):

    def __init__(self, *, timeout: float | None = 300, embed: discord.Embed, users_liste:list, users_data: dict, parie:Parie= None, get_user):
        super().__init__(timeout=timeout)
        self.embed= embed
        self.users= users_liste
        self.tour= 0
        self.gun= sample([True, False, False, False, False, False], 6)
        self.users_data= users_data
        self.parie= parie
        self.get_user= get_user
        self.completed= False


    async def on_timeout(self):
        if self.completed is False:
            try:
                await self.message.edit(content="# Trop lent", embed=None, view=None)
            except AttributeError:
                await self.message.edit_original_response(content="# Trop lent", embed=None, view=None)


    async def tour_suivant(self, interaction:discord.Interaction):
        self.tour+=1
        if self.tour == len(self.users):
            self.tour= 0

        self.embed.description= f"{self.embed.description}Au tour de **{self.users[self.tour].display_name}**..."
        self.embed.clear_fields()

        for i in range(len(self.users)):
            if i == self.tour:
                self.embed.add_field(name= self.users[i].display_name, value="<:floppasuicide:1207472961548722247>")
                continue
            self.embed.add_field(name= "", value=f"{self.users[i].display_name}")

        
        await interaction.message.edit(content=self.users[self.tour].mention, embed=self.embed)

        if self.users[self.tour].bot is True :
            await asyncio.sleep(3)
            if randint(0, len(self.gun)*2)== 1:
                if self.gun.pop() is True:
                    await self.fin_de_game(self.users[0], interaction)
                else:
                    await self.fin_de_game(self.users[self.tour], interaction, False)
            else:
                if self.gun.pop() is True:
                    await self.fin_de_game(self.users[self.tour], interaction)
                else:
                    self.embed.description= f"{self.users[self.tour].display_name} se tire dessus, rien ne se passe...\n"
                    await self.tour_suivant(interaction)

    
    async def fin_de_game(self, perdant:discord.User, interaction:discord.Interaction, dead_status:bool= True):

            if dead_status is True:
                self.embed.description= f"**{perdant.display_name}** est mort...\nFélicitations aux survivants..."
            else:
                self.embed.description= f"**{perdant.display_name}** à tenter de feinter mais la balle n'est pas partie... Il est donc éliminé.\nFélicitations aux survivants..."
            self.embed.title= "Partie terminée."
            self.embed.color= discord.Color.red()

            self.embed.clear_fields()

            for user in self.users:
                if user == perdant:
                    self.embed.add_field(name= user.display_name, value="💀")
                    continue
                self.embed.add_field(name= "", value=f"{user.display_name}")


            await interaction.message.edit(content=None, embed= self.embed, view=None)
            self.completed= True

            for user in self.users:
                if user != perdant and user.bot is False:
                    luck = randint(1, 3)
                    if luck == 1:
                        self.users_data[str(user.id)]["packs"] += 1
                        await interaction.channel.send(f"**{user.display_name}** à trouvé un Floppack 📦!")

            if self.parie is not None:
                await self.parie.winner(interaction=interaction, winner= self.parie.users[perdant])



    @discord.ui.button(emoji="<:floppasuicide:1207472961548722247>", style=discord.ButtonStyle.success)            #--TO DO---------mettre_un_emoji----------------------------------------------------
    async def suicide_callback(self, interaction: discord.Interaction, button: discord.ui.Button):  
        
        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        if self.gun.pop() == True :
            enraillment= randint(0,100)
            if enraillment==1:
                self.embed.description= f"{interaction.user.display_name} se tire dessus, mais la balle n'est pas partie... Peut-être que l'arme s'est enraillée ?\n"
                self.gun.append(True)
                await self.tour_suivant(interaction)
            else:
                await self.fin_de_game(interaction.user, interaction)

        else:
            self.embed.description= f"{interaction.user.display_name} se tire dessus, rien ne se passe...\n"
            await self.tour_suivant(interaction)

            await interaction.message.edit(content=self.users[self.tour].mention, embed=self.embed)



    
    @discord.ui.button(emoji="<:gun:1182715561575206962>", style=discord.ButtonStyle.danger)          
    async def kill_callback(self, interaction: discord.Interaction, button: discord.ui.Button):  
        
        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        if len(self.users) == 2:

            for user in self.users:
                if user != interaction.user:
                    lautre= user

            if self.gun.pop() == True :
                await self.fin_de_game(lautre, interaction)

            else:
                await self.fin_de_game(interaction.user, interaction, False)

        else:
            view=Roulette_users(game=self)
            await interaction.message.edit(view=view)

#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________



class Select_users(discord.ui.Select):

    def __init__(self, game:Roulette_russe) -> None:
        self.o= game
        options=[]
        for user in self.o.users:
            if user != self.o.users[self.o.tour]:
                options.append(discord.SelectOption(label=user.display_name, value= str(user.id)))
        super().__init__(placeholder="Choisie ta victime", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        if interaction.user != self.o.users[self.o.tour]:
            return
        
        await interaction.response.defer()
        
        lautre= self.o.get_user(int(self.values[0]))

        if self.o.gun.pop() == True :
            await self.o.fin_de_game(lautre, interaction)

        else:
            await self.o.fin_de_game(interaction.user, interaction, False)

#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Roulette_users(discord.ui.View):
  
  def __init__(self, *, timeout: float | None = 180, game:Roulette_russe):
      super().__init__(timeout=timeout)
      self.add_item(Select_users(game= game))

#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Mastermind(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, embed:discord.Embed, users:list[discord.User], combinaison:list, users_data:dict, parie:Parie|None=None):
        super().__init__(timeout=timeout)
        self.embed= embed
        self.users= users
        self.users_data= users_data
        self.tour=0
        self.combinaison= combinaison
        self.choix=["⚪","⚪","⚪","⚪"]
        self.indice=["⚪","⚪","⚪","⚪"]
        self.completed= False
        self.parie= parie


    async def on_timeout(self):
        if self.completed is False:
            try:
                await self.message.edit(content="# Trop lent", embed=None, view=None)
            except AttributeError:
                await self.message.edit_original_response(content="# Trop lent", embed=None, view=None)


                
    async def check_couleur(self, interaction:discord.Interaction, couleur):

        for i in range(len(self.choix)):
            if self.choix[i] == "⚪":
                self.choix[i]= couleur
                if self.choix[i] == self.combinaison[i]:
                    self.indice[i] = couleur
                break

        self.embed.description= f"**Tour de {self.users[self.tour].display_name}**\nChoix:\n{''.join(self.choix)}\nCombinaison à trouver:\n{''.join(self.indice)}"
        
        await interaction.message.edit(embed=self.embed, view=self)

        if "⚪" not in self.choix:
            if self.choix == self.combinaison:
                await self.the_end(interaction=interaction, winner=self.users[self.tour])
                return
            self.embed.set_footer(text=f"Dernière tentative de {self.users[self.tour].display_name}: {''.join(self.choix)}")
            await self.tour_suivant(interaction=interaction)
        

    async def tour_suivant(self, interaction:discord.Interaction):

        self.choix = ["⚪","⚪","⚪","⚪"]
        self.tour+=1
        if self.tour == len(self.users):
            self.tour= 0
        
        for child in self.children:
            child.disabled= False

        self.embed.description= f"**Tour de {self.users[self.tour].display_name}**\nChoix:\n{''.join(self.choix)}\nCombinaison à trouver:\n{''.join(self.indice)}"
        
        await interaction.message.edit(content=self.users[self.tour].mention, embed=self.embed, view=self)

        await self.check_bot(interaction=interaction)
    

    def smart_random_color(self):
        couleur="⚪"
        while True:
            if couleur in self.choix or couleur in self.indice:
                couleur= "".join(sample(["🟢","🔵","🟣","🟤","🔴","🟠","🟡"], 1))
            else:
                break
        return couleur


    async def check_bot(self, interaction:discord.Interaction):
        
        if self.users[self.tour].bot is False:
            return
        
        for i in range(len(self.indice)):
            if self.indice[i] == "⚪":
                await self.check_couleur(interaction=interaction, couleur= self.smart_random_color())
            else:
                await self.check_couleur(interaction=interaction, couleur= self.indice[i])



    async def the_end(self, interaction:discord.Interaction, winner:discord.User):
        self.embed.title= "Partie terminée."
        self.embed.color= discord.Color.green()
        self.embed.description= f"**Victoire de {winner.display_name}**\nChoix:\n{''.join(self.choix)}\nCombinaison à trouver:\n{''.join(self.combinaison)}"

        await interaction.message.edit(content=None, embed= self.embed, view=None)
        self.completed= True

        if winner.bot is False:
            luck = randint(1, 3)
            if luck == 1:
                self.users_data[str(winner.id)]["packs"] += 1
                await interaction.channel.send(f"**{winner.display_name}** à trouvé un Floppack 📦!")

        if self.parie is not None:
            await self.parie.winner(interaction=interaction, winner= winner)
    

    @discord.ui.button(emoji="🟢", style=discord.ButtonStyle.secondary)          
    async def vert_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🟢")


    @discord.ui.button(emoji="🔵", style=discord.ButtonStyle.secondary)          
    async def bleu_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🔵")



    @discord.ui.button(emoji="🟣", style=discord.ButtonStyle.secondary)          
    async def purple_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🟣")



    @discord.ui.button(emoji="🟤", style=discord.ButtonStyle.secondary)          
    async def kanaky_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🟤")



    @discord.ui.button(emoji="🔴", style=discord.ButtonStyle.secondary)          
    async def red_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🔴")



    @discord.ui.button(emoji="🟠", style=discord.ButtonStyle.secondary)          
    async def orange_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🟠")




    @discord.ui.button(emoji="🟡", style=discord.ButtonStyle.secondary)          
    async def jaune_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.users[self.tour]:
            return
        
        await interaction.response.defer()

        button.disabled= True
        await self.check_couleur(interaction=interaction, couleur="🟡")




#_________________________________________________________________________________________________________________________________________________




#_________________________________________________________________________________________________________________________________________________

class Leaderboard(discord.ui.View):

    def __init__(self, *, timeout: float | None = 180, users_data:dict):
        super().__init__(timeout=timeout)
        self.users_data= users_data
    
    async def on_timeout(self) -> None:
        try:
            await self.message.edit(view=None)
        except AttributeError:
            try:
                await self.message.edit_original_response(view=None)
            except AttributeError:
                pass
            

    @discord.ui.button(label= "Nombre Messages",style=discord.ButtonStyle.primary, disabled=True)
    async def msg_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = False

        button.disabled = True

        lb= []
        for data in self.users_data.values():
            lb.append({"pseudo":data["pseudo"], "msg count":data["msg count"]})
        
        lb.sort(key=lambda x: x["msg count"], reverse=True)
        msg = "# Floppa Leaderboard\n***Top 10 - Nombres de messages***\n\n```"
        for i in range(10):
            msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
        msg+="```"
        await interaction.message.edit(content=msg, view= self)



    @discord.ui.button(label= "Rank",style=discord.ButtonStyle.primary)
    async def rank_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = False

        button.disabled = True

        lb= []
        for data in self.users_data.values():
            lb.append({"pseudo":data["pseudo"], "msg count":data["lvl"]})
        
        lb.sort(key=lambda x: x["msg count"], reverse=True)
        msg = "# Floppa Leaderboard\n***Top 10 - Rank***\n\n```"
        for i in range(10):
            msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
        msg+="```"
        await interaction.message.edit(content=msg, view= self)

    
    @discord.ui.button(label= "Fidèlité",style=discord.ButtonStyle.primary)
    async def fidel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = False

        button.disabled = True

        lb= []
        for data in self.users_data.values():
            lb.append({"pseudo":data["pseudo"], "msg count":data["fidelite"]})
        
        lb.sort(key=lambda x: x["msg count"], reverse=True)
        msg = "# Floppa Leaderboard\n***Top 10 - Floppa Fidèles***\n\n```"
        for i in range(10):
            msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
        msg+="```"
        await interaction.message.edit(content=msg, view= self)

    
    @discord.ui.button(label= "Prière",style=discord.ButtonStyle.primary)
    async def prier_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = False

        button.disabled = True

        lb= []
        for data in self.users_data.values():
            lb.append({"pseudo":data["pseudo"], "msg count":data["pray_count"]})
        
        lb.sort(key=lambda x: x["msg count"], reverse=True)
        msg = "# Floppa Leaderboard\n***Top 10 - Nombre de Prières***\n\n```"
        for i in range(10):
            msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
        msg+="```"
        await interaction.message.edit(content=msg, view= self)


    @discord.ui.button(label= "Floppas",style=discord.ButtonStyle.primary)
    async def flop_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = False

        button.disabled = True

        lb= []
        for data in self.users_data.values():
            lb.append({"pseudo":data["pseudo"], "msg count":len(data["storage"])})
        
        lb.sort(key=lambda x: x["msg count"], reverse=True)
        msg = "# Floppa Leaderboard\n***Top 10 - Nombre de Floppas***\n\n```"
        for i in range(10):
            msg += f"{i+1} - {lb[i]['pseudo']} : {lb[i]['msg count']}\n"
        msg+="```"
        await interaction.message.edit(content=msg, view= self)