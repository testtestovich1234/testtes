from inspect import FrameInfo
import discord
from discord.ext import commands
import asyncio
import datetime

import vk
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)

token_vk = 
vk_id_ghetto = "2000000001" #ид беседы кф лидеров банд
vk_id_fam = "2000000002" #ид беседы кф лидеров семей

token_ds = "MTAzNzY5NTg1ODQ4NzA4NzE1NA.G-pTXQ.9QFjH7s-bRX0mF-6VmXqzG8exAW1qnZ7WSLq6c" #токен дс бота

vk_session = vk_api.VkApi(token = token_vk)
give = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


zabiv_channel = 813870429831692291 #канал для забивов каптов гетто
capt_info_channel = 813870429831692291 #капт-инфо канал
sled_ghetto = 816323525987401768 #роль следящего гетто, которая будет упинаться при забива
zgs_ghetto = 816323525987401768 #роль Згс следящего гетто, которая будет упинаться при забива

famzabiv_channel = 813870429831692291 #канал для забивов каптов фам
fam_info_channel = 813870429831692291 #фамкапт-инфо канал
sled_fam = 819244493450510366 #роль следящего за фамами, которая будет упинаться при забива

moderator_roles = [
    816323525987401768, #роли следящих за гетто
    816323525987401768,
    816323525987401768
]

fam_moderator_roles = [ 
    819244493450510366, #роли следящих за семьями
    819244493450510366
]

trigger = [
    "!капт",
    "!рп",
    "!нрп",
    "!отбив",
    "!беру мороз",
    "!беру отказ"
]

@client.listen("on_message")
async def on_message(message: discord.Message):
    if message.author.bot: return
    if message.channel.id == zabiv_channel:
        for msg in trigger:
            all_messages = message.content
            if msg in all_messages.lower():
                author = message.author
                sled_role = discord.utils.get(message.guild.roles, id=sled_ghetto)
                zgs_role = discord.utils.get(message.guild.roles, id=zgs_ghetto)
                await message.delete()
                await message.channel.send((f'**{sled_role.mention} {zgs_role.mention}| От: {author.mention}**'))
                await message.channel.send((f'```{message.content}```\nЗабил: {author}'), view=Buttons())
    if message.channel.id == famzabiv_channel:
        all_messages = message.content
        if "!забив" in all_messages.lower():
            author = message.author
            sled_famrole = discord.utils.get(message.guild.roles, id=sled_fam)
            await message.delete()
            await message.channel.send((f'**{sled_famrole.mention} | От: {author.mention}**'))
            await message.channel.send((f'```{message.content}```\nЗабил: {author}'), view=ButtonsFam())
    if message.channel.id == famzabiv_channel or message.channel.id == zabiv_channel:
        all_messages = message.content
        if "!инфо" in all_messages.lower():
            await message.delete()
            embedInfo = discord.Embed(title="🌹 Arizona Saint Rose 🌹| Информация по боту 📋", description=f"Бот функционирует для семейных и гетто каптов.", color=0xFF69B4)
            embedInfo.add_field(name="**Гетто капты 🔫**", value=f"Команды 🔖\n```!капт, !откат, !беру мороз, !беру отказ```", inline=False)
            embedInfo.add_field(name="** **", value=f"Примеры форм 📄\n*!капт вагос от нв на 17:30\n!отбив грув от рифа на 20:40\n!беру мороз на 2 дня, причина: состав\n!беру отказ от каптов на 24 часа*", inline=True)

            embedInfo.add_field(name="**Семейные капты 🧨**", value=f"Команды 🔖\n```!забив```", inline=False)
            embedInfo.add_field(name="** **", value=f"Примеры форм 📄\n*!забив [название семьи] от [название семьи], дата и время, условия забива*", inline=True) 
            embedInfo.set_image(url="https://i.imgur.com/dIhVWv6.png")
            embedInfo.set_footer(text=f"Bot created with ❤️ by blessave", icon_url="https://i.imgur.com/S3u0Psn.png")
            await message.channel.send(embed=embedInfo, delete_after=100)
   
            

class Buttons(discord.ui.View):
    def __init__(self, capt=None, timeout=1802344234230):
        super().__init__(timeout=timeout)
        self.capture = capt

    @discord.ui.button(label="Подтвердить", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for role in interaction.user.roles:
            if role.id in moderator_roles:
                await interaction.response.send_message(content=f"✅ **Капт подтверждён администратором {interaction.user.mention}**")
                channel = client.get_channel(capt_info_channel)
                embedVar = discord.Embed(title="🌹 Arizona Saint Rose 🌹| Система гетто каптов 🥩", description=f"", timestamp=datetime.datetime.utcnow(), color=0x7FFFD4)
                embedVar.add_field(name="** **", value=f"{interaction.message.content}\n✅ **Подтвердил: **{interaction.user.mention}", inline=False)
                await channel.send(embed=embedVar)
                text = interaction.message.content
                res_text = text.replace('`', '') 
                vk_session.method("messages.send", {"peer_id": vk_id_ghetto, "message": f"🌹 Arizona Saint Rose 🌹| Система гетто каптов 🥩\n{res_text}\n✅ Подтвердил: {interaction.user}", "random_id": 0})
                return

    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for role in interaction.user.roles:
            if role.id in moderator_roles:
                await interaction.response.send_message(
                    content=f"⛔️ **Капт отклонён администратором {interaction.user.mention}**")

                
class ButtonsFam(discord.ui.View):
    def __init__(self, capt=None, timeout=180423423430):
        super().__init__(timeout=timeout)
        self.capture = capt

    @discord.ui.button(label="Подтвердить", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for role in interaction.user.roles:
            if role.id in fam_moderator_roles:
                await interaction.response.send_message(content=f"✅ **Фамкапт подтверждён администратором {interaction.user.mention}**")
                channel = client.get_channel(fam_info_channel)
                embedVar = discord.Embed(title="🌹 Arizona Saint Rose 🌹| Система семейных каптов 🧰", description=f"", timestamp=datetime.datetime.utcnow(), color=0xF0E68C)
                embedVar.add_field(name="** **", value=f"{interaction.message.content}\n✅ **Подтвердил: **{interaction.user.mention}", inline=False)
                await channel.send(embed=embedVar)
                text = interaction.message.content
                res_text = text.replace('`', '') 
                vk_session.method("messages.send", {"peer_id": vk_id_fam, "message": f"🌹 Arizona Saint Rose 🌹| Система семейных каптов 🧰\n{res_text}\n✅ Подтвердил: {interaction.user}", "random_id": 0})
                return

    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for role in interaction.user.roles:
            if role.id in fam_moderator_roles:
                await interaction.response.send_message(
                    content=f"⛔️ **Фамкапт отклонён администратором {interaction.user.mention}**")

client.run(token_ds)
